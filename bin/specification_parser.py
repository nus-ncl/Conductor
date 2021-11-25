'''
input: specification.yml
output: various configuration files
'''

import os
import copy
import yaml
import jinja2
from jinja2 import Environment, PackageLoader
import default
import yaml_parser
import operating_system

dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(dir_path)
templates_path = f"{root_path}/templates"
specification_path = f"{root_path}/specification"
outputs_path = f"{root_path}/outputs"

def os_parser(vm):
	provider = vm['provider']
	platform = vm['os']['platform']
	release = vm['os']['release']
	version = vm['os']['version']
	bit = vm['os']['bit']
	return operating_system.os[provider][platform][release][version][bit]

def vagrantfile_renderer(vms):
	loader = jinja2.FileSystemLoader(templates_path)
	with open(f"{outputs_path}/Vagrantfile", 'w') as file:
		env = Environment(loader=loader)
		Vagrantfile = env.get_template('Vagrantfile.j2')
		content = Vagrantfile.render(vms=vms, os_parser=os_parser)
		file.write(content)

def hosts_renderer(vms):
	loader = jinja2.FileSystemLoader(templates_path)
	with open(f"{outputs_path}/hosts", 'w') as file:
		env = Environment(loader=loader)
		hostsfile = env.get_template('hosts.j2')
		content = hostsfile.render(vms=vms)
		file.write(content)

def NSfile_renderer(lans, metadata, nodes):
	loader = jinja2.FileSystemLoader(templates_path)
	with open(f"{outputs_path}/NSfile", 'w') as file:
		env = Environment(loader=loader)
		NSfile = env.get_template('NSfile.j2')
		content = NSfile.render(lans=lans,metadata=metadata,nodes=nodes)
		file.write(content)


# TODO: specify pack version and 'route add -net' & 'hostonlyif'
def nodesfile_renderer(nodes,node_virtualbox_version):
	# For nodefile
	# Output: n1.sh(n2.sh...)
	# which consists of many entries of the rendered result of [service]_ansible.j2

	templates_path = [f"{default.CONDUCTOR_PATH}/templates", f"{default.CONDUCTOR_PATH}/services"]
	loader = jinja2.FileSystemLoader(templates_path)
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
	templates_path = [f"{default.CONDUCTOR_PATH}/templates"]
	loader = jinja2.FileSystemLoader(templates_path)
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
	ROOT_DIR = default.CONDUCTOR_PATH
	templates_path = [f"{default.CONDUCTOR_PATH}/templates", f"{default.CONDUCTOR_PATH}/services"]
	loader = jinja2.FileSystemLoader(templates_path)
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
						with open(f"{default.CONDUCTOR_PATH}/services/{vm['services'][0]['name']}/{vm['services'][0]['name']}.yml", 'r') as stream:
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
	specification_content = yaml_parser.yaml_file_load(f"{specification_path}/apt32_specification_complicated.yml")
	# print(specification_content)
	# vagrantfile_renderer(specification_content['vm'])
	# hosts_renderer(specification_content['vm'])
	NSfile_renderer(specification_content['lan'], specification_content['metadata'],specification_content['node'])


	# yaml_parser.yaml_file_dump(yaml_content,'hkwany')
	# metadata, vms, lans, nodes, docker_networks = yaml_parser.yaml_content_parser(yaml_content)
	# if default.debug:
	# 	pass
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
