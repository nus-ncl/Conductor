import json

# all functions' parameters are string type
class Experiment:
	def __init__(self):
		self.teamname = ''
		self.experimentname = ''
		self.lans_num = 0
		self.nodes_num = 0
		self.vms_num = 0
		self.reserve_nodes = []

	# def __init__(self, teamname, experimentname, lans_num, nodes_num, vms_num, reserve_nodes):
	# 	self.teamname = teamname
	# 	self.experimentname = experimentname
	# 	self.lans_num = lans_num
	# 	self.nodes_num = nodes_num
	# 	self.vms_num = vms_num
	# 	self.reserve_nodes = reserve_nodes

	def set_teamname(self,teamname):
		self.teamname = teamname

	def set_experimentname(self,experimentname):
		self.experimentname = experimentname

	def set_lans_num(self,lans_num):
		self.lans_num = int(lans_num)

	def set_nodes_num(self,nodes_num):
		self.nodes_num = int(nodes_num)

	def set_vms_num(self,vms_num):
		self.vms_num = int(vms_num)

	def get_lans_num(self):
		return self.lans_num

	def get_nodes_num(self):
		return self.nodes_num

	def get_vms_num(self):
		return self.vms_num

	def pp(self):
		print(self.teamname,self.experimentname,self.lans_num,self.nodes_num,self.vms_num ,self.reserve_nodes)

	# def load(self, file):
	# 	''' load experiment from network definition json '''
	# 	print("Loading from " + file)
	# 	with open(file, 'r') as afile:
	# 		file_content = afile.read()
	# 	exp_conf = json.loads(file_content)
	#
	# 	# retrieve experiment level info: name, reserve_nodes...
	# 	if 'ExperimentDomainName' in exp_conf:
	# 		self.name = exp_conf['ExperimentDomainName']
	#
	# def show(self):
	# 	print("Experiment: %s" % self.name)
	# 	for node in self.nodes:
	# 		print('  Node: {}, OS: {}, IP Address: {}.'.format(node.name, node.OS, self.find_node_ip(node.name)))


class Lan:
	def __init__(self):
		self.name = ''
		self.endpoints = []

	# def __init__(self, name, endpoints):
	# 	self.name = name
	# 	self.endpoints = endpoints


	def set_name(self, name):
		self.name = name

	def set_endpoints(self, endpoints):
		self.endpoints = endpoints

	def pp(self):
		print(self.name,self.endpoints)

class Node:
	def __init__(self):
		self.name = ''
		self.OS = 'Ubuntu1604-64-STD'
		self.connectivity = None
		self.lan = []
		self.lan_node_ip = []
		self.lan_node_netmask = ('255.255.255.0,' * len(self.lan_node_ip)).split(',')[:-1]
		self.hostonly_network_name = []
		self.hostonly_network_ip = []
		self.hostonly_network_netmask = ('255.255.255.0,' * len(self.hostonly_network_ip)).split(',')[:-1]
		self.service = []

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

	def set_node_name(self,name):
		self.name = name

	def set_node_connectivity(self,connectivity):
		self.connectivity=connectivity

	def set_node_lan(self,lan):
		self.lan=lan.split(',')

	def set_node_lan_node_ip(self,node_ip):
		self.lan_node_ip=node_ip.split(',')

	def set_node_lan_node_netmask(self,node_netmask):
		self.lan_node_netmask=node_netmask.split(',')

	def set_node_host_network_name(self,name):
		self.hostonly_network_name=name.split(',')

	def set_node_host_network_ip(self,ip):
		self.hostonly_network_ip=ip.split(',')

	def set_node_host_network_netmask(self,netmask):
		self.hostonly_network_netmask=netmask.split(',')

	def set_node_service(self,service):
		self.service=service.split(',')

	def pp(self):
		print(self.name, \
		self.OS, \
		self.connectivity ,\
		self.lan ,\
		self.lan_node_ip ,\
		self.lan_node_netmask ,\
		self.hostonly_network_name ,\
		self.hostonly_network_ip ,\
		self.hostonly_network_netmask ,\
		self.service)


class VM:
	def __init__(self):
		self.node = ''
		self.hostname = ''
		self.provider = 'virtualbox/docker'
		self.hostonly_network = []
		self.hostonly_ip = []
		self.internal_network = None
		self.internal_ip = None
		self.image = 'generic/ubuntu1910'
		self.service = []
		self.activity = []
		self.vrdeport = ''
		self.guest_port_forward = []
		self.host_port_forward = []

	# def __init__(self, node, hostname, provider, hostonly_network, hostonly_ip, image, service, activity, vrdeport,
	#              guest_port_forward, host_port_forward):
	# 	self.node = node
	# 	self.hostname = hostname
	# 	self.provider = provider
	# 	self.hostonly_network = hostonly_network
	# 	self.hostonly_ip = hostonly_ip
	# 	self.internal_network = None
	# 	self.internal_ip = None
	# 	self.image = image
	# 	self.service = service
	# 	self.activity = activity
	# 	self.vrdeport = vrdeport
	# 	self.guest_port_forward = guest_port_forward
	# 	self.host_port_forward = host_port_forward

	def set_vm_node(self,node):
		self.node = node

	def set_vm_hostname(self,hostname):
		self.hostname = hostname

	def set_vm_provider(self,provider):
		self.provider = provider

	def set_vm_hostonly_network(self,network):
		self.hostonly_network=network.split(',')

	def set_vm_hostonly_ip(self,ip):
		self.hostonly_ip=ip.split(',')

	def set_vm_internal_network(self):
		pass

	def set_vm_internal_ip(self):
		pass

	def set_vm_image(self,image):
		self.image=image

	def set_vm_service(self,service):
		self.service=service.split(',')

	def set_vm_activity(self,activity):
		self.activity=activity.split(',')

	def set_vm_vrdeport(self,vrdeport):
		self.vrdeport=vrdeport

	def set_vm_guest_port_forward(self,guest_port_forward):
		self.guest_port_forward=guest_port_forward.split(',')

	def set_vm_host_port_forward(self,host_port_forward):
		self.host_port_forward=host_port_forward.split(',')

	def pp(self):
		print(self.node ,\
		self.hostname ,\
		self.provider,\
		self.hostonly_network ,\
		self.hostonly_ip ,\
		self.internal_network ,\
		self.internal_ip ,\
		self.image,\
		self.service,\
		self.activity ,\
		self.vrdeport ,\
		self.guest_port_forward ,\
		self.host_port_forward)


def main():
	ex1 = Experiment()
	ex1.load("../tests/netdef1.json")
	ex1.show()
	ex2 = Experiment()
	ex2.load("../tests/netdef2.json")
	ex2.show()


if __name__ == "__main__":
	main()
