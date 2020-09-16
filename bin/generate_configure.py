import sys

sys.path.append('../')
from defaults import default
import configparser


def specification_generator(exp, lan, node, vm, filename=default.GENERATED_TEST_CONFIG_FILE):
	pass

def cfg_generator(sections_list, keys_list, values_list, filename=default.GENERATED_TEST_CONFIG_FILE):
	'''
	Take all cfg info like section, key & value in list type and generate the cfg file under config directory
	:param sections_list: section list (str)
	:param keys_list: keys list enclosing each key lists corresponding to its section list (str)
	:param values_list: values list enclosing each value lists corresponding to its key list (str)
	:param filename: cfg filename (str)
	:return:
	'''
	# values_list = list(map(str,values_list))
	config = configparser.ConfigParser()
	for section_index in range(0, len(sections_list)):
		config[sections_list[section_index]] = {}
		for index in range(0, len(keys_list[section_index])):
			config[sections_list[section_index]][keys_list[section_index][index]] = values_list[section_index][index]

	with open(filename, 'w') as config_file:
		config.write(config_file)
		print("save gen_configuration.cfg to %s" % (filename))


if __name__ == "__main__":
	sections = ['Experiment', 'LANs', 'LAN1', 'Nodes', 'Node1', 'Node2', 'VMs', 'VM1', 'VM2']
	keys = [['teamname', 'experimentname', 'lans_num', 'nodes_num', 'vms_num'], \
	        [], \
	        ['name', 'endpoints'], \
	        [], \
	        ['name', 'connectivity', 'lan', 'lan_node_ip', 'lan_netmask', 'host_network_name', 'host_network_ip',
	         'host_network_netmask'], \
	        ['name', 'connectivity', 'lan', 'lan_node_ip', 'lan_netmask', 'host_network_name', 'host_network_ip',
	         'host_network_netmask'], \
	        [], \
	        ['node', 'hostname', 'provider', 'network', 'ip', 'image', 'service', 'activity', 'vrdeport'], \
	        ['node', 'hostname', 'provider', 'network', 'ip', 'image', 'service', 'activity', 'vrdeport']]
	values = [['CS4238-19-01', 'Exp3', '1', '2', '2'], \
	          [], \
	          ['lan1', 'n1,n2'], \
	          [], \
	          ['n1', 'n2', 'lan1', '172.16.10.101', '255.255.255.0', 'vboxnet0,vboxnet1', '172.16.1.1,172.16.2.1',
	           '255.255.255.0,255.255.255.0'], \
	          ['n2', 'n1', 'lan1', '172.16.10.102', '255.255.255.0', 'vboxnet0', '172.16.1.1', '255.255.255.0'], \
	          [], \
	          ['n2', 'VM1', 'virtualbox', 'vboxnet0', '172.16.1.101', 'generic/ubuntu1910',
	           'essentials,python,php,django,attribution,blx,binspace,zara,klara', 'CVE-2013-2028', '12345'], \
	          ['n2', 'VM2', 'virtualbox', 'vboxnet0', '172.16.1.102', 'generic/ubuntu1910', 'flowsim', '12346']]

	cfg_generator(sections, keys, values)
