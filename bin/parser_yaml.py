#!/usr/bin/python3
import operating_system
import copy


def print_configure_file(content):
	print(content)


def os_parser(content):
	type = content['type']
	platform = content['platform']
	release = content['release']
	version = content['version']
	architecture = content['architecture']
	return operating_system.os[type][platform][release][version][architecture]


def get_teamname(content):
	return content['metadata']['teamname']


def get_experimentname(content):
	return content['metadata']['experimentname']


def get_lans_num(content):
	return int(content['metadata']['lans_num'])


def get_nodes_num(content):
	return int(content['metadata']['nodes_num'])


def get_vms_num(content):
	return int(content['metadata']['vms_num'])


def get_reserve_nodes(content):
	return content['metadata']['reserve_nodes']


def get_lans(content):
	'''
	Construct each lan's info into a dictionary and then combine them into a list
	:return: list
	'''
	lans = []
	for lan in content['lan']:
		lan_name = lan['name']
		lan_endpoints_list = []
		for endpoint in lan['endpoints']:
			lan_endpoints_list.append(endpoint['name'])
		lan_entry = {'name': lan_name, 'endpoints': lan_endpoints_list}
		lans.append(lan_entry)
	return lans


def get_nodes(content):
	'''
	Construct each node's info into a dictionary and then combine them into a list
	:return: list
	'''
	nodes = []
	for node in content['node']:
		node_name = node['name']
		node_os = os_parser(node['os'])
		node_lan = []
		for lan in content['lan']:
			for endpoint in lan['endpoints']:
				if endpoint['name'] == node_name:
					node_lan_entry = {'lan': lan['name'], 'ip': endpoint['ip'], 'netmask': endpoint['netmask']}
					node_lan.append(node_lan_entry)
		# copy, deepcopy or assignment?
		node_hostonly_network = copy.deepcopy(node['network']['hostonly_network'])
		service = copy.deepcopy(node['service'])

		node_entry = {'name': node_name, 'os': node_os, 'lan': node_lan, 'hostonly_network': node_hostonly_network,
		              'service': service}
		nodes.append(node_entry)
	return nodes


def get_vms(content):
	'''
	Construct each vm's info into a dictionary and then combine them into a list
	:return: list
	'''
	vms = []
	for vm in content['vm']:
		vm_hostname = vm['name']
		vm_node = vm['node']
		vm_provider = vm['provider']
		vm_os = os_parser(vm['os'])
		vm_hostonly_network = []
		for network in vm['network']:
			if network['type'] == 'hostonly':
				vm_hostonly_network_entry = {'gateway': network['gateway'], 'ip': network['ip'],
				                             'netmask': network['netmask']}
				vm_hostonly_network.append(vm_hostonly_network_entry)
		vm_vrde = vm['vrde']['enabled']
		vm_vrdeport = vm['vrde']['port']
		vm_port_forwarding = []
		vm_guest_port_forward_list = str(vm['port_forwarding']['guest_port']).split(',')
		vm_host_port_forward_list = str(vm['port_forwarding']['host_port']).split(',')
		for index in range(len(vm_guest_port_forward_list)):
			vm_port_forwarding_entry = {'guest_port': vm_guest_port_forward_list[index],
			                            'host_port': vm_host_port_forward_list[index]}
			vm_port_forwarding.append(vm_port_forwarding_entry)
		# copy, deepcopy or assignment?
		vm_service_list = copy.deepcopy(vm['service'])
		vm_activity_list = []

		vm_entry = {'hostname': vm_hostname, 'node': vm_node, 'provider': vm_provider, 'os': vm_os,
		            'hostonly_network': vm_hostonly_network, 'vrde': vm_vrde, 'vrdeport': vm_vrdeport,
		            'port_forwarding': vm_port_forwarding, 'service': vm_service_list,
		            'activity': vm_activity_list}
		vms.append(vm_entry)
	return vms


def get_node_lan():
	pass


def get_node_lan_node_ip():
	pass


def get_node_lan_netmask():
	pass


def get_node_host_network_name():
	pass


def get_node_host_network_ip():
	pass


def get_node_host_network_netmask():
	pass


def get_node_service():
	pass


def get_vm_hostname():
	pass


def get_vm_provider():
	pass


def get_vm_hostonly_network():
	pass


def get_vm_hostonly_ip():
	pass


def get_vm_internal_network():
	pass


def get_vm_internal_ip():
	pass


def get_vm_image():
	pass


def get_vm_service():
	pass


def get_vm_activity():
	pass


def get_vm_vrdeport():
	pass


def get_vm_guest_port_forward():
	pass


def get_vm_host_port_forward():
	pass
