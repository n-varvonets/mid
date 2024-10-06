
# Создание кастомной инфраструктуры AWS с использованием Terraform

Если требуется создать свою собственную инфраструктуру с кастомной VPC и подсетями, рекомендуется выполнить следующие шаги:

## 1. Создание кастомной VPC

Для создания кастомной VPC используйте ресурс `aws_vpc`. Пример создания кастомной VPC с CIDR-блоком `10.0.0.0/16`:

```hcl
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "MyCustomVPC"
  }
}
```

- **cidr_block**: Указывает диапазон IP-адресов для VPC.
- **tags**: Используются для добавления метаданных для ресурса, например, имени.

## 2. Создание кастомных подсетей

После создания VPC создайте подсети для размещения ресурсов в различных зонах доступности (Availability Zones). Используйте ресурс `aws_subnet`:

```hcl
resource "aws_subnet" "my_subnet_az1" {
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = data.aws_availability_zones.available.names[0]
}

resource "aws_subnet" "my_subnet_az2" {
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = data.aws_availability_zones.available.names[1]
}
```

- **vpc_id**: Идентификатор VPC, к которой принадлежит подсеть.
- **cidr_block**: Диапазон IP-адресов для каждой подсети.
- **availability_zone**: Указывает зону доступности, в которой будет создана подсеть. Здесь используются разные зоны для обеспечения отказоустойчивости.

## 3. Использование созданных подсетей в Auto Scaling Group

После создания кастомных подсетей, их можно использовать в ресурсе `aws_autoscaling_group`. Пример использования подсетей:

```hcl
resource "aws_autoscaling_group" "web" {
  name                 = "WebServer-Highly-Available-ASG"
  launch_configuration = aws_launch_configuration.web.name

  min_size = 2
  max_size = 2
  vpc_zone_identifier = [aws_subnet.my_subnet_az1.id, aws_subnet.my_subnet_az2.id]

  # Остальные параметры настройки
}
```

- **vpc_zone_identifier**: Список идентификаторов подсетей, в которых Auto Scaling Group будет запускать экземпляры. Используются ранее созданные подсети.

## Заключение

В текущем файле `main.tf` не создаётся кастомная VPC, а используются подсети из дефолтной VPC, которую AWS предоставляет по умолчанию. Если требуется полная настройка с созданием новой VPC и подсетей, необходимо добавить ресурсы `aws_vpc` и `aws_subnet`, что позволит полностью контролировать параметры сети, такие как CIDR-блоки и зоны доступности.

Использование кастомной VPC и подсетей позволяет настроить сеть под специфические нужды проекта, улучшить безопасность и оптимизировать распределение ресурсов в AWS.
