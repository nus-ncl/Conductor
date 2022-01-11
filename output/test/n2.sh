#!/bin/bash

# virtualbox extpack & ssh key
wget https://download.virtualbox.org/virtualbox/5.2.12/Oracle_VM_VirtualBox_Extension_Pack-5.2.12.vbox-extpack -O ~/Extension_Pack
sudo vboxmanage extpack install ~/Extension_Pack
vboxmanage extpack install ~/Extension_Pack
vboxmanage list extpacks
# used for node to ssh into its VMs
ssh-keygen -t rsa
# ssh-copy-id vagrant@remote_VMs_ip

# Create Host Adapter for VMs
# No need to create real Host Adapter for internal_network, which is specified by 'virtualbox__intnet' in Vagrantfile


# service: nginx (scripts for node)
# This script suits for nginx_version==1.3.9/1.4.0, verification is needed for other versions.

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


