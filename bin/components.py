# all functions' parameters are string type

'''
{'teamname': 'NCLSecurity', 'experimentname': 'Enterprise', 'lans_num': '1', 'nodes_num': '1', 'vms_num': '1',
 'reserved_nodes': ''}
'''

'''
Design Desciplines:
For initialization for each component. 
	If the key's value's type is simple:
		If the key's value's type is a string, None
		If the key's value's type is a num, 0
		If the key's value's type is a list, []
		If the key's value's type is a dict, {}
	If the key's value's type is complicated, Class
'''


class metadata:
	def __init__(self):
		self.teamname = None
		self.experimentname = None
		self.lans_num = 0
		self.nodes_num = 0
		self.vms_num = 0
		self.reserved_nodes = None

	# def __init__(self, teamname, experimentname, lans_num, nodes_num, vms_num, reserve_nodes):
	# 	self.teamname = teamname
	# 	self.experimentname = experimentname
	# 	self.lans_num = lans_num
	# 	self.nodes_num = nodes_num
	# 	self.vms_num = vms_num
	# 	self.reserve_nodes = reserve_nodes

	def set_teamname(self, teamname):
		if teamname == '':
			pass
		else:
			self.teamname = teamname

	def set_experimentname(self, experimentname):
		if experimentname == '':
			pass
		else:
			self.experimentname = experimentname

	def set_lans_num(self, lans_num):
		if lans_num == '':
			pass
		else:
			self.lans_num = int(lans_num)

	def set_nodes_num(self, nodes_num):
		if nodes_num == '':
			pass
		else:
			self.nodes_num = int(nodes_num)

	def set_vms_num(self, vms_num):
		if vms_num == '':
			pass
		else:
			self.vms_num = int(vms_num)

	def set_reserved_nodes(self, reserved_nodes):
		if reserved_nodes == '':
			pass
		else:
			self.reserved_nodes = reserved_nodes

	def get_lans_num(self):
		return self.lans_num

	def get_nodes_num(self):
		return self.nodes_num

	def get_vms_num(self):
		return self.vms_num

	def output(self):
		output = {'teamname': self.teamname, 'experimentname': self.experimentname, 'lans_num': self.lans_num,
		          'nodes_num': self.nodes_num, 'vms_num': self.vms_num, 'reserved_nodes': self.reserved_nodes}
		return output

	def pp(self):
		print(self.teamname, self.experimentname, self.lans_num, self.nodes_num, self.vms_num, self.reserve_nodes)


class endpoint:
	def __init__(self):
		self.name = None
		self.ip = None
		self.netmask = None

	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_ip(self, ip):
		if ip == '':
			pass
		else:
			self.ip = ip

	def set_netmask(self, netmask):
		if netmask == '':
			pass
		else:
			self.netmask = netmask

	def output(self):
		output = {'name': self.name, 'ip': self.ip, 'netmask': self.netmask}
		return output


# {'name': 'lan1', 'endpoints': [{'name': 'n1', 'ip': '172.16.1.1', 'netmask': '255.255.255.0'}]}
class lan:
	def __init__(self):
		self.name = None
		self.endpoints = []

	# def __init__(self, name, endpoints):
	# 	self.name = name
	# 	self.endpoints = endpoints

	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_endpoints_list(self, endpoint_list):
		# endpoints_list is a dictionary list
		self.endpoints = endpoint_list

	def set_endpoints_dict(self, endpoint_dict):
		# endpoints_list is a dictionary
		self.endpoints.append(endpoint_dict)

	def add_endpoints(self, name, ip, netmask):
		# endpoint is a dictionary
		endpoint_entry = endpoint()
		endpoint_entry.set_name(name)
		endpoint_entry.set_ip(ip)
		endpoint_entry.set_netmask(netmask)
		endpoint_entry = endpoint_entry.output()
		self.endpoints.append(endpoint_entry)

	def output(self):
		output = {'name': self.name, 'endpoints': self.endpoints}
		return output

	def pp(self):
		print(self.name, self.endpoints)


class os:
	def __init__(self, type=None, platform=None, release=None, version=None, architecture=None):
		self.type = type
		self.platform = platform
		self.release = release
		self.version = version
		self.architecture = architecture

	def set_type(self, type):
		if type == '':
			pass
		else:
			self.type = type

	def set_platform(self, platform):
		if platform == '':
			pass
		else:
			self.platform = platform

	def set_release(self, release):
		if release == '':
			pass
		else:
			self.release = release

	def set_version(self, version):
		if version == '':
			pass
		else:
			self.version = version

	def set_architecture(self, architecture):
		if architecture == '':
			pass
		else:
			self.architecture = architecture

	def output(self):
		output = {'type': self.type, 'platform': self.platform, 'release': self.release, 'version': self.version,
		          'architecture': self.architecture}
		return output


class hostonly_network:
	def __init__(self):
		self.name = None
		self.ip = None
		self.netmask = None

	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_ip(self, ip):
		if ip == '':
			pass
		else:
			self.ip = ip

	def set_netmask(self, netmask):
		if netmask == '':
			pass
		else:
			self.netmask = netmask

	def output(self):
		output = {'name': self.name, 'ip': self.ip, 'netmask': self.netmask}
		return output


class internal_network:
	def __init__(self):
		self.name = None
		self.ip = None
		self.netmask = None

	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_ip(self, ip):
		if ip == '':
			pass
		else:
			self.ip = ip

	def set_netmask(self, netmask):
		if netmask == '':
			pass
		else:
			self.netmask = netmask

	def output(self):
		output = {'name': self.name, 'ip': self.ip, 'netmask': self.netmask}
		return output


class node_network:
	def __init__(self):
		self.hostonly_network = []
		self.internal_network = []

	def set_hostonly_network(self, hostonly_networks_list):
		self.hostonly_network = hostonly_networks_list

	def set_internal_network(self, internal_networks_list):
		self.internal_network = internal_networks_list

	def add_hostonly_network(self, name, ip, netmask):
		hostonly_network_entry = hostonly_network()
		hostonly_network_entry.set_name(name)
		hostonly_network_entry.set_ip(ip)
		hostonly_network_entry.set_netmask(netmask)
		hostonly_network_entry = hostonly_network_entry.output()

		self.hostonly_network.append(hostonly_network_entry)

	def add_internal_network(self, name, ip, netmask):
		internal_network_entry = hostonly_network()
		internal_network_entry.set_name(name)
		internal_network_entry.set_ip(ip)
		internal_network_entry.set_netmask(netmask)
		internal_network_entry = internal_network_entry.output()

		self.internal_network.append(internal_network_entry)

	def output(self):
		output = {'hostonly_network': self.hostonly_network, 'internal_network': self.internal_network}
		return output


class service:
	def __init__(self):
		self.name = None
		self.parameter = None

	def set_name(self, name):
		self.name = name

	def set_parameter(self, parameter):
		self.parameter = parameter

	def output(self):
		output = {'name': self.name, 'parameter': self.parameter}
		return output


'''
{'name': 'n1',
 'os': {'type': 'node', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'},
 'network': {'hostonly_network': [{'name': 'vboxnet1', 'ip': '172.16.1.1', 'netmask': '255.255.255.0'}],
             'internal_network': []}, 'services': ['nginx']}
'''


class node:
	def __init__(self):
		self.name = ''
		self.os = os()
		self.network = node_network()
		self.services = []

	# def __init__(self, name, lan, lan_node_ip,lan_node_netmask, hostonly_network_name, hostonly_network_ip, service):
	# 	self.name = name
	# 	self.OS = 'Ubuntu1604-64-STD'
	# 	self.connectivity = None
	# 	self.lan = lan
	# 	self.lan_node_ip = lan_node_ip
	# 	self.lan_node_netmask = lan_node_netmask
	# 	self.hostonly_network_name = hostonly_network_name
	# 	self.hostonly_network_ip = hostonly_network_ip
	# 	self.hostonly_network_netmask = ('255.255.255.0,' * len(hostonly_network_name)).split(',')[:-1]
	# 	self.service = service

	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_os(self, os_dict):
		self.os.set_type(os_dict['type'])
		self.os.set_platform(os_dict['platform'])
		self.os.set_release(os_dict['release'])
		self.os.set_version(os_dict['version'])
		self.os.set_architecture(os_dict['architecture'])

	# self.os = self.os.output()

	def set_network(self, network_dict):
		self.network.set_hostonly_network(network_dict['hostonly_network'])
		self.network.set_internal_network(network_dict['internal_network'])

	def add_network(self, network_type, name, ip, netmask):
		if network_type == 'hostonly':
			self.network.add_hostonly_network(name, ip, netmask)

	# self.network=self.network.output()

	def set_services_v1(self, service_list):
		# service_list is a service name list
		self.services = service_list

	def add_services_v1(self, service):
		# service is a service name
		if self.services is None:
			self.services = []
			self.services.append(service)
		else:
			self.services.append(service)

	def set_services_v2(self, service_list):
		# service_list is a service class list
		self.services = service_list

	# ToDo
	def add_services_v2(self, service):
		# service is a service class
		if self.services is None:
			self.services = []
			self.services.append(service)
		else:
			self.services.append(service)

	def output(self):
		output = {'name': self.name, 'os': self.os.output(), 'network': self.network.output(),
		          'services': self.services}
		return output


class vm_network:
	def __init__(self):
		self.gateway = None
		self.type = None
		self.ip = None
		self.netmask = None

	def set_gateway(self, gateway):
		if gateway == '':
			pass
		else:
			self.gateway = gateway

	def set_type(self, type):
		if type == '':
			pass
		else:
			self.type = type

	def set_ip(self, ip):
		if ip == '':
			pass
		else:
			self.ip = ip

	def set_netmask(self, netmask):
		if netmask == '':
			pass
		else:
			self.netmask = netmask

	def output(self):
		output = {'gateway': self.gateway, 'type': self.type, 'ip': self.ip, 'netmask': self.netmask}
		return output


class vrde:
	def __init__(self):
		self.enabled = False
		self.port = None

	def set_enabled(self, enabled):
		# enabled is True or False
		if enabled == '':
			pass
		else:
			self.enabled = enabled

	def set_port(self, port):
		if port == '':
			pass
		else:
			self.port = port

	def output(self):
		output = {'enabled': self.enabled, 'port': self.port}
		return output


class port_forwarding:
	def __init__(self):
		self.guest_port = None
		self.host_port = None

	def set_guest_port(self, guest_port):
		# guest_port is String
		if guest_port == '':
			pass
		else:
			self.guest_port = guest_port

	def set_host_port(self, host_port):
		# host_port is String
		if host_port == '':
			pass
		else:
			self.host_port = host_port

	def output(self):
		output = {'guest_port': self.guest_port, 'host_port': self.host_port}
		return output


'''
{'name': 'VM1', 'node': 'n1', 'provider': 'Virtualbox',
 'os': {'type': 'vagrant', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'},
 'network': [{'gateway': 'vboxnet1', 'ip': '172.16.1.1', 'netmask': '255.255.255.0', 'type': 'hostonly'},
             {'gateway': 'vboxnet2', 'ip': '172.16.1.2', 'netmask': '255.255.255.0', 'type': 'internal'}],
 'vrde': {'enabled': True, 'port': '12345'}, 'port_forwarding': {'guest_port': '22,80', 'host_port': '2200,8000'},
 'services': []}
'''


class vm:
	def __init__(self):
		self.name = None
		self.node = None
		self.provider = None
		self.os = os()
		self.network = []
		self.vrde = vrde()
		self.port_forwarding = port_forwarding()
		self.services = []

	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_node(self, node):
		if node == '':
			pass
		else:
			self.node = node

	def set_provider(self, provider):
		if provider == '':
			pass
		else:
			self.provider = provider

	def set_os(self, os_dict):
		self.os.set_type(os_dict['type'])
		self.os.set_platform(os_dict['platform'])
		self.os.set_release(os_dict['release'])
		self.os.set_version(os_dict['version'])
		self.os.set_architecture(os_dict['architecture'])

	# self.os = self.os.output()

	def set_network(self, network_list):
		self.network = network_list

	def add_network(self, gateway, type, ip, netmask):
		vm_network_entry = vm_network()
		vm_network_entry.set_gateway(gateway)
		vm_network_entry.set_type(type)
		vm_network_entry.set_ip(ip)
		vm_network_entry.set_netmask(netmask)
		vm_network_entry = vm_network_entry.output()
		if self.network is None:
			self.network = []
			self.network.append(vm_network_entry)
		else:
			self.network.append(vm_network_entry)

	def set_vrde(self, vrde_dict):
		self.vrde.set_enabled(vrde_dict['enabled'])
		self.vrde.set_port(vrde_dict['port'])

	def modify_vrde(self, enabled, port):
		self.vrde.set_enabled(enabled)
		self.vrde.set_port(port)

	def set_port_forwarding(self, port_forwarding_dict):
		self.port_forwarding.set_guest_port(port_forwarding_dict['guest_port'])
		self.port_forwarding.set_host_port(port_forwarding_dict['host_port'])

	def modify_port_forwarding(self, guest_port, host_port):
		self.port_forwarding.set_guest_port(guest_port)
		self.port_forwarding.set_host_port(host_port)

	def set_services_v1(self, service_list):
		# service_list is a service name list
		self.services = service_list

	def add_services_v1(self, service):
		# service is a service name
		if self.services is None:
			self.services = []
			self.services.append(service)
		else:
			self.services.append(service)

	def set_services_v2(self, service_list):
		# service_list is a service class list
		self.services = service_list

	def add_services_v2(self, service):
		# service is a service class
		if self.services is None:
			self.services = []
			self.services.append(service)
		else:
			self.services.append(service)

	def output(self):
		output = {'name': self.name, 'node': self.node, 'provider': self.provider, 'os': self.os.output(),
		          'network': self.network, 'vrde': self.vrde.output(), 'port_forwarding': self.port_forwarding.output(),
		          'services': self.services}
		return output
