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

# TODO: output for node
def vagrantfile_renderer(vms):
		file = open(default.VAGRANT_FILE, 'w')
		env = Environment(loader=PackageLoader('templates'))
		Vagrantfile = env.get_template('Vagrantfile.j2')
		content = Vagrantfile.render(vms=vms)
		file.write(content)
		file.close()

# TODO: output for node
def hosts_renderer(vms):
		file = open(default.HOSTS_FILE, 'w')
		env = Environment(loader=PackageLoader('templates'))
		hostsfile = env.get_template('hosts.j2')
		content = hostsfile.render(vms=vms)
		file.write(content)
		file.close()


# def ansiblefile_header_renderer(vm):
# 		file = open(default.ANSIBLE_FILE, 'w')
# 		env = Environment(loader=PackageLoader('templates'))
# 		ansiblefile = env.get_template('ansiblefile_header.j2')
# 		content = ansiblefile.render(vm=vm)
# 		file.write(content)
# 		# file.write('\n')
# 		file.close()

# TODO: output for node
def ansiblefile_renderer(vms):
		# dir = os.path.dirname(__file__)
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
						content = ansiblefile.render(vm=vm, USER='{{ ansible_env.USER }}',item='{{ item }}')
						# content = ansiblefile.render(path=dir + '/../services/' + service)
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

# TODO: output for node
def Clientfile_renderer(hostname):
		file = open(default.CLIENT_FILE, 'w')
		env = Environment(loader=PackageLoader('templates'))
		Clientfile = env.get_template('Client.j2')
		content = Clientfile.render(hostname=hostname)
		file.write(content)
		file.close()


if __name__ == "__main__":
		PRINT = 0
		NSFILE = 1
		HOSTS = 1
		VAGRANTFILE = 1
		ANSIBLEFILE = 1
		CLIENTFILE = 0

		conf = configparser.ConfigParser()
		conf.read(default.CONFIG_FILE)
		nodes_num = conf.get("Experiment", "nodes_num")
		lans_num = conf.get("Experiment", "lans_num")
		vms_num = conf.get("Experiment", "vms_num")

		# print configure.cfg
		if (PRINT):
				print_configure_file(default.CONFIG_FILE)

		# generate NSfile
		if (NSFILE):
				nodes = []
				for i in range(1, int(nodes_num) + 1):
						node_index = 'Node' + str(i)
						node_name = conf.get(node_index, "name")
						node_connectivity = conf.get(node_index, "connectivity")
						node_lan = conf.get(node_index, "lan")
						node_lan_node_ip = conf.get(node_index, "lan_node_ip")
						node_entry = {'name': node_name, 'connectivity': node_connectivity, 'lan': node_lan,
						              'lan_node_ip': node_lan_node_ip, }
						nodes.append(node_entry)

				lans = []
				for i in range(1, int(lans_num) + 1):
						lan_index = 'LAN' + str(i)
						lan_name = conf.get(lan_index, "name")
						lan_endpoints = conf.get(lan_index, "endpoints")
						lan_endpoints_list = lan_endpoints.split(',')
						lan_entry = {'name': lan_name, 'endpoints': lan_endpoints_list}
						lans.append(lan_entry)

				NSfile_renderer(nodes, lans)

		# generate hosts file
		if (HOSTS):
				vms = []
				for i in range(1, int(vms_num) + 1):
						node_index = 'VM' + str(i)
						vm_node = conf.get(node_index, "node")
						vm_hostname = conf.get(node_index, "hostname")
						vm_provider = conf.get(node_index, "provider")
						vm_network = conf.get(node_index, "network")
						vm_network_list = vm_network.split(',')
						vm_ip = conf.get(node_index, "ip")
						vm_ip_list = vm_ip.split(',')
						vm_image = conf.get(node_index, "image")
						vm_service = conf.get(node_index, "service")
						vm_service_list = vm_service.split(',')
						vm_activity = conf.get(node_index, "activity")
						vm_activity_list = vm_activity.split(',')

						vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
						            'network': vm_network_list, 'ip': vm_ip_list, 'image': vm_image,
						            'service': vm_service_list, 'activity': vm_activity_list}
						vms.append(vm_entry)
				# print(vms)
				vagrantfile_renderer(vms)
				hosts_renderer(vms)

		# generate vagrantfile
		if (VAGRANTFILE):
				vms = []
				for i in range(1, int(vms_num) + 1):
						node_index = 'VM' + str(i)
						vm_node = conf.get(node_index, "node")
						vm_hostname = conf.get(node_index, "hostname")
						vm_provider = conf.get(node_index, "provider")
						vm_network = conf.get(node_index, "network")
						vm_network_list = vm_network.split(',')
						vm_ip = conf.get(node_index, "ip")
						vm_ip_list = vm_ip.split(',')
						vm_image = conf.get(node_index, "image")
						vm_service = conf.get(node_index, "service")
						vm_service_list = vm_service.split(',')
						vm_activity = conf.get(node_index, "activity")
						vm_activity_list = vm_activity.split(',')

						vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
						            'network': vm_network_list, 'ip': vm_ip_list, 'image': vm_image,
						            'service': vm_service_list, 'activity': vm_activity_list}
						vms.append(vm_entry)
				# print(vms)
				vagrantfile_renderer(vms)

		# generate ansible file
		if (ANSIBLEFILE):
				vms = []
				for i in range(1, int(vms_num) + 1):
						node_index = 'VM' + str(i)
						vm_node = conf.get(node_index, "node")
						vm_hostname = conf.get(node_index, "hostname")
						vm_provider = conf.get(node_index, "provider")
						vm_network = conf.get(node_index, "network")
						vm_network_list = vm_network.split(',')
						vm_ip = conf.get(node_index, "ip")
						vm_ip_list = vm_ip.split(',')
						vm_image = conf.get(node_index, "image")
						vm_service = conf.get(node_index, "service")
						vm_service_list = vm_service.split(',')
						vm_activity = conf.get(node_index, "activity")
						vm_activity_list = vm_activity.split(',')

						vm_entry = {'node': vm_node, 'hostname': vm_hostname, 'provider': vm_provider,
						              'network': vm_network_list, 'ip': vm_ip_list, 'image': vm_image,
												'service': vm_service_list,'activity': vm_activity_list}
						vms.append(vm_entry)
				# print(vms)
				ansiblefile_renderer(vms)

		# generate clientfile
		if (CLIENTFILE):
				Clientfile_renderer(hostname)
