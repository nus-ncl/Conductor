#!/usr/bin/bash

#expand swap
mkdir /usr/img
rm -rf /usr/img/swap
dd if=/dev/zero of=/usr/img/swap bs=1024 count=2048000
mkswap /usr/img/swap
swapon /usr/img/swap

