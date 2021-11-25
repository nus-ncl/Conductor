'''
input: screenplay.yml
output: specification.yml & activity.yml
'''
import os
import yaml
import operating_system
import copy
import default

dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(dir_path)


def yaml_load_from_screenplay(filename):
	try:
		with open(f"{root_path}/screenplay/{filename}", 'r') as steam:
			return yaml.safe_load(steam)
	except OSError:
		print(f"No Such Screenplay File: {filename}")
		return {}


def yaml_templatefile_load(filename):
	with open(f"{default.CONDUCTOR_PATH}/template/{filename}", 'r') as stream:
		return yaml.safe_load(stream)


def generate_specification_version():
	return default.VERSION


def generate_specification_properties():
	properties = {}
	properties['platform'] = default.PLATFORM
	properties['format'] = default.FORMAT

	return properties


def generate_specification_metadata(content):
	metadata = {}
	if 'metadata' not in content:
		print(f"No metadata checked")
		pass
	else:
		metadata['teamname'] = get_teamname(content)
		metadata['experimentname'] = get_experimentname(content)
		# metadata['lan_num'] = default.LAN_NUMBER
		metadata['lan_num'] = get_network_num(content)
		metadata['node_num'] = default.NODE_NUMBER
		metadata['vm_num'] = get_host_num(content)
		# metadata['reserved_node'] = default.RESERVE_NODE
		metadata['reserved_node'] = default.RESERVE_NODE

	return metadata


def generate_specification_lan():
	lans = []
	# lans = [{'name': 'lan1', 'endpoints': [{'name': 'n1', 'ip': '172.16.10.101', 'netmask': '255.255.255.0'},
	#                                        {'name': 'n2', 'ip': '172.16.10.102', 'netmask': '255.255.255.0'}],
	#          {'name': 'lan2', 'endpoints': [{'name': 'n3', 'ip': '172.16.10.103', 'netmask': '255.255.255.0'},
	#                                         {'name': 'n4', 'ip': '172.16.10.104', 'netmask': '255.255.255.0'}]}]
	used_node_account = 1
	for lan in range(0, default.LAN_NUMBER):
		lan_entry = {'name': f"lan{lan + 1}", 'endpoints': []}
		for node in range(0, default.NODE_NUMBER):
			node_entry = {'name': f"n{node + used_node_account}", 'ip': f"172.16.10.10{node + used_node_account}",
			              'netmask': '255.255.255.0'}
			lan_entry['endpoints'].append(node_entry)
		lans.append(lan_entry)
		used_node_account = used_node_account + default.NODE_NUMBER

	return lans


def generate_specification_node(network):
	nodes = []
	for node in range(0, default.NODE_NUMBER):
		node_entry = {'name': f"n{node + 1}", 'connectivity': None, 'hostonly_network': [], 'internal_network': [],
		              'prerequisite': ['ansible'], 'event': []}
		for private_network in range(0, len(network['lan'])):
			private_network_entry = {'name': f"{network['lan'][private_network]['name']}",
			                         'ip': f"192.168.5{private_network + 6}.0",
			                         'netmask': '255.255.255.0'}
			node_entry['hostonly_network'].append(private_network_entry)
		nodes.append(node_entry)

	return nodes


def generate_specification_node_event():
	pass


def generate_specification_vm(host, network):
	vms = []
	for vm_index in range(0, len(host)):
		vm_entry = {'name': host[vm_index]['name'], 'node': 'n1', 'provider': 'virtualbox',
		            'os': {'platform': None, 'release': None, 'version': None, 'bit': None},
		            'network': [], 'vrde': {'enabled': False, 'port': None},
		            'port_forwarding': {'guest_port': None, 'host_port': None}, 'prerequisite': ['essentials_common']}
		platform, release, version, bit = generate_specification_os(host[vm_index]['os'])
		vm_entry['os']['platform'] = platform
		vm_entry['os']['release'] = release
		vm_entry['os']['version'] = version
		vm_entry['os']['bit'] = bit

		for private_network in network['lan']:
			if host[vm_index]['name'] in private_network['endpoints']:
				vm_network_entry = {'name': private_network['name'], 'type': 'hostonly', 'ip': None,
				                    'netmask': '255.255.255.0', 'gateway': None}
				vm_entry['network'].append(vm_network_entry)
		vms.append(vm_entry)
	return vms


def generate_specification_vm_event(screenplay):
	vm_event = []
	pass

def generate_specification_files(screenplay):
	pass

def vm_ip_allocation(specification):
	node_lan_network_ip = {}
	for node in specification['node']:
		node_lan_network_ip[node['name']] = {}
		for lan in node['hostonly_network']:
			node_lan_network_ip[node['name']][lan['name']] = lan['ip']

	node_lan_ip_pool = {}
	for node in specification['node']:
		node_lan_ip_pool[node['name']] = {}
		for lan in node['hostonly_network']:
			node_lan_ip_pool[node['name']][lan['name']] = list(range(default.IP_POOL_START, default.IP_POOL_END))

	for vm in specification['vm']:
		# print(vm['name'])
		# node_affiliation = vm['node']
		for vm_network in vm['network']:
			vm_network['ip'] = f"{node_lan_network_ip[vm['node']][vm_network['name']][:-1]}{node_lan_ip_pool[vm['node']][vm_network['name']].pop(0)}"
			vm_network['gateway'] = f"{node_lan_network_ip[vm['node']][vm_network['name']][:-1]}1"

def get_teamname(content):
	return content['metadata']['teamname']


def get_experimentname(content):
	return content['metadata']['experimentname']


def get_network_num(content):
	return int(content['metadata']['network_num'])


def get_host_num(content):
	return int(content['metadata']['host_num'])


def get_lans(content):
	'''
	Construct each lan's info into a dictionary and then combine them into a list
	:return: list
	'''
	lans = []
	if 'lan' not in content:
		return lans
	else:
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
	if 'node' not in content:
		return nodes
	else:
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
			node_internal_network = copy.deepcopy(node['network']['internal_network'])
			services = copy.deepcopy(node['services'])

			node_entry = {'name': node_name, 'os': node_os, 'lan': node_lan, 'hostonly_network': node_hostonly_network,
			              'internal_network': node_internal_network, 'services': services}
			nodes.append(node_entry)
		return nodes


def get_docker_networks(content):
	docker_networks = []
	if 'networks' not in content:
		return docker_networks
	else:
		for network in content['networks']:
			network_name = network['name']
			network_drive = network['driver']
			network_subnet = network['subnet']
			network_gateway = network['gateway']
			network_entry = {'name': network_name, 'driver': network_drive, 'subnet': network_subnet,
			                 'gateway': network_gateway}
			docker_networks.append(network_entry)
		return docker_networks


def get_vms(content):
	'''
	Construct each vm's info into a dictionary and then combine them into a list
	:return: list
	'''
	vms = []
	# print(content['vm'])
	if 'vm' not in content:
		return vms
	else:
		for vm in content['vm']:
			vm_hostname = vm['name']
			vm_node = vm['node']
			vm_provider = vm['provider']
			vm_os = os_parser(vm['os'])
			vm_hostonly_network = []
			vm_internal_network = []
			for network in vm['network']:
				if network['type'] == 'hostonly':
					vm_hostonly_network_entry = {'gateway': network['gateway'], 'ip': network['ip'],
					                             'netmask': network['netmask']}
					vm_hostonly_network.append(vm_hostonly_network_entry)
				elif network['type'] == 'internal':
					vm_internal_network_entry = {'gateway': network['gateway'], 'ip': network['ip'],
					                             'netmask': network['netmask']}
					vm_internal_network.append(vm_internal_network_entry)
			vm_vrde = vm['vrde']['enabled']
			vm_vrdeport = vm['vrde']['port']
			vm_port_forwarding = []
			if (vm['port_forwarding']['guest_port'] is None or vm['port_forwarding']['host_port'] is None):
				vm_port_forwarding = []
			else:
				vm_guest_port_forward_list = str(vm['port_forwarding']['guest_port']).split(',')
				# print(vm_guest_port_forward_list)
				vm_host_port_forward_list = str(vm['port_forwarding']['host_port']).split(',')
				# print(vm_host_port_forward_list)
				for index in range(len(vm_guest_port_forward_list)):
					vm_port_forwarding_entry = {'guest_port': vm_guest_port_forward_list[index],
					                            'host_port': vm_host_port_forward_list[index]}
					vm_port_forwarding.append(vm_port_forwarding_entry)
			# copy, deepcopy or assignment?
			vm_services_list = copy.deepcopy(vm['services'])
			vm_activity_list = []

			vm_entry = {'hostname': vm_hostname, 'node': vm_node, 'provider': vm_provider, 'os': vm_os,
			            'hostonly_network': vm_hostonly_network, 'internal_network': vm_internal_network,
			            'vrde': vm_vrde, 'vrdeport': vm_vrdeport,
			            'port_forwarding': vm_port_forwarding, 'services': vm_services_list,
			            'activity': vm_activity_list}
			vms.append(vm_entry)
		return vms


def get_vms_names(content):
	vms_names = []
	for vm in content['host']:
		vms_names.append(vm['name'])
	return vms_names


def yaml_service_load(filename):
	with open(f"{default.CONDUCTOR_PATH}/services/{filename}/{filename}.yml", 'r') as stream:
		return yaml.safe_load(stream)


def yaml_dump_to_specification(content, filename):
	with open(f"{root_path}/specification/{filename}", 'w') as stream:
		yaml.safe_dump(content, stream, default_flow_style=False, explicit_start=True, allow_unicode=True,
		               sort_keys=False)

def yaml_dump_to_activity(content):
	activity_directory = f"{root_path}/activity/{content['metadata']['experimentname']}"
	for index in range(len(content['file'])):
		content['file'][index] = f"{activity_directory}/{content['file'][index]}"

	for activity in content['activity']:
		for event in activity['event']:
			if '[' in event:
				# print(event) -> install [service]
				# print(event.split(' ')) -> ['install', '[service]']
				for host in content['host']:
					if host['name'] == activity['subject']:
						print(host[event.split(' ')[1][1:-1]])
						# print(host[event.split(' ')[1][1:-1]]) -> print('service')

	output = {'file': content['file'],'activity': content['activity']}

	if not os.path.exists(activity_directory):
		print('Not existed!')
		os.mkdir(activity_directory)
	with open(f"{activity_directory}/activity.yml", 'w') as stream:
		yaml.safe_dump(output, stream, default_flow_style=False, explicit_start=True, allow_unicode=True,
		               sort_keys=False)

def yaml_content_parser(content):
	metadata = get_metadata(content)
	vms = get_vms(content)
	lans = get_lans(content)
	nodes = get_nodes(content)
	networks = get_docker_networks(content)
	return metadata, vms, lans, nodes, networks


def generate_specification_os(platform):
	release, version, bit = platform.split('_')
	if 'window' in release.lower():
		platform = 'Windows'
	else:
		platform = 'Linux'
	return platform, release, version, bit


def os_parser(content):
	type = content['type']
	platform = content['platform']
	release = content['release']
	version = content['version']
	architecture = content['architecture']
	return operating_system.os[type][platform][release][version][architecture]


if __name__ == '__main__':
	specification_output = {}
	specification_output['version'] = generate_specification_version()
	# screenplay_content = yaml_load_from_screenplay('apt32_screenplay.yml')
	screenplay_content = yaml_load_from_screenplay('apt32_screenplay_complicated.yml')

	# activity
	yaml_dump_to_activity(screenplay_content)
	# activity

	# specification
	# specification_output['properties'] = generate_specification_properties()
	# specification_output['metadata'] = generate_specification_metadata(screenplay_content)
	# specification_output['lan'] = generate_specification_lan()
	# specification_output['node'] = generate_specification_node(screenplay_content['network'])
	# if specification_output['properties']['format'] == 'virtual':
	# 	specification_output['vm'] = generate_specification_vm(screenplay_content['host'],
	# 	                                                       screenplay_content['network'])
	# vm_ip_allocation(specification_output)
	# # yaml_dump_to_specification(specification_output, 'apt32_specification.yml')
	# yaml_dump_to_specification(specification_output, 'apt32_specification_complicated.yml')
	# specification
