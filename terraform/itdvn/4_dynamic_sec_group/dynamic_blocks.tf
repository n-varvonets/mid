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

resource "aws_security_group" "my_webserver" {
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
