#!/bin/bash -xe

yum -y update

yum -y install httpd
amazon-linux-extras install -y php7.2
amazon-linux-extras install epel -y
systemctl enable httpd
systemctl start httpd

echo "<html><head></head><body>" >> /var/www/html/index.html
echo "<center><h1>G'day!</h1></center><br>" >> /var/www/html/index.html
echo "</body></html>" >> /var/www/html/index.html

usermod -a -G apache ec2-user   
chown -R ec2-user:apache /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} \;
find /var/www -type f -exec chmod 0664 {} \;