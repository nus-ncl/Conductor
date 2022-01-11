#!/bin/bash

# virtualbox extpack & ssh key
wget https://download.virtualbox.org/virtualbox/6.0.16/Oracle_VM_VirtualBox_Extension_Pack-6.0.16.vbox-extpack -O ~/Extension_Pack
sudo vboxmanage extpack install ~/Extension_Pack
vboxmanage extpack install ~/Extension_Pack
vboxmanage list extpacks
ssh-keygen -t rsa
# ssh-copy-id vagrant@remote_VMs_ip

# service: nginx (scripts for node)
sudo apt-get install -y build-essential libpcre3 libpcre3-dev libpcrecpp0v5 libssl-dev zlib1g-dev
wget http://nginx.org/download/nginx-1.4.0.tar.gz
tar zxf nginx-1.4.0.tar.gz
cd nginx-1.4.0
./configure \
    --prefix=/usr \
	--conf-path=/etc/nginx/nginx.conf \
	--error-log-path=/var/log/nginx/error.log \
	--http-log-path=/var/log/nginx/access.log \
	--pid-path=/var/run/nginx.pid \
	--lock-path=/var/lock/nginx.lock \
	--with-http_ssl_module \
	--user=www-data \
	--group=www-data \
    --with-http_stub_status_module \
	--with-http_gzip_static_module \
	--without-mail_pop3_module \
	--without-mail_imap_module \
	--without-mail_smtp_module

make
sudo make install


