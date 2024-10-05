#------------------------------------
# My Terraform
#
# Build WebServer during Bootstrap
#
# Made by Nick Varvonets
#------------------------------------
provider "aws" {
  region = "eu-central-1"
}


# все 3 инстанса подівмуться одинаково, если не УКАЗЫВАТЬ DEPENDENCY
resource "aws_instance" "my_server_web" {
  ami           = "ami-0592c673f0b1e7665"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.my_webserver.id]

  tags = {
    Name = "Server-Web"
  }
  # добавим что б сначала ДБ поднялась, а потом аппка
  depends_on = [aws_instance.my_server_db]
}

resource "aws_instance" "my_server_app" {
  ami           = "ami-0592c673f0b1e7665"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.my_webserver.id]

  tags = {
    Name = "Server-Application"
  }

  # добавим что б сначала ДБ поднялась, а потом аппка
  depends_on = [aws_instance.my_server_db]
}

resource "aws_instance" "my_server_db" {
  ami           = "ami-0592c673f0b1e7665"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.my_webserver.id]

  tags = {
    Name = "Server-Database"
  }
}


# Resource for creating an EC2 instance for the web server.
resource "aws_instance" "my_webserver" {
  ami           = "ami-0592c673f0b1e7665"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.my_webserver.id]

  # User data to configure the instance during bootstrapping.
  user_data = templatefile("user_data.sh.tpl", {
    f_name = "Denis"
    l_name = "Astahov"
    names = ["Vasya", "Kolya", "Petya", "John", "Donald", "Masha", "Katya"]
  })

  # Tags for identifying and organizing resources.
  tags = {
    Name  = "Web Server Build by Terraform"
    Owner = "Denis Astahov"
  }

  # Lifecycle block to ensure the new instance is created before the old one is destroyed.
  lifecycle {
    create_before_destroy = true
    # Prevents downtime by ensuring that a new instance is ready before terminating the old one.
  }
}

# Security group for the web server instance.
resource "aws_security_group" "my_webserver" {
  name        = "WebServer Security Group"
  description = "My First SecurityGroup"

  # Dynamic ingress block to create multiple ingress rules.
  dynamic "ingress" {
    # типовые (standard ports)
    for_each = ["80", "443", "8080", "1541", "9092"]
    content {
      from_port = ingress.value
      to_port   = ingress.value
      protocol  = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  # Custom CIDR for SSH access.
  ingress {
    # кастомный сидр (custom CIDR)
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["10.10.0.0/16"]
  }

  # Outbound rules (egress).
  egress {
    # (то что Уходит С сервера) - outbound traffic
    from_port = 0
    to_port   = 0
    protocol = "-1" # -1 любой протокл (any protocol)
    cidr_blocks = ["0.0.0.0/0"]
    #     prefix_list_ids = ["pl-12c4e678"]  # Uncomment to use prefix list IDs for additional control
  }
}
