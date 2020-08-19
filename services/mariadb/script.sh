#!/usr/bin/bash

# import databases and grants
sudo mysql < ~/VM1/mariadb/sherlock_VM1_all_databases.sql
sudo mysql < ~/VM1/mariadb/sherlock_VM1_all_grants.sql