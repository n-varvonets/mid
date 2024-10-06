#------------------------------------
# My Terraform
#
# Find Latest AMI id of:
#   - Ubuntu 18.04
#   - Amazon Linux 2
#   - Windows Server 2016 Base
#
# High level website with:
# - security group
# - launch instances with Auto-AMI with ZerDownTime(due updating sources OUR DOMAIN(url) always running, by other words it constantly will be working)
# -- by using green/blue deployment
# - Auto scaling group using 2 availability zones
# - Classic Load Balancer in 2 availability zones

# Made by Nick Varvonets
#
# ------------------------------------ 0. prepared data ------------------------------------


provider "aws" {
  region = "ca-central-1"
}


data "aws_availability_zones" "available" {}

data "aws_ami" "latest_amazon_linux" {
  owners = ["amazon"]
  most_recent = true
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# ------------------------------------ 1. security group ------------------------------------
resource "aws_security_group" "web" {
  name        = "WebServer Security Group"
  description = "My First SecurityGroup"

  dynamic "ingress" {
    # типовые
    for_each = ["80", "443", "8080", "1541", "9092"]
    content {
      from_port = ingress.value
      to_port   = ingress.value
      protocol  = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  ingress {
    # кастомный сидр
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["10.10.0.0/16"]
  }

  egress {
    # (то что Уходит С сервера)
    from_port = 0
    to_port   = 0
    protocol = "-1" # -1 любой протокл
    cidr_blocks = ["0.0.0.0/0"]
    #     prefix_list_ids = ["pl-12c4e678"]  #
  }
}
# ------------------------------------ 2. launch instances ------------------------------------
resource "aws_launch_configuration" "web" {
  name          = "WebServer-Highly-Available-LC"
  image_id      = data.aws_ami.latest_amazon_linux.id
  instance_type = "t3.micro"
  security_groups = [aws_security_group.web.id]
  user_data = file("user_data.sh.tpl")

  lifecycle {
    create_before_destroy = true
  }
}

# ------------------------------------ 3. Auto scaling group using 2 availability zones ------------------------------------
resource "aws_autoscaling_group" "web" {
  name                 = "WebServer-Highly-Available-ASG"
  launch_configuration = aws_launch_configuration.web.name

  # min_size указывает минимальное количество экземпляров, которые всегда должны быть запущены в группе авто-масштабирования.
  # Установка min_size в значение 2 гарантирует, что всегда будет запущено минимум 2 экземпляра для обеспечения резервирования.
  min_size = 2

  # max_size указывает максимальное количество экземпляров, которые могут быть созданы группой авто-масштабирования.
  # Установка max_size в значение 2 ограничивает масштабирование, гарантируя, что будет не более 2 экземпляров.
  # В данном случае, min_size и max_size установлены в 2, что создаёт фиксированную группу из 2 экземпляров.
  max_size = 2

  # min_elb_capacity указывает минимальное количество экземпляров, которые должны быть здоровыми и доступными для балансировщика нагрузки.
  # Установка в значение 2 гарантирует, что как минимум 2 экземпляра всегда будут доступны для обслуживания трафика через ELB.
  min_elb_capacity = 2

  # health_check_type может быть установлен в "ELB" или "EC2":
  # - "ELB": Проверки здоровья выполняются на основе проверок здоровья балансировщика нагрузки. Используйте этот вариант, когда экземпляры
  #   обслуживаются ELB, так как проверки ELB обеспечивают более комплексную проверку доступности.
  # - "EC2": Проверки здоровья выполняются на основе проверок статуса экземпляров, предоставленных AWS. Используйте этот вариант,
  #   если у вас нет балансировщика нагрузки, либо для более простых проверок. В данном случае рекомендуется "ELB", так как
  #   он предоставляет более комплексную проверку здоровья при использовании ELB.
  health_check_type = "ELB"

  vpc_zone_identifier = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id] # !!!!!
  # !!!!! Здесь нужно указать идентификаторы подсетей (subnet IDs) после создания необходимых подсетей VPC.

  load_balancers = [aws_elb.web.name]  # !!!!!
  # !!!!! Здесь нужно указать имя ресурса балансировщика нагрузки после его создания.

  dynamic "tag" {
    for_each = {
      Name   = "WebServer in ASG"
      Owner  = "Denis Astahov"
      TAGKEY = "TAGVALUE"
    }
    content {
      key   = tag.key
      value = tag.value

      # propagate_at_launch указывает, нужно ли добавлять тег к экземплярам, которые запускаются группой авто-масштабирования.
      # Установка значения в true означает, что теги, определённые здесь, будут автоматически добавлены к экземплярам при их создании.
      propagate_at_launch = true
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}


# ------------------------------------ 4. loud balancer ------------------------------------

resource "aws_elb" "web" {
  name = "WebServer-HA-ELB"

  # Доступные зоны для балансировщика нагрузки.
  # Возможные значения: ["us-east-1a", "us-east-1b", "us-east-1c", ...]
  # Используются разные зоны для обеспечения высокой доступности.
  availability_zones = [data.aws_availability_zones.available.names[0], data.aws_availability_zones.available.names[1]]

  # Группы безопасности для балансировщика.
  # Возможное значение: ["sg-0b12f34a56789abc0"]
  # Здесь используется группа безопасности, которая контролирует доступ к ELB.
  security_groups = [aws_security_group.web.id]

  # Настройка слушателя для балансировщика нагрузки
  # Это как вахтёр или система на входе, которая проверяет и направляет запросы.
  # Например, если люди хотят войти в определённый сервер, слушатель перенаправляет их к нужной двери (серверу).
  listener {
    lb_port = 80             # Порт балансировщика (лоад банасер)
    lb_protocol = "http"         # Протокол балансировщика (HTTP)
    instance_port = 80             # Порт инстанса, к которому подключается LB (хост=сервер=инстанс)
    instance_protocol = "http"         # Протокол инстанса (HTTP)

    # Возможные значения для порта: 80, 443 (HTTPS), 8080 и другие, в зависимости от нужд.
    # HTTP и HTTPS чаще всего используются для доступа к веб-приложениям.
  }

  # Проверка состояния (health check) для балансировщика
  health_check {
    healthy_threshold = 2            # Количество успешных проверок до пометки инстанса как "здорового"
    # Обычно 2-3 проверки достаточны для уверенности в работоспособности.

    unhealthy_threshold = 2            # Количество неудачных проверок до пометки инстанса как "нездорового"
    # Используется значение 2, чтобы исключить случайные ошибки.

    timeout = 3            # Таймаут для проверки состояния (в секундах)
    # Возможное значение: 2-5. Меньшее значение позволяет быстрее определить статус, но увеличивает вероятность ложных ошибок.

    target = "HTTP:80/"   # Цель для проверки состояния (протокол и путь)
    # Возможные значения: "HTTP:80/", "HTTPS:443/health", "TCP:3306".
    # HTTP/HTTPS - часто используется для проверки веб-приложений. TCP - для баз данных и других сервисов.

    interval = 10           # Интервал между проверками состояния (в секундах)
    # Возможные значения: 5-30. Значение 10 позволяет поддерживать баланс между нагрузкой на сервис и скоростью реакции на проблемы.
  }

  # Теги для балансировщика нагрузки
  tags = {
    Name = "WebServer-Highly-Available-ELB" # Имя ресурса для идентификации
    # Возможное значение: любое строковое значение, используемое для удобства в идентификации.
  }
}

# ------------------------------------ add. Default subnets in two availability zones ------------------------------------
# Создание двух подсетей в разных зонах доступности (по умолчанию).
# Эти ресурсы используют существующие подсети в default VPC, а не создают новые.
# Если default VPC была удалена или не существует, Terraform выдаст ошибку.
# Используйте кастомные подсети (`aws_subnet`), если вам нужен полный контроль над сетью.

resource "aws_default_subnet" "default_az1" {
  availability_zone = data.aws_availability_zones.available.names[0]
}

resource "aws_default_subnet" "default_az2" {
  availability_zone = data.aws_availability_zones.available.names[1]
}

## 1. Создание кастомной VPC
# Для создания кастомной VPC используйте ресурс `aws_vpc`. Пример создания кастомной VPC с CIDR-блоком `10.0.0.0/16`:
# resource "aws_vpc" "my_vpc" {
#   cidr_block = "10.0.0.0/16"
#   tags = {
#     Name = "MyCustomVPC"
#   }
# }
#
# - **cidr_block**: Указывает диапазон IP-адресов для VPC.
# - **tags**: Используются для добавления метаданных для ресурса, например, имени.

# ## 2. Создание кастомных подсетей
# После создания VPC создайте подсети для размещения ресурсов в различных зонах доступности (Availability Zones). Используйте ресурс `aws_subnet`:
#
# resource "aws_subnet" "my_subnet_az1" {
#   vpc_id     = aws_vpc.my_vpc.id
#   cidr_block = "10.0.1.0/24"
#   availability_zone = data.aws_availability_zones.available.names[0]
# }
#
# resource "aws_subnet" "my_subnet_az2" {
#   vpc_id     = aws_vpc.my_vpc.id
#   cidr_block = "10.0.2.0/24"
#   availability_zone = data.aws_availability_zones.available.names[1]
# }
#
# - **vpc_id**: Идентификатор VPC, к которой принадлежит подсеть.
# - **cidr_block**: Диапазон IP-адресов для каждой подсети.
# - **availability_zone**: Указывает зону доступности, в которой будет создана подсеть. Здесь используются разные зоны для обеспечения отказоустойчивости.

## 3. Использование созданных подсетей в Auto Scaling Group
# После создания кастомных подсетей, их можно использовать в ресурсе `aws_autoscaling_group`. Пример использования подсетей:

# resource "aws_autoscaling_group" "web" {
#   name                 = "WebServer-Highly-Available-ASG"
#   launch_configuration = aws_launch_configuration.web.name
#
#   min_size = 2
#   max_size = 2
#   vpc_zone_identifier = [aws_subnet.my_subnet_az1.id, aws_subnet.my_subnet_az2.id]
#
#   # Остальные параметры настройки
# }

## Заключение
# В текущем файле `main.tf` не создаётся кастомная VPC, а используются подсети из дефолтной VPC, которую AWS
# предоставляет по умолчанию. Если требуется полная настройка с созданием новой VPC и подсетей, необходимо добавить
# ресурсы `aws_vpc` и `aws_subnet`, что позволит полностью контролировать параметры сети, такие как CIDR-блоки и зоны доступности.



# -------------------- output ---------------
output "web_load_balancer_url" {
  value = aws_elb.web.dns_name
}
