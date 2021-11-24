#!/usr/bin/python3

import os
import configparser
from jinja2 import Environment, PackageLoader
from defaults import default


def print_configure_file(config_file):
	conf = configparser.ConfigParser()
	conf.read(config_file)
	# print all sections and key-values
	for section in conf.sections():
		print('---------------------')
		print('[%s]' % (section))
		for key in conf[section]:
			print("%s:%s" % (key, conf[section][key]))
		print('---------------------')


def vagrantfile_renderer(vms):
	file = open(default.VAGRANT_FILE, 'w')
	env = Environment(loader=PackageLoader('templates'))
	Vagrantfile = env.get_template('Vagrantfile.j2')
	content = Vagrantfile.render(vms=vms)
	file.write(content)
	file.close()


def hosts_renderer(vms):
	file = open(default.HOSTS_FILE, 'w')
	env = Environment(loader=PackageLoader('templates'))
	hostsfile = env.get_template('hosts.j2')
	content = hostsfile.render(vms=vms)
	file.write(content)
	file.close()


def ansiblefile_renderer(vms):
	current_dir = os.path.dirname(__file__)
	ROOT_DIR = os.path.abspath(os.path.join(current_dir, os.pardir))
	file = open(default.ANSIBLE_FILE, 'w')
	# ansible file header '---'
	file.write("---\n\n")
	env = Environment(loader=PackageLoader('services'))
	for vm in vms:
		ansiblefile = env.get_template('ansiblefile_header.j2')
		content = ansiblefile.render(vm=vm)
		file.write(content)
		for service in vm['service']:
			ansiblefile = env.get_template(service + '.j2')
			content = ansiblefile.render(vm=vm, USER='{{ ansible_env.USER }}', conductor_path=ROOT_DIR)
			file.write(content)
			file.write('\n\n')
	file.close()


def NSfile_renderer(nodes, lans):
	print(nodes)
	print(lans)
	file = open(default.NS_FILE, 'w')
	env = Environment(loader=PackageLoader('templates'))
	NSfile = env.get_template('NSfile.j2')
	content = NSfile.render(nodes=nodes, lans=lans)
	file.write(content)
	file.close()


# TODO: specify pack version and 'route add -net' & 'hostonlyif'
def nodesfile_renderer(nodes):
	env = Environment(loader=PackageLoader('templates'))
	nodefile = env.get_template('node.j2')
	for node in nodes:
		node_filename = default.NODES_PATH + node['name'] + '.sh'
		file = open(node_filename, 'w')
		# env = Environment(loader=PackageLoader('templates'))
		# nodefile = env.get_template('node.j2')
		content = nodefile.render(node=node)
		file.write(content)
		file.close()


def clientfile_renderer(experiment_metadata, vms):
	file = open(default.CLIENT_FILE, 'w')
	env = Environment(loader=PackageLoader('templates'))
	Clientfile = env.get_template('Client.j2')
	content = Clientfile.render(experiment_metadata=experiment_metadata, vms=vms)
	file.write(content)
	file.close()

def dockerfile_renderer(vms):
	file = open(default.DOCKER_FILE, 'w')
	env = Environment(loader=PackageLoader('templates'))
	Dockerfile = env.get_template('Dockerfile.j2')
	content = Dockerfile.render(vms=vms)
	file.write(content)
	file.close()


if __name__ == "__main__":
	print_configure_file('specification/sherlock/configure.cfg')
	# PRINT = 0
	# NSFILE = 0
	# HOSTS = 0
	# VAGRANTFILE = 0
	# ANSIBLEFILE = 0
	# CLIENTFILE = 0
	# NODESFILE = 0
	# DOCKERFILE = 0
	#
	# conf = configparser.ConfigParser()
	# conf.read(default.CONFIG_FILE)
	# nodes_num = conf.get("Experiment", "nodes_num")
	# lans_num = conf.get("Experiment", "lans_num")
	# vms_num = conf.get("Experiment", "vms_num")
	#
	# # print configure.cfg
	# if (PRINT):
	# 	print_configure_file(default.CONFIG_FILE)
	#
	# # generate NSfile
	# if (NSFILE):
	# 	nodes = []
	# 	for i in range(1, int(nodes_num) + 1):
	# 		node_index = 'Node' + str(i)
	# 		node_name = conf.get(node_index, "name")
	# 		node_connectivity = conf.get(node_index, "connectivity")
	# 		node_lan = conf.get(node_index, "lan")
	# 		node_lan_list = node_lan.split(',')
	# 		node_lan_node_ip = conf.get(node_index, "lan_node_ip")
	# 		node_lan_node_ip_list = node_lan_node_ip.split(',')
	# 		node_entry = {'name': node_name, 'connectivity': node_connectivity, 'lan': node_lan_list,
	# 		              'lan_node_ip': node_lan_node_ip_list, }
	# 		nodes.append(node_entry)
	#
	# 	lans = []
	# 	for i in range(1, int(lans_num) + 1):
	# 		lan_index = 'LAN' + str(i)
	# 		lan_name = conf.get(lan_index, "name")
	# 		lan_endpoints = conf.get(lan_index, "endpoints")
	# 		lan_endpoints_list = lan_endpoints.split(',')
	# 		lan_entry = {'name': lan_name, 'endpoints': lan_endpoints_list}
	# 		lans.append(lan_entry)
	#
	# 	# print(nodes)
	# 	# print(lans)
	# 	NSfile_renderer(nodes, lans)
	#
	# # generate hosts file
	# if (HOSTS):
	# 	vms = []
	# 	for i in range(1, int(vms_num) + 1):
	# 		node_index = 'VM' + str(i)
	# 		vm_node = conf.get(node_index, "node")
	# 		vm_hostname = conf.get(node_index, "hostname")
	# 		vm_provider = conf.get(node_index, "provider")
	# 		vm_hostonly_network = conf.get(node_index, "hostonly_network")
	# 		vm_hostonly_network_list = vm_hostonly_network.split(',')
	# 		vm_hostonly_ip = conf.get(node_index, "hostonly_ip")
	# 		vm_hostonly_ip_list = vm_hostonly_ip.split(',')
	# 		vm_image = conf.get(node_index, "image")
	# 		vm_service = conf.get(node_index, "service")
	# 		vm_service_list = vm_service.split(',')
	# 		vm_activity = conf.get(node_index, "activity")
	# 		vm_activity_list = vm_activity.split(',')
	#
	# 		vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
	# 		            'hostonly_network': vm_hostonly_network_list, 'hostonly_ip': vm_hostonly_ip_list, 'image': vm_image,
	# 		            'service': vm_service_list, 'activity': vm_activity_list}
	# 		vms.append(vm_entry)
	# 	# print(vms)
	# 	hosts_renderer(vms)
	#
	# # generate vagrantfile
	# if (VAGRANTFILE):
	# 	vms = []
	# 	for i in range(1, int(vms_num) + 1):
	# 		node_index = 'VM' + str(i)
	# 		vm_node = conf.get(node_index, "node")
	# 		vm_hostname = conf.get(node_index, "hostname")
	# 		vm_provider = conf.get(node_index, "provider")
	# 		vm_hostonly_network = conf.get(node_index, "hostonly_network")
	# 		vm_hostonly_network_list = vm_hostonly_network.split(',')
	# 		vm_hostonly_ip = conf.get(node_index, "hostonly_ip")
	# 		vm_hostonly_ip_list = vm_hostonly_ip.split(',')
	# 		vm_image = conf.get(node_index, "image")
	# 		vm_service = conf.get(node_index, "service")
	# 		vm_service_list = vm_service.split(',')
	# 		vm_activity = conf.get(node_index, "activity")
	# 		vm_activity_list = vm_activity.split(',')
	# 		vm_vrdeport = conf.get(node_index, "vrdeport")
	# 		vm_guest_port_forward = conf.get(node_index, "guest_port_forward")
	# 		vm_guest_port_forward_list = vm_guest_port_forward.split(',')
	# 		vm_host_port_forward = conf.get(node_index, "host_port_forward")
	# 		vm_host_port_forward_list = vm_host_port_forward.split(',')
	#
	# 		vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
	# 		            'hostonly_network': vm_hostonly_network_list, 'hostonly_ip': vm_hostonly_ip_list, 'image': vm_image,
	# 		            'service': vm_service_list, 'activity': vm_activity_list,
	# 		            'vrdeport': vm_vrdeport, 'guest_port_forward': vm_guest_port_forward_list,
	# 		            'host_port_forward': vm_host_port_forward_list}
	# 		vms.append(vm_entry)
	# 	print(vms)
	# 	vagrantfile_renderer(vms)
	#
	# # generate ansible file
	# if (ANSIBLEFILE):
	# 	vms = []
	# 	for i in range(1, int(vms_num) + 1):
	# 		node_index = 'VM' + str(i)
	# 		vm_node = conf.get(node_index, "node")
	# 		vm_hostname = conf.get(node_index, "hostname")
	# 		vm_provider = conf.get(node_index, "provider")
	# 		vm_hostonly_network = conf.get(node_index, "hostonly_network")
	# 		vm_hostonly_network_list = vm_hostonly_network.split(',')
	# 		vm_hostonly_ip = conf.get(node_index, "hostonly_ip")
	# 		vm_hostonly_ip_list = vm_hostonly_ip.split(',')
	# 		vm_image = conf.get(node_index, "image")
	# 		vm_service = conf.get(node_index, "service")
	# 		vm_service_list = vm_service.split(',')
	# 		vm_activity = conf.get(node_index, "activity")
	# 		vm_activity_list = vm_activity.split(',')
	#
	# 		vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
	# 		            'hostonly_network': vm_hostonly_network_list, 'hostonly_ip': vm_hostonly_ip_list, 'image': vm_image,
	# 		            'service': vm_service_list, 'activity': vm_activity_list}
	# 		vms.append(vm_entry)
	# 	# print(vms)
	# 	ansiblefile_renderer(vms)
	#
	# # generate node configuration file
	# if (NODESFILE):
	# 	nodes = []
	# 	for i in range(1, int(nodes_num) + 1):
	# 		node_index = 'Node' + str(i)
	# 		node_name = conf.get(node_index, "name")
	# 		node_host_network_name = conf.get(node_index, "host_network_name")
	# 		node_host_network_name_list = node_host_network_name.split(',')
	# 		node_host_network_ip = conf.get(node_index, "host_network_ip")
	# 		node_host_network_ip_list = node_host_network_ip.split(',')
	# 		node_host_network_netmask = conf.get(node_index, "host_network_netmask")
	# 		node_host_network_netmask_list = node_host_network_netmask.split(',')
	# 		node_service = conf.get(node_index, "service")
	# 		node_service_list = node_service.split(',')
	#
	# 		node_entry = {'name': node_name, 'host_network_name': node_host_network_name_list, \
	# 		              'host_network_ip': node_host_network_ip_list,
	# 		              'host_network_netmask': node_host_network_netmask_list,
	# 		              'node_service_list': node_service_list}
	# 		nodes.append(node_entry)
	# 	# print(nodes)
	# 	nodesfile_renderer(nodes)
	#
	# # generate clientfile
	# if (CLIENTFILE):
	# 	experiment_metadata = {}
	# 	experimentname = conf.get("Experiment", "experimentname")
	# 	teamname = conf.get("Experiment", "teamname")
	# 	experiment_metadata['ExperimentName'] = experimentname
	# 	experiment_metadata['TeamName'] = teamname
	#
	# 	vms = []
	# 	for i in range(1, int(vms_num) + 1):
	# 		node_index = 'VM' + str(i)
	# 		vm_node = conf.get(node_index, "node")
	# 		vm_hostname = conf.get(node_index, "hostname")
	# 		vm_provider = conf.get(node_index, "provider")
	# 		vm_hostonly_network = conf.get(node_index, "hostonly_network")
	# 		vm_hostonly_network_list = vm_hostonly_network.split(',')
	# 		vm_hostonly_ip = conf.get(node_index, "hostonly_ip")
	# 		vm_hostonly_ip_list = vm_hostonly_ip.split(',')
	# 		vm_internal_network = conf.get(node_index, "internal_network")
	# 		vm_internal_network_list = vm_internal_network.split(',')
	# 		vm_internal_ip = conf.get(node_index, "internal_ip")
	# 		vm_internal_ip_list = vm_internal_ip.split(',')
	# 		vm_image = conf.get(node_index, "image")
	# 		vm_service = conf.get(node_index, "service")
	# 		vm_service_list = vm_service.split(',')
	# 		vm_activity = conf.get(node_index, "activity")
	# 		vm_activity_list = vm_activity.split(',')
	# 		vm_vrdeport = conf.get(node_index, "vrdeport")
	# 		vm_guest_port_forward = conf.get(node_index, "guest_port_forward")
	# 		vm_guest_port_forward_list = vm_guest_port_forward.split(',')
	# 		vm_host_port_forward = conf.get(node_index, "host_port_forward")
	# 		vm_host_port_forward_list = vm_host_port_forward.split(',')
	#
	# 		vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
	# 		            'hostonly_network': vm_hostonly_network_list, 'hostonly_ip': vm_hostonly_ip_list, 'image': vm_image,
	# 		            'service': vm_service_list, 'activity': vm_activity_list, 'vrdeport': vm_vrdeport,
	# 		            'guest_port_forward': vm_guest_port_forward_list,
	# 		            'host_port_forward': vm_host_port_forward_list,
	# 		            'internal_network': vm_internal_network_list, 'internal_ip': vm_internal_ip_list
	# 		            }
	# 		vms.append(vm_entry)
	# 	print(vms)
	# 	clientfile_renderer(experiment_metadata, vms)
	#
	# if (DOCKERFILE):
	# 	vms = []
	# 	for i in range(1, int(vms_num) + 1):
	# 		node_index = 'VM' + str(i)
	# 		vm_node = conf.get(node_index, "node")
	# 		vm_hostname = conf.get(node_index, "hostname")
	# 		vm_provider = conf.get(node_index, "provider")
	# 		vm_hostonly_network = conf.get(node_index, "hostonly_network")
	# 		vm_hostonly_network_list = vm_hostonly_network.split(',')
	# 		vm_hostonly_ip = conf.get(node_index, "hostonly_ip")
	# 		vm_hostonly_ip_list = vm_hostonly_ip.split(',')
	# 		vm_image = conf.get(node_index, "image")
	# 		vm_service = conf.get(node_index, "service")
	# 		vm_service_list = vm_service.split(',')
	# 		vm_activity = conf.get(node_index, "activity")
	# 		vm_activity_list = vm_activity.split(',')
	# 		vm_vrdeport = conf.get(node_index, "vrdeport")
	# 		vm_guest_port_forward = conf.get(node_index, "guest_port_forward")
	# 		vm_guest_port_forward_list = vm_guest_port_forward.split(',')
	# 		vm_host_port_forward = conf.get(node_index, "host_port_forward")
	# 		vm_host_port_forward_list = vm_host_port_forward.split(',')
	#
	# 		vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
	# 		            'hostonly_network': vm_hostonly_network_list, 'hostonly_ip': vm_hostonly_ip_list, 'image': vm_image,
	# 		            'service': vm_service_list, 'activity': vm_activity_list,
	# 		            'vrdeport': vm_vrdeport, 'guest_port_forward': vm_guest_port_forward_list,
	# 		            'host_port_forward': vm_host_port_forward_list}
	# 		vms.append(vm_entry)
	# 	print(vms)
	# 	vagrantfile_renderer(vms)
