#!/usr/bin/bash
sudo apt install -y nfs-kernel-server
tar -xzvf /mnt/sda3/attribution.tar.gz -C /mnt/sda3/
if ! grep "/mnt/sda3/attribution *(rw,insecure,no_subtree_check,no_root_squash)" /etc/exports; then echo "/mnt/sda3/attribution *(rw,insecure,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports; else echo 'exists!'; fi
sudo service nfs-kernel-server restart
sudo systemctl restart nfs-kernel-server

{{ mount_src_directory }} *(rw, insecure, no_subtree_check, no_root_squash)