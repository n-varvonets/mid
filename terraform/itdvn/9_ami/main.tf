#------------------------------------
# My Terraform
#
# Find Latest AMI id of:
#   - Ubuntu 18.04
#   - Amazon Linux 2
#   - Windows Server 2016 Base
#
# Made by Nick Varvonets
#------------------------------------

provider "aws" {
  region = "ca-central-1"
}

data "aws_ami" "latest_ubuntu" {
  # ID владельца AMI - это ID учетной записи, которой принадлежит этот образ.
  # В данном случае "099720109477" - это официальный ID учетной записи Canonical (Ubuntu).
  # Этот ID можно найти в документации AWS или на AWS Marketplace.
  owners = ["099720109477"]

  # Опция "most_recent = true" указывает, что нужно получить самую свежую (последнюю) версию AMI.
  most_recent = true

  # Фильтр для поиска нужного AMI
  filter {
    # Параметр "name" указывает, что будем фильтровать по названию AMI
    name = "name"

    # Значение фильтра указывает шаблон для поиска AMI.
    # В данном случае ищем все образы с именем, начинающимся на "ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-".
    # "*" означает любые символы после основной части имени.
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
    # Эти шаблоны можно найти на AWS Marketplace или в документации на соответствующие образы AMI.
  }
}

output "latest_ubuntu_ami_id" {
  value = data.aws_ami.latest_ubuntu.id
}

output "latest_ubuntu_ami_name" {
  value = data.aws_ami.latest_ubuntu.name
}
