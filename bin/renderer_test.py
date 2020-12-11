import sys
import copy
sys.path.append('../defaults')
import yaml
import jinja2
from jinja2 import Environment, PackageLoader
import default
import yaml_parser

def vagrantfile_renderer(vms):
	template_dir = [f"{default.conductor_path}/templates"]
	loader = jinja2.FileSystemLoader(template_dir)
	with open(default.VAGRANT_TEST_FILE, 'w') as file:
		env = Environment(loader=loader)
		Vagrantfile = env.get_template('Vagrantfile.j2')
		content = Vagrantfile.render(vms=vms)
		file.write(content)


def hosts_renderer(vms):
	template_dir = [f"{default.conductor_path}/templates"]
	loader = jinja2.FileSystemLoader(template_dir)
	with open(default.HOSTS_TEST_FILE, 'w') as file:
		env = Environment(loader=loader)
		hostsfile = env.get_template('hosts.j2')
		content = hostsfile.render(vms=vms)
		file.write(content)


def ansiblefile_renderer(vms):
	#
	# For ansible
	# Output: ansible.yml, like:

	# - hosts: VM1
	# gather_facts: true
	# vars:
	#   nginx_version: 1.4.0
	#   nginx_port: 81
	# tasks:
	#
	# - hosts: VM2
	# gather_facts: true
	# vars: null
	# tasks:

	# which consists of many entries of ansiblefile_header.j2 & [service]_ansible.j2

	ROOT_DIR = default.conductor_path
	template_dir = [f"{default.conductor_path}/templates", f"{default.conductor_path}/services"]
	loader = jinja2.FileSystemLoader(template_dir)
	with open(default.ANSIBLE_TEST_FILE, 'w') as file:
		# ansible file header '---'
		file.write("---\n\n")
		env = Environment(loader=loader)
		# For one vm entry:
		for vm in vms:
			# First, ansiblefile_header.j2, with vm as input
			# ansiblefile_header.j2 will traverse vm['services'], all services for one vm, get all their parameters customized by users,
			# list then under 'vars:' or no parameter like 'vars: null'
			# so that the [service]_ansible.j2 under 'tasks' can
			# access their own service parameter directly by {{ [service]_[option] }}
			ansiblefile = env.get_template('ansiblefile_header.j2')
			content = ansiblefile.render(vm=vm)
			file.write(content)
			if vm['services']:
				# Second, [service]_ansible.j2, with vm,service_yml_content as input
				# For each service for one vm
				# [service]_ansible.j2 will get this [service] configured
				# It will access their own service users' parameter input via {{ [service]_[option] }} enclosed by {% raw %}-{% endraw %} block
				# provided by ansiblefile_header.j2(if no parameter, no such reference)
				# and
				# use service['parameter']['service_option'] in jinja2 template
				# and
				# access their own service other configurations info by service_yml_content['*configuration_key*'], no need to enclose by {% raw %}-{% endraw %} blcok
				# provided by [service].yml

				for service in vm['services']:
					# get ansible template file of specific service
					# if 'parameter' in service:
					ansiblefile = env.get_template(f"{service['name']}/{service['name']}_ansible.j2")
					# load specification(YAML-style) file of specific service
					service_yml_content = yaml_parser.yaml_service_load(service['name'])
					# print('service->')
					# print(service)
					# the ansible file after rendering
					content = ansiblefile.render(service=service, conductor_path=ROOT_DIR, service_yml_content=service_yml_content)
					# content = ansiblefile.render(vm=vm, USER='{{ ansible_env.USER }}', conductor_path=ROOT_DIR, service=service)
					file.write(content)
					file.write('\n\n')


def NSfile_renderer(lans, nodes, metadata):
	template_dir = [f"{default.conductor_path}/templates"]
	loader = jinja2.FileSystemLoader(template_dir)
	with open(default.NS_TEST_FILE, 'w') as file:
		env = Environment(loader=loader)
		NSfile = env.get_template('NSfile.j2')
		content = NSfile.render(lans=lans, nodes=nodes, metadata=metadata)
		file.write(content)


# TODO: specify pack version and 'route add -net' & 'hostonlyif'
def nodesfile_renderer(nodes,node_virtualbox_version):
	# For nodefile
	# Output: n1.sh(n2.sh...)
	# which consists of many entries of the rendered result of [service]_ansible.j2

	template_dir = [f"{default.conductor_path}/templates", f"{default.conductor_path}/services"]
	loader = jinja2.FileSystemLoader(template_dir)
	env = Environment(loader=loader)
	# node.j2 with node, yaml_service_load(which is a function) as inputs
	# First, it will complete pre-defined common tasks
		# virtualbox extpack
		# ssh key
		# Create Host Adapter for VMs
	# Second, it will traverse all services, node['services'], for one node
	# node.j2 incorporates all rendered result of [service]_node.j2
	# it uses with-include block
	# for service that has parameter, with parameter=service['parameter'] & service_yml_content = yaml_service_load(service['name'])
	# (MUST pass into parameter=service['parameter' instead of service_yml_content['parameter'], cuz the previous is customized by user)
	# for service that doesn't have parameter, with service_yml_content = yaml_service_load(service['name'])

	nodefile = env.get_template('node.j2')
	for node in nodes:
		node_filename = default.NODES_TEST_PATH + node['name'] + '.sh'
		with open(node_filename, 'w') as file:
			content = nodefile.render(node=node,node_virtualbox_version=node_virtualbox_version,yaml_service_load=yaml_parser.yaml_service_load)
			file.write(content)

def vm_configure_renderer(vms):
	template_dir = [f"{default.conductor_path}/templates"]
	loader = jinja2.FileSystemLoader(template_dir)
	env = Environment(loader=loader)
	vm_configure = env.get_template('vm_configure.j2')
	for vm in vms:
		vm_filename = default.VM_CONFIGURE_TEST_PATH + vm['hostname'] + '.conf.sh'
		with open(vm_filename, 'w') as file:
			content = vm_configure.render(vm=vm)
			file.write(content)


def clientfile_renderer(experiment_metadata, vms):
	with open(default.CLIENT_TEST_FILE, 'w') as file:
		env = Environment(loader=PackageLoader('templates'))
		Clientfile = env.get_template('Client.j2')
		content = Clientfile.render(experiment_metadata=experiment_metadata, vms=vms)
		file.write(content)


def dockerfile_renderer(vms):
	header=0
	services={}
	ROOT_DIR = default.conductor_path
	template_dir = [f"{default.conductor_path}/templates", f"{default.conductor_path}/services"]
	loader = jinja2.FileSystemLoader(template_dir)
	env = Environment(loader=loader)
	# output Dockerfile
	for vm in vms:
		if vm['provider'] == 'docker':
			if vm['services'] and vm['os']:
				if not header:
					try:
						with open(default.DOCKERCOMPOSE_TEST_FILE, 'w') as file:
							file.write("version: '3.8'\nservices:\n")
					except OSError:
						print(f"{default.DOCKERCOMPOSE_TEST_FILE} open failure")
					header=1
				# one docker one service, so here specify vm['services'][0], cuz vm['services'] is 1-element list
				with open(f"{default.DOCKERFILE_TEST_FILE}_{vm['hostname']}_{vm['services'][0]['name']}", 'w') as file:
					# get docker template file of specific service
					dockerfile = env.get_template(f"{vm['services'][0]['name']}/{vm['services'][0]['name']}_docker.j2")
					# load specification(YAML-style) file of specific service
					try:
						with open(f"{default.conductor_path}/services/{vm['services'][0]['name']}/{vm['services'][0]['name']}.yml", 'r') as stream:
							service = yaml.safe_load(stream)
							services[f"{vm['services'][0]['name']}"]=copy.deepcopy(service)
						# print('service->')
						# print(service)
						content = dockerfile.render(vm=vm, service=service)
						# content = ansiblefile.render(vm=vm, USER='{{ ansible_env.USER }}', conductor_path=ROOT_DIR, service=service)
						file.write(content)
						print(f"{default.DOCKERFILE_TEST_FILE}_{vm['hostname']}_{vm['services'][0]['name']} is generated!")
					except OSError:
						print('No Such Service for Docker')

					# print('services->')
					# print(services)
					# print(vm['services'][0]['name'])
					# print(vm['hostname'])
					# output docker-compose.yml
					try:
						with open(default.DOCKERCOMPOSE_TEST_FILE, 'a') as file:
							docker_compose_file = env.get_template('docker-compose.j2')
							content = docker_compose_file.render(vm=vm, services=services, conductor_path=ROOT_DIR)
							file.write(content)
							print(f"{default.DOCKERCOMPOSE_TEST_FILE} is updated! ")
					except OSError:
						print(f"{default.DOCKERCOMPOSE_TEST_FILE} open error")
			else:
				print('No Any Service or OS to generate This Dockerfile of a container!')
		else:
			# This is no docker
			pass

if __name__ == "__main__":
	yaml_content = yaml_parser.yaml_file_load('output')
	# json_content = yaml_parser.yaml_file_load('output')
	print(yaml_content)
	yaml_parser.yaml_file_dump(yaml_content,'hkwany')

	metadata, vms, lans, nodes, docker_networks = yaml_parser.yaml_content_parser(yaml_content)
	if default.debug:
		pass
		# print('metadata->')
		# print(metadata)
		# print('nodes->')
		# print(nodes)
		# print('lans->')
		# print(lans)
		# print('docker_networks->')
		# print(docker_networks)
		# print('vms->')
		# print(vms)
		# vm_configure_renderer(vms)
		# vagrantfile_renderer(vms)
		# hosts_renderer(vms)
		# nodesfile_renderer(nodes,default.NODE_VIRTUALBOX_VERSION)
		# NSfile_renderer(lans, nodes, metadata)
		# ansiblefile_renderer(vms)
		# dockerfile_renderer(vms)
