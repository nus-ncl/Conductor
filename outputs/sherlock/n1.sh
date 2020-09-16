#!/bin/bash

# virtualbox extpack & ssh key
wget https://download.virtualbox.org/virtualbox/5.2.12/Oracle_VM_VirtualBox_Extension_Pack-5.2.12.vbox-extpack -O ~/Extension_Pack
sudo vboxmanage extpack install ~/Extension_Pack
vboxmanage extpack install ~/Extension_Pack
vboxmanage list extpacks
ssh-keygen -t rsa
# ssh-copy-id vagrant@remote_VMs_ip


# ansible
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get -y install ansible



# attribution
# first prepare attribution.tar.gz at /mnt/sda3/
tar -xzvf /mnt/sda3/attribution.tar.gz -C /mnt/sda3/
if ! grep "/mnt/sda3/attribution *(rw,insecure,no_subtree_check,no_root_squash)" /etc/exports; then echo "/mnt/sda3/attribution *(rw,insecure,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports; else echo 'exists!'; fi



