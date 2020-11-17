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
'''
Output Desciplines:
For output for each component. 
	If the key's value's type is a string, None
	If the key's value's type is a num, 0
	If the key's value's type is a dict, {}
	directly output
	
	If the key's value's type is a list, []
		iterate to item.output()
	
'''


class metadata:
	def __init__(self, teamname=None, experimentname=None, lans_num=0, nodes_num=0, vms_num=0, reserved_nodes=None):
		self.teamname = teamname
		self.experimentname = experimentname
		self.lans_num = lans_num
		self.nodes_num = nodes_num
		self.vms_num = vms_num
		self.reserved_nodes = reserved_nodes

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
	def __init__(self, name=None, ip=None, netmask=None):
		self.name = name
		self.ip = ip
		self.netmask = netmask

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


class lan:
	def __init__(self, name=None, endpoints=None):
		self.name = name
		if endpoints is None:
			self.endpoints = []



	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_endpoints_dict_list(self, endpoint_dict_list):
		# endpoint_list is a list of endpoint dict, not endpoint object
		endpoints_list = []
		for endpoint_dict in endpoint_dict_list:
			endpoint_entry = endpoint()
			endpoint_entry.set_name(endpoint_dict['name'])
			endpoint_entry.set_ip(endpoint_dict['ip'])
			endpoint_entry.set_netmask(endpoint_dict['netmask'])
			endpoints_list.append(endpoint_entry)
		self.endpoints = endpoints_list

	def set_endpoints_object_list(self, endpoint_object_list):
		# endpoint_list is a list of endpoint object
		self.endpoints = endpoint_object_list

	def add_endpoints_object(self, endpoint_object):
		# endpoint_object is an endpoint object
		self.endpoints.append(endpoint_object)

	def add_endpoints_dict(self, endpoint_dict):
		# endpoints_dict is a endpoint dict
		endpoint_entry = endpoint()
		endpoint_entry.set_name(endpoint_dict['name'])
		endpoint_entry.set_ip(endpoint_dict['ip'])
		endpoint_entry.set_netmask(endpoint_dict['netmask'])
		self.endpoints.append(endpoint_entry)

	def add_endpoints(self, name, ip, netmask):
		# endpoint is a dictionary
		endpoint_entry = endpoint()
		endpoint_entry.set_name(name)
		endpoint_entry.set_ip(ip)
		endpoint_entry.set_netmask(netmask)
		self.endpoints.append(endpoint_entry)

	def output(self):
		endpoints_output = []
		for endpoint in self.endpoints:
			endpoints_output.append(endpoint.output())
		output = {'name': self.name, 'endpoints': endpoints_output}
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
	def __init__(self, name=None, ip=None, netmask=None):
		self.name = name
		self.ip = ip
		self.netmask = netmask

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
	def __init__(self, name=None, ip=None, netmask=None):
		self.name = name
		self.ip = ip
		self.netmask = netmask

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
	def __init__(self, hostonly_network=None, internal_network=None):
		if hostonly_network is None:
			self.hostonly_network = []
		if internal_network is None:
			self.internal_network = []

	# hostonly network
	def add_hostonly_network(self, name, ip, netmask):
		hostonly_network_entry = hostonly_network()
		hostonly_network_entry.set_name(name)
		hostonly_network_entry.set_ip(ip)
		hostonly_network_entry.set_netmask(netmask)
		self.hostonly_network.append(hostonly_network_entry)

	def add_hostonly_network_object(self, hostonly_network_object):
		# hostonly_network_list is a hostonly_network-type list
		self.hostonly_network.append(hostonly_network_object)

	def add_hostonly_network_dict(self, hostonly_network_dict):
		# hostonly_network_dict is a dict
		hostonly_network_entry = hostonly_network()
		hostonly_network_entry.set_name(hostonly_network_dict['name'])
		hostonly_network_entry.set_ip(hostonly_network_dict['ip'])
		hostonly_network_entry.set_netmask(hostonly_network_dict['netmask'])
		self.hostonly_network.append(hostonly_network_entry)

	def set_hostonly_network_dict_list(self, hostonly_network_dict_list):
		# hostonly_network_list is a hostonly_network dict list, not hostonly_network object list.
		hostonly_network_list = []
		for hostonly_network_dict in hostonly_network_dict_list:
			hostonly_network_entry = hostonly_network()
			hostonly_network_entry.set_name(hostonly_network_dict['name'])
			hostonly_network_entry.set_ip(hostonly_network_dict['ip'])
			hostonly_network_entry.set_netmask(hostonly_network_dict['netmask'])
			hostonly_network_list.append(hostonly_network_entry)
		self.hostonly_network = hostonly_network_list

	def set_hostonly_network_object_list(self, hostonly_network_object_list):
		# hostonly_network_list is a hostonly_network-type list
		self.hostonly_network = hostonly_network_object_list

	# internal network
	def add_internal_network(self, name, ip, netmask):
		internal_network_entry = hostonly_network()
		internal_network_entry.set_name(name)
		internal_network_entry.set_ip(ip)
		internal_network_entry.set_netmask(netmask)
		self.internal_network.append(internal_network_entry)

	def add_internal_network_object(self, internal_network_object):
		# internal_network is an object of class internal_network
		self.internal_network.append(internal_network_object)

	def add_internal_network_dict(self, internal_network_dict):
		# internal_network_dict is a dict
		internal_network_entry = internal_network()
		internal_network_entry.set_name(internal_network_dict['name'])
		internal_network_entry.set_ip(internal_network_dict['ip'])
		internal_network_entry.set_netmask(internal_network_dict['netmask'])
		self.internal_network.append(internal_network_entry)

	def set_internal_network_dict_list(self, internal_network_dict_list):
		# internal_network_list is a internal_network dict list not object list
		internal_network_list = []
		for internal_network_dict in internal_network_dict_list:
			internal_network_entry = internal_network()
			internal_network_entry.set_name(internal_network_dict['name'])
			internal_network_entry.set_ip(internal_network_dict['ip'])
			internal_network_entry.set_netmask(internal_network_dict['netmask'])
			internal_network_list.append(internal_network_entry)
		self.internal_network = internal_network_list

	def set_internal_network_object_list(self, internal_network_object_list):
		# internal_network_list is a internal_network-type list
		self.internal_network = internal_network_object_list

	def output(self):
		hostonly_network_output = []
		internal_network_output = []
		if self.hostonly_network is not None:
			for hostonly_network in self.hostonly_network:
				hostonly_network_output.append(hostonly_network.output())
		if self.internal_network is not None:
			for internal_network in self.internal_network:
				internal_network_output.append(internal_network.output())
		output = {'hostonly_network': hostonly_network_output, 'internal_network': internal_network_output}
		return output


class detailed_service:
	def __init__(self, service=None, parameter=None):
		self.service = service
		if parameter is None:
			self.parameter = {}

	def set_name(self, service):
		self.service = service

	def set_parameter(self, parameter):
		self.parameter = parameter

	def output(self):
		output = {'name': self.service, 'parameter': self.parameter}
		return output


# For docker
class networks:
	def __init__(self, name=None, driver=None, subnet=None, gateway=None):
		self.name = name
		self.driver = driver
		self.subnet = subnet
		self.gateway = gateway

	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_driver(self, driver):
		if driver == '':
			pass
		else:
			self.driver = driver

	def set_subnet(self, subnet):
		if subnet == '':
			pass
		else:
			self.subnet = subnet

	def set_gateway(self, gateway):
		if gateway == '':
			pass
		else:
			self.gateway = gateway


class node:
	def __init__(self, name=None, os_para=None, network=None , services=None):
		self.name = name
		if os_para is None:
			self.os = os()
		if network is None:
			self.network = node_network()
		if services is None:
			self.services = []

	def get_name(self):
		return self.name

	def set_name(self, name):
		if name == '':
			pass
		else:
			self.name = name

	def set_os_dict(self, os_dict):
		self.os.set_type(os_dict['type'])
		self.os.set_platform(os_dict['platform'])
		self.os.set_release(os_dict['release'])
		self.os.set_version(os_dict['version'])
		self.os.set_architecture(os_dict['architecture'])

	def set_network(self, network_dict):
		# Take format as reference
		# network_dict = {
		#                 "hostonly_network": [{"name": "vboxnet1", "ip": "172.16.1.1", "netmask": "255.255.255.0"},
		#                                      {"name": 'vboxnet2', "ip": "172.16.2.1", "netmask": "255.255.255.0"}],
		#                 "internal_network": [{"name": "vboxnet3", "ip": "172.16.3.1", "netmask": "255.255.255.0"},
		#                                      {"name": 'vboxnet4', "ip": "172.16.4.1", "netmask": "255.255.255.0"}]
		#                }
		self.network.set_hostonly_network_dict_list(network_dict['hostonly_network'])
		self.network.set_internal_network_dict_list(network_dict['internal_network'])

	def add_network(self, network_type, name, ip, netmask):
		if network_type == 'hostonly':
			self.network.add_hostonly_network(name, ip, netmask)
		elif network_type == 'internal':
			self.network.add_internal_network(name, ip, netmask)

	def get_services(self):
		# two formats
		# 1. services name list
		# 2. services dict(containing two keys: service & parameter) list
		return self.services

	def set_services_rough(self, service_list):
		# service_list is a service name list
		# service_list=['ansible','apt','build-essentials']
		#
		# services:
		#   - ansible
		#   - apt
		#   - build-essentials
		self.services = service_list

	def add_services_rough(self, service):
		# service is a service name
		self.services.append(service)

	# if self.services is None:
	# 	self.services = []
	# 	self.services.append(service)
	# else:
	# 	self.services.append(service)

	def set_services_detailed(self, service_dict_list):
		# service_list is a service dict list
		# service_list=[{'service':,'parameter':{}},{'service':,'parameter':{}}]
		#
		# services:
		#   - service: ansible
		#     parameter: null
		#   - service: nfs-server
		#     parameter:
		#       mount_src_directory: '/mnt/sda3/attribution'
		detailed_service_list = []
		for service_dict in service_dict_list:
			detailed_service_entry = detailed_service()
			# if dict is not empty
			if bool(service_dict):
				detailed_service_entry.set_name(service_dict['service'])
				detailed_service_entry.set_parameter(service_dict['parameter'])
			else:
				pass
			detailed_service_list.append(detailed_service_entry)
		self.services = detailed_service_list

	def add_services_detailed(self, service):
		# service is a detailed_service class
		self.services.append(service)

	# if self.services is None:
	# 	self.services = []
	# 	self.services.append(service)
	# else:
	# 	self.services.append(service)

	def output(self):
		if not self.services or type(self.services[0]).__name__ == 'str':
			output = {'name': self.name, 'os': self.os.output(), 'network': self.network.output(),
			          'services': self.services}
		else:
			services_output = []
			for service in self.services:
				services_output.append(service.output())
			output = {'name': self.name, 'os': self.os.output(), 'network': self.network.output(),
			          'services': services_output}
		return output


class vm_network:
	def __init__(self, gateway=None, ip=None, netmask=None, type=None):
		self.gateway = gateway
		self.ip = ip
		self.netmask = netmask
		self.type = type

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
		output = {'gateway': self.gateway, 'ip': self.ip, 'netmask': self.netmask, 'type': self.type}
		return output


class vrde:
	def __init__(self, enabled=False, port=None):
		self.enabled = enabled
		self.port = port

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
	def __init__(self, guest_port=None, host_port=None):
		self.guest_port = guest_port
		self.host_port = host_port

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


class vm:
	def __init__(self, name=None, node=None, provider=None, os_para=None, network=None, vrde_para=None,
	             port_forwarding_para=None, services=None):
		self.name = name
		self.node = node
		self.provider = provider
		if os_para is None:
			self.os = os()
		if network is None:
			self.network = []
		if vrde_para is None:
			self.vrde = vrde()
		if port_forwarding_para is None:
			self.port_forwarding = port_forwarding()
		if services is None:
			self.services = []

	def get_name(self):
		return self.name

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

	def set_os_dict(self, os_dict):
		self.os.set_type(os_dict['type'])
		self.os.set_platform(os_dict['platform'])
		self.os.set_release(os_dict['release'])
		self.os.set_version(os_dict['version'])
		self.os.set_architecture(os_dict['architecture'])

	def set_network_dict_list(self, network_dict_list):
		# Take format as reference
		# vm_networks_list = [
		# 	                  {"gateway": "vboxnet1", "ip": "172.16.1.1", "netmask": "255.255.255.0", "type": "hostonly"},
		#                     {"gateway": "vboxnet2", "ip": "172.16.2.1", "netmask": "255.255.255.0", "type": "hostonly"},
		#                     {"gateway": "vboxnet3", "ip": "172.16.3.1", "netmask": "255.255.255.0", "type": "internal"}
		#                    ]
		for network_dict in network_dict_list:
			vm_network_entry = vm_network()
			vm_network_entry.set_gateway(network_dict['gateway'])
			vm_network_entry.set_ip(network_dict['ip'])
			vm_network_entry.set_netmask(network_dict['netmask'])
			vm_network_entry.set_type(network_dict['type'])
			self.network.append(vm_network_entry)

	def add_network(self, gateway, ip, netmask, type):
		vm_network_entry = vm_network()
		vm_network_entry.set_gateway(gateway)
		vm_network_entry.set_ip(ip)
		vm_network_entry.set_netmask(netmask)
		vm_network_entry.set_type(type)
		# vm_network_entry = vm_network_entry.output()
		self.network.append(vm_network_entry)

	# if self.network is None:
	# 	self.network = []
	# 	self.network.append(vm_network_entry)
	# else:
	# 	self.network.append(vm_network_entry)

	def set_vrde_dict(self, vrde_dict):
		self.vrde.set_enabled(vrde_dict['enabled'])
		self.vrde.set_port(vrde_dict['port'])

	def modify_vrde(self, enabled, port):
		self.vrde.set_enabled(enabled)
		self.vrde.set_port(port)

	def set_port_forwarding_dict(self, port_forwarding_dict):
		self.port_forwarding.set_guest_port(port_forwarding_dict['guest_port'])
		self.port_forwarding.set_host_port(port_forwarding_dict['host_port'])

	def modify_port_forwarding(self, guest_port, host_port):
		self.port_forwarding.set_guest_port(guest_port)
		self.port_forwarding.set_host_port(host_port)

	def set_services_rough(self, service_list):
		# service_list is a service name list
		self.services = service_list

	def get_services(self):
		# two formats
		# 1. services name list
		# 2. services dict(containing two keys: service & parameter) list
		return self.services

	def add_services_rough(self, service):
		# service is a service name
		self.services.append(service)

	# if self.services is None:
	# 	self.services = []
	# 	self.services.append(service)
	# else:
	# 	self.services.append(service)

	def set_services_detailed(self, service_dict_list):
		# service_list is a service dict list
		# service_list=[{'service':,'parameter':{}},{'service':,'parameter':{}}]
		#
		# services:
		#   - service: ansible
		#     parameter: null
		#   - service: nfs-server
		#     parameter:
		#       mount_src_directory: '/mnt/sda3/attribution'
		detailed_service_list = []
		for service_dict in service_dict_list:
			detailed_service_entry = detailed_service()
			# if dict is not empty
			if bool(service_dict):
				detailed_service_entry.set_name(service_dict['service'])
				detailed_service_entry.set_parameter(service_dict['parameter'])
			else:
				pass
			detailed_service_list.append(detailed_service_entry)
		self.services = detailed_service_list

	def add_services_detailed(self, service):
		# service is a service class
		self.services.append(service)

	# if self.services is None:
	# 	self.services = []
	# 	self.services.append(service)
	# else:
	# 	self.services.append(service)

	def output(self):
		# print(len(self.network))
		network_output = []
		for network in self.network:
			network_output.append(network.output())

		if not self.services or type(self.services[0]).__name__ == 'str':
			output = {'name': self.name, 'node': self.node, 'provider': self.provider, 'os': self.os.output(),
			          'network': network_output, 'vrde': self.vrde.output(),
			          'port_forwarding': self.port_forwarding.output(),
			          'services': self.services}
		else:
			services_output = []
			for service in self.services:
				services_output.append(service.output())

			output = {'name': self.name, 'node': self.node, 'provider': self.provider, 'os': self.os.output(),
			          'network': network_output, 'vrde': self.vrde.output(),
			          'port_forwarding': self.port_forwarding.output(),
			          'services': services_output}
		return output
