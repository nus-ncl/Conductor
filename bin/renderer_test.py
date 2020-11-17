import sys
import copy
sys.path.append('../defaults')
import yaml
import jinja2
from jinja2 import Environment, PackageLoader
import default
import yaml_parser
import pathlib


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
	ROOT_DIR = default.conductor_path
	template_dir = [f"{default.conductor_path}/templates", f"{default.conductor_path}/services"]
	loader = jinja2.FileSystemLoader(template_dir)
	with open(default.ANSIBLE_TEST_FILE, 'w') as file:
		# ansible file header '---'
		file.write("---\n\n")
		env = Environment(loader=loader)
		for vm in vms:
			ansiblefile = env.get_template('ansiblefile_header.j2')
			content = ansiblefile.render(vm=vm)
			file.write(content)
			if vm['services']:
				for service in vm['services']:
					# get ansible template file of specific service
					if 'Error' not in service['parameter']:
						ansiblefile = env.get_template(f"{service['name']}/{service['name']}_ansible.j2")
						# load specification(YAML-style) file of specific service
						with open(f"{default.conductor_path}/services/{service['name']}/{service['name']}.yml",
						          'r') as stream:
							service = yaml.safe_load(stream)
						# print('service->')
						# print(service)
						# the ansible file after rendering
						content = ansiblefile.render(vm=vm, conductor_path=ROOT_DIR, service=service)
						# content = ansiblefile.render(vm=vm, USER='{{ ansible_env.USER }}', conductor_path=ROOT_DIR, service=service)
						file.write(content)
						file.write('\n\n')


def NSfile_renderer(lans, nodes):
	template_dir = [f"{default.conductor_path}/templates"]
	loader = jinja2.FileSystemLoader(template_dir)
	with open(default.NS_TEST_FILE, 'w') as file:
		env = Environment(loader=loader)
		NSfile = env.get_template('NSfile.j2')
		content = NSfile.render(lans=lans, nodes=nodes)
		file.write(content)


# TODO: specify pack version and 'route add -net' & 'hostonlyif'
def nodesfile_renderer(nodes,node_virtualbox_version):
	template_dir = [f"{default.conductor_path}/templates", f"{default.conductor_path}/services"]
	loader = jinja2.FileSystemLoader(template_dir)
	env = Environment(loader=loader)
	nodefile = env.get_template('node.j2')
	for node in nodes:
		node_filename = default.NODES_TEST_PATH + node['name'] + '.sh'
		with open(node_filename, 'w') as file:
			content = nodefile.render(node=node,node_virtualbox_version=node_virtualbox_version)
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
	# print(yaml_content)
	vms, lans, nodes, docker_networks = yaml_parser.yaml_content_parser(yaml_content)
	if default.debug:
		# print('nodes->')
		# print(nodes)
		# print('lans->')
		# print(lans)
		# print('docker_networks->')
		# print(docker_networks)
		# print('vms->')
		# print(vms)
	# vagrantfile_renderer(vms)
	# hosts_renderer(vms)
	# nodesfile_renderer(nodes,default.NODE_VIRTUALBOX_VERSION)
	# NSfile_renderer(lans, nodes)
	# ansiblefile_renderer(vms)
		dockerfile_renderer(vms)
