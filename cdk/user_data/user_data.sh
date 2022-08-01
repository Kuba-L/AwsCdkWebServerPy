#!/bin/bash -xe

sudo su
yum -y update

yum -y install httpd
amazon-linux-extras install -y php7.2
amazon-linux-extras install epel -y
systemctl enable httpd
systemctl start httpd

aws s3 cp s3://artifacts-bucket-for-that-web-server-yup/index.html /var/www/html/index.html

usermod -a -G apache ec2-user   
chown -R ec2-user:apache /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} \;
find /var/www -type f -exec chmod 0664 {} \;
