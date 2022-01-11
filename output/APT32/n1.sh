#!/bin/bash

# virtualbox extpack & ssh key
wget https://download.virtualbox.org/virtualbox/5.2.12/Oracle_VM_VirtualBox_Extension_Pack-5.2.12.vbox-extpack -O ~/Extension_Pack
sudo vboxmanage extpack install ~/Extension_Pack
vboxmanage extpack install ~/Extension_Pack
vboxmanage list extpacks
# ssh-keygen -t rsa
# ssh-copy-id vagrant@remote_VMs_ip







