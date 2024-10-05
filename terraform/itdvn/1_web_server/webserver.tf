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

resource "aws_instance" "my_webserver" {
  ami = "ami-0592c673f0b1e7665"  # Amazon Linux AMI
  instance_type = "t2.micro"
  # берем ВПС, который создаем ниже
  # т.к. код тераформа віполняется сразу, то он увидит его(ХОТЬ даже и ниже стоит)
  vpc_security_group_ids = [aws_security_group.my_webserver.id]
  # можно так же добавить BASH скрипт
  user_data     = <<EOF
#!/bin/bash
yum -y update
yum -y install httpd
myip=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)
echo "<h2>WebServer with IP: $myip</h2><br>Build by Terraform!" > /var/www/html/index.html
sudo service httpd start
chkconfig httpd on
EOF
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
