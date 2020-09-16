#!/usr/bin/python3
import configparser
from defaults import default

conf = configparser.ConfigParser()
conf.read(default.CONFIG_FILE)

def print_configure_file():
	# print all sections and key-values
	for section in conf.sections():
		print('---------------------')
		print('[%s]' % (section))
		for key in conf[section]:
			print("%s:%s" % (key, conf[section][key]))
		print('---------------------')


def get_teamname():
	return conf.get("Experiment", "teamname")


def get_experimentname():
	return conf.get("Experiment", "experimentname")


def get_lans_num():
	return conf.get("Experiment", "lans_num")


def get_nodes_num():
	return conf.get("Experiment", "nodes_num")


def get_vms_num():
	return conf.get("Experiment", "vms_num")


def get_lans():
	'''
	Construct each lan's info into a dictionary and then combine them into a list
	:return: list
	'''
	lans = []
	for i in range(1, int(get_lans_num()) + 1):
		lan_index = 'LAN' + str(i)
		lan_name = conf.get(lan_index, "name")
		lan_endpoints = conf.get(lan_index, "endpoints")
		lan_endpoints_list = lan_endpoints.split(',')
		lan_entry = {'name': lan_name, 'endpoints': lan_endpoints_list}
		lans.append(lan_entry)
	return lans


def get_nodes():
	'''
	Construct each node's info into a dictionary and then combine them into a list
	:return: list
	'''
	nodes = []
	for i in range(1, int(get_nodes_num()) + 1):
		node_index = 'Node' + str(i)
		node_name = conf.get(node_index, "name")
		node_connectivity = conf.get(node_index, "connectivity")
		node_lan = conf.get(node_index, "lan")
		node_lan_list = node_lan.split(',')
		node_lan_node_ip = conf.get(node_index, "lan_node_ip")
		node_lan_node_ip_list = node_lan_node_ip.split(',')
		node_lan_node_netmask = conf.get(node_index, "lan_node_netmask")
		node_lan_node_netmask_list = node_lan_node_netmask.split(',')
		node_hostonly_network_name = conf.get(node_index, "hostonly_network_name")
		node_hostonly_network_name_list = node_hostonly_network_name.split(',')
		node_hostonly_network_ip = conf.get(node_index, "hostonly_network_ip")
		node_hostonly_network_ip_list = node_hostonly_network_ip.split(',')
		node_hostonly_network_netmask = conf.get(node_index, "hostonly_network_netmask")
		node_hostonly_network_netmask_list = node_hostonly_network_netmask.split(',')
		node_service = conf.get(node_index, "service")
		node_service_list = node_service.split(',')

		node_entry = {'name': node_name, 'connectivity': node_connectivity, 'lan': node_lan_list,
		              'lan_node_ip': node_lan_node_ip_list, 'lan_node_netmask': node_lan_node_netmask_list,
		              'hostonly_network_name': node_hostonly_network_name_list,
		              'hostonly_network_ip': node_hostonly_network_ip_list,
		              'hostonly_network_netmask': node_hostonly_network_netmask_list,
		              'service': node_service_list}
		nodes.append(node_entry)
	return nodes


def get_vms():
	'''
	Construct each vm's info into a dictionary and then combine them into a list
	:return: list
	'''
	vms = []
	for i in range(1, int(get_vms_num()) + 1):
		node_index = 'VM' + str(i)
		vm_node = conf.get(node_index, "node")
		vm_hostname = conf.get(node_index, "hostname")
		vm_provider = conf.get(node_index, "provider")
		vm_hostonly_network = conf.get(node_index, "hostonly_network")
		vm_hostonly_network_list = vm_hostonly_network.split(',')
		vm_hostonly_ip = conf.get(node_index, "hostonly_ip")
		vm_hostonly_ip_list = vm_hostonly_ip.split(',')
		vm_image = conf.get(node_index, "image")
		vm_service = conf.get(node_index, "service")
		vm_service_list = vm_service.split(',')
		vm_activity = conf.get(node_index, "activity")
		vm_activity_list = vm_activity.split(',')
		vm_vrdeport = conf.get(node_index, "vrdeport")
		vm_guest_port_forward = conf.get(node_index, "guest_port_forward")
		vm_guest_port_forward_list = vm_guest_port_forward.split(',')
		vm_host_port_forward = conf.get(node_index, "host_port_forward")
		vm_host_port_forward_list = vm_host_port_forward.split(',')

		vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
		            'hostonly_network': vm_hostonly_network_list, 'hostonly_ip': vm_hostonly_ip_list,
		            'image': vm_image, 'service': vm_service_list, 'activity': vm_activity_list,
		            'vrdeport': vm_vrdeport, 'guest_port_forward': vm_guest_port_forward_list,
		            'host_port_forward': vm_host_port_forward_list}
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
