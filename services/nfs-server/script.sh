# service: nfs-server
sudo apt install -y nfs-kernel-server
if ! grep "{{ configuration['mount_src_directory'] }} *(rw,insecure,no_subtree_check,no_root_squash)" /etc/exports; then echo "{{ configuration['mount_src_directory'] }} *(rw,insecure,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports; else echo 'exists!'; fi
sudo service nfs-kernel-server restart

# tar -xzvf /mnt/sda3/attribution.tar.gz -C /mnt/sda3/
# {{ mount_src_directory }} *(rw, insecure, no_subtree_check, no_root_squash)