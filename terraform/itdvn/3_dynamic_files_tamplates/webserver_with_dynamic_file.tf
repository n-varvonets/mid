#------------------------------------
# My Terraform
#
# динаимический файл - єто файл, в котором передаем наши переменные
#
# Build WebServer during Bootstrap
#
# Made by Nick Varvonets
#------------------------------------

provider "aws" {
  region = "eu-central-1"
}

resource "aws_instance" "my_webserver" {
  ami = "ami-0592c673f0b1e7665"  # Amazon Linux AMI
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.my_webserver.id]
  #   user_data = file("user_data.sh")  # через функцию тераформа
  # послать в файл параметры отсюда. нужно файл переимновать с (.tpl) --> user_data.sh.tpl
  user_data = templatefile("user_data.sh.tpl", {
    f_name = "Nick"
    l_name = "Varvonets"
    names_list = ["Vasya", "Kolya", 1]
  })

  tags = {
    Name  = "Web Server Build by Terraform"
    Owner = "Nick Var"
  }
}


resource "aws_security_group" "my_webserver" {
  name        = "WebServer Security Group"
  description = "My First SecurityGroup"

  ingress {
    # TLS ports
    from_port = 80 # 443
    to_port = 80 # 443
    protocol = "tcp" # "-1"
    cidr_blocks = ["0.0.0.0/0"] # add a CIDR block here, 0.0.0.0/0 - любой может к нам постучать со ВСЕГО нета
  }

  ingress {
    # второе правило на ИНКОМИНГ трафик
    from_port = 443
    to_port   = 443
    protocol = "tcp" # "-1"
    cidr_blocks = ["0.0.0.0/0"] # add a CIDR block here, 0.0.0.0/0 - любой может к нам постучать со ВСЕГО нета
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
