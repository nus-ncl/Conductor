# service: attribution (scripts for node)
# first prepare attribution.tar.gz at /mnt/sda3/
tar -xzvf /mnt/sda3/attribution.tar.gz -C /mnt/sda3/
if ! grep "/mnt/sda3/attribution *(rw,insecure,no_subtree_check,no_root_squash)" /etc/exports; then echo "/mnt/sda3/attribution *(rw,insecure,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports; else echo 'exists!'; fi
