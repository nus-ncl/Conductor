#!/usr/bin/bash

# make some customized configurations for your apache2
# apache2 configuration for sherlock

if ! grep 'Listen 2080' /etc/apache2/apache2.conf; then echo 'Listen 2080' | sudo tee -a /etc/apache2/apache2.conf; else echo 'exists!'; fi
sudo sed -i 's/:80/:2080/g' /etc/apache2/sites-available/000-default.conf
sudo a2dissite 000-default
sudo a2ensite 000-default
#sudo systemctl reload apache2
#sudo systemctl restart apache2


