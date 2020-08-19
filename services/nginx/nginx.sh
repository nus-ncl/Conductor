#!/bin/bash

sudo apt-get install build-essential -y
sudo apt-get install libpcre3 libpcre3-dev libpcrecpp0v5 libssl-dev zlib1g-dev -y
wget http://nginx.org/download/nginx-1.4.0.tar.gz
tar zxf nginx-1.4.0.tar.gz
cd nginx-1.4.0
./configure --prefix=/usr \
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
sudo update-rc.d -f nginx defaults
sudo service nginx restart


