#!/usr/bin/env python
# _*_coding:utf-8_*_

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager


def read_hosts(sources):
		hosts_list = []
		loader = DataLoader()
		inventory = InventoryManager(loader=loader, sources=sources)
		variable_manager = VariableManager(loader=loader, inventory=inventory)
		host_list = inventory.hosts
		for _host in host_list:
				host = inventory.get_host(hostname=_host)
				extra_vars = variable_manager.get_vars(host=host)
				ans_port = extra_vars.get("ansible_ssh_port") if extra_vars.get("ansible_ssh_port") else extra_vars.get(
						"ansible_port")
				ans_host = extra_vars.get("ansible_ssh_host") if extra_vars.get("ansible_ssh_host") else extra_vars.get(
						"ansible_host")
				hosts_list.append(
						{"hostname": extra_vars.get("inventory_hostname"), "host": ans_host, "port": ans_port if ans_port else 22,
						 "group_name": extra_vars.get("group_names")})

		return hosts_list


if __name__ == "__main__":
		sources = ["/etc/ansible/hosts"]
		print(read_hosts(sources))
