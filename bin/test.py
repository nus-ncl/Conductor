import yaml_parser
import cli
from defaults import default


class a:
	def output(self):
		return 'this is a'

class b:
	def output(self):
		return 'this is b'

class metadata:
	# def __init__(self):
	# 	self.teamname = None
	# 	self.experimentname = None
	# 	self.lans_num = 0
	# 	self.nodes_num = 0
	# 	self.vms_num = 0
	# 	self.reserved_nodes = None

	def __init__(self, teamname=None, experimentname=None, lans_num=0, nodes_num=0, vms_num=0, reserved_nodes=None):
		self.teamname = teamname
		self.experimentname = experimentname
		self.lans_num = lans_num
		self.nodes_num = nodes_num
		self.vms_num = vms_num
		self.reserved_nodes = reserved_nodes

node = {'name': None,
               'os': {'type': 'node', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04',
                      'architecture': 'amd64'},
               'network': {'hostonly_network': [{'name': 'vboxnet1', 'ip': '172.16.1.2', 'netmask': '255.255.255.0'}],
                           'internal_network': [{'name': 'vboxnet2', 'ip': '172.16.2.2', 'netmask': '255.255.255.0'}]},
               'services': ['nginx', 'nfs-client']}

if __name__ == '__main__':
	# yaml_parser.yaml_file_dump(node, 'output')
	a = metadata()
	print(a.reserved_nodes)
	print(a.vms_num)
	print(a.lans_num)