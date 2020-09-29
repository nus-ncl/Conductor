# all functions' parameters are string type

class metadata:
	def __init__(self):
		self.teamname = ''
		self.experimentname = ''
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
		self.teamname = teamname

	def set_experimentname(self, experimentname):
		self.experimentname = experimentname

	def set_lans_num(self, lans_num):
		self.lans_num = int(lans_num)

	def set_nodes_num(self, nodes_num):
		self.nodes_num = int(nodes_num)

	def set_vms_num(self, vms_num):
		self.vms_num = int(vms_num)

	def set_reserved_nodes(self, reserved_nodes):
		self.reserved_nodes = reserved_nodes

	# def get_lans_num(self):
	# 	return self.lans_num
	#
	# def get_nodes_num(self):
	# 	return self.nodes_num
	#
	# def get_vms_num(self):
	# 	return self.vms_num

	def output(self):
		output = {
			'metadata': {'teamname': self.teamname, 'experimentname': self.experimentname, 'lans_num': self.lans_num,
			             'nodes_num': self.nodes_num, 'vms_num': self.vms_num, 'reserved_nodes': self.reserved_nodes}}
		return output

	def pp(self):
		print(self.teamname, self.experimentname, self.lans_num, self.nodes_num, self.vms_num, self.reserve_nodes)


class endpoint:
	def __init__(self):
		self.name = ''
		self.ip = ''
		self.netmask = ''

	def set_name(self, name):
		self.name = name

	def set_ip(self, ip):
		self.ip = ip

	def set_netmask(self, netmask):
		self.netmask = netmask

	def output(self):
		output = {'name': self.name, 'ip': self.ip, 'netmask': self.netmask}
		return output


class lan:
	def __init__(self):
		self.name = ''
		self.endpoints = []

	# def __init__(self, name, endpoints):
	# 	self.name = name
	# 	self.endpoints = endpoints

	def set_name(self, name):
		self.name = name

	def set_endpoints(self, endpoint_list):
		# endpoints_list is a dictionary list
		self.endpoints = endpoint_list

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
	def __init__(self):
		self.type = ''
		self.platform = ''
		self.release = ''
		self.version = ''
		self.architecture = ''

	def set_type(self, type):
		self.type = type

	def set_platform(self, platform):
		self.platform = platform

	def set_release(self, release):
		self.release = release

	def set_version(self, version):
		self.version = version

	def set_architecture(self, architecture):
		self.architecture = architecture

	def output(self):
		output = {'type': self.type, 'platform': self.platform, 'release': self.release, 'version': self.version,
		          'architecture': self.architecture}
		return output


class hostonly_network:
	def __init__(self):
		self.name = ''
		self.ip = ''
		self.netmask = ''

	def set_name(self, name):
		self.name = name

	def set_ip(self, ip):
		self.ip = ip

	def set_netmask(self, netmask):
		self.netmask = netmask

	def output(self):
		output = {'name': self.name, 'ip': self.ip, 'netmask': self.netmask}
		return output


class internal_network:
	def __init__(self):
		self.name = ''
		self.ip = ''
		self.netmask = ''


class node_network:
	def __init__(self):
		self.hostonly_network = None
		self.internal_network = None

	def set_hostonly_network(self, hostonly_networks_list):
		self.hostonly_network = hostonly_networks_list

	def add_hostonly_network(self, name, ip, netmask):
		hostonly_network_entry = hostonly_network()
		hostonly_network_entry.set_name(name)
		hostonly_network_entry.set_ip(ip)
		hostonly_network_entry.set_netmask(netmask)
		hostonly_network_entry = hostonly_network_entry.output()

		if self.hostonly_network is None:
			self.hostonly_network = []
			self.hostonly_network.append(hostonly_network_entry)
		else:
			self.hostonly_network.append(hostonly_network_entry)

	def output(self):
		output = {'hostonly_network': self.hostonly_network, 'internal_network': self.internal_network}
		return output


class service:
	def __init__(self):
		self.name = ''
		self.parameter = None

	def set_name(self, name):
		self.name = name

	def set_parameter(self, parameter):
		self.parameter = parameter

	def output(self):
		output = {'name': self.name, 'parameter': self.parameter}
		return output


class node:
	def __init__(self):
		self.name = ''
		self.os = os()
		self.network = node_network()
		self.services = None

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
		self.name = name

	def set_os(self, type, platform, release, version, architecture):
		self.os.set_type(type)
		self.os.set_platform(platform)
		self.os.set_release(release)
		self.os.set_version(version)
		self.os.set_architecture(architecture)
		self.os = self.os.output()

	def set_network(self, network):
		self.network = network

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
		output = {'name': self.name, 'os': self.os, 'network': self.network.output(), 'services': self.services}
		return output


class vm_network:
	def __init__(self):
		self.gateway = ''
		self.type = ''
		self.ip = ''
		self.netmask = ''

	def set_gateway(self, gateway):
		self.gateway = gateway

	def set_type(self, type):
		self.type = type

	def set_ip(self, ip):
		self.ip = ip

	def set_netmask(self, netmask):
		self.netmask = netmask

	def output(self):
		output = {'gateway': self.gateway, 'type': self.type, 'ip': self.ip, 'netmask': self.netmask}
		return output


class vrde:
	def __init__(self):
		self.enabled = True
		self.port = ''

	def set_enabled(self, enabled):
		# enabled is True or False
		self.enabled = enabled

	def set_port(self, port):
		self.port = port

	def output(self):
		output = {'enabled': self.enabled, 'port': self.port}
		return output


class port_forwarding:
	def __init__(self):
		self.guest_port = ''
		self.host_port = ''

	def set_guest_port(self, guest_port):
		# guest_port is String
		self.guest_port = guest_port

	def set_host_port(self, host_port):
		# host_port is String
		self.host_port = host_port

	def output(self):
		output = {'guest_port': self.guest_port, 'host_port': self.host_port}
		return output


class vm:
	def __init__(self):
		self.name = ''
		self.node = ''
		self.provider = ''
		self.os = os()
		self.network = None
		self.vrde = None
		self.port_forwarding = None
		self.services = None

	def set_name(self, name):
		self.name = name

	def set_node(self, node):
		self.node = node

	def set_provider(self, provider):
		self.provider = provider

	def set_os(self, type, platform, release, version, architecture):
		self.os.set_type(type)
		self.os.set_platform(platform)
		self.os.set_release(release)
		self.os.set_version(version)
		self.os.set_architecture(architecture)

	def set_network(self, network):
		self.network = network

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

	def set_vrde(self, enabled, port):
		vrde_entry = vrde()
		vrde_entry.set_enabled(enabled)
		vrde_entry.set_port(port)
		self.vrde = vrde_entry.output()

	def set_port_forwarding(self, guest_port, host_port):
		port_forwarding_entry = port_forwarding()
		port_forwarding_entry.set_guest_port(guest_port)
		port_forwarding_entry.set_host_port(host_port)
		self.port_forwarding = port_forwarding_entry.output()

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
		output = {'vm': {'name': self.name, 'node': self.node, 'provider': self.provider, 'os': self.os.output(),
		                 'network': self.network, 'vrde': self.vrde, 'port_forwarding': self.port_forwarding,
		                 'services': self.services}}
		return output

	def pp(self):
		print(self.node, \
		      self.hostname, \
		      self.provider, \
		      self.hostonly_network, \
		      self.hostonly_ip, \
		      self.internal_network, \
		      self.internal_ip, \
		      self.image, \
		      self.service, \
		      self.activity, \
		      self.vrdeport, \
		      self.guest_port_forward, \
		      self.host_port_forward)
