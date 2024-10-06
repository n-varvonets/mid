#!/bin/bash
yum -y update
yum -y install httpd

# Получаем локальный IP адрес инстанса, используя метаданные EC2.
myip=`curl http://169.254.169.254/latest/meta-data/local-ipv4`

# Создаем HTML файл для отображения информации на веб-сервере.
cat <<EOF > /var/www/html/index.html
<html>
<body bgcolor="black">
<h2><font color="gold">Build by Power of Terraform <font color="red"> v0.12</font></h2><br><p>
<font color="green">Server PrivateIP: <font color="aqua">$myip</font></p><br>

<font color="magenta">
<b>Version 1.0</b>
</body>
</html>
EOF

# Запускаем веб-сервер Apache.
sudo service httpd start
chkconfig httpd on
