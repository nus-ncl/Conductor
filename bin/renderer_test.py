import yaml
import jinja2
from jinja2 import Environment, PackageLoader
from defaults import default

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
	template_dir = [f"{default.conductor_path}/templates",f"{default.conductor_path}/services"]
	loader = jinja2.FileSystemLoader(template_dir)
	with open(default.ANSIBLE_TEST_FILE, 'w') as file:
		# ansible file header '---'
		file.write("---\n\n")
		env = Environment(loader=loader)
		for vm in vms:
			ansiblefile = env.get_template('ansiblefile_header.j2')
			content = ansiblefile.render(vm=vm)
			file.write(content)
			if vm['services'] is not None:
				for service in vm['services']:
					# get ansible template file of specific service
					ansiblefile = env.get_template(f"{service['service']}/{service['service']}.j2")
					# load specification(YAML-style) file of specific service
					with open(f"{default.conductor_path}/services/{service['service']}/{service['service']}.yml", 'r') as stream:
						service = yaml.safe_load(stream)
					# print('service->')
					# print(service)
					# the ansible file after rendering
					content = ansiblefile.render(vm=vm, conductor_path=ROOT_DIR, service=service)
					# content = ansiblefile.render(vm=vm, USER='{{ ansible_env.USER }}', conductor_path=ROOT_DIR, service=service)
					file.write(content)
					file.write('\n\n')

def NSfile_renderer(lans,nodes):
	template_dir = [f"{default.conductor_path}/templates"]
	loader = jinja2.FileSystemLoader(template_dir)
	with open(default.NS_TEST_FILE, 'w') as file:
		env = Environment(loader=loader)
		NSfile = env.get_template('NSfile.j2')
		content = NSfile.render(lans=lans,nodes=nodes)
		file.write(content)

# TODO: specify pack version and 'route add -net' & 'hostonlyif'
def nodesfile_renderer(nodes):
	template_dir = [f"{default.conductor_path}/templates",f"{default.conductor_path}/services"]
	loader = jinja2.FileSystemLoader(template_dir)
	env = Environment(loader=loader)
	nodefile = env.get_template('node.j2')
	for node in nodes:
		node_filename = default.NODES_TEST_PATH + node['name'] + '.sh'
		with open(node_filename, 'w') as file:
			content = nodefile.render(node=node)
			file.write(content)

def clientfile_renderer(experiment_metadata, vms):
	with open(default.CLIENT_TEST_FILE, 'w') as file:
		env = Environment(loader=PackageLoader('templates'))
		Clientfile = env.get_template('Client.j2')
		content = Clientfile.render(experiment_metadata=experiment_metadata, vms=vms)
		file.write(content)

def dockerfile_renderer(vms):
	with open(default.DOCKER_TEST_FILE, 'w') as file:
		env = Environment(loader=PackageLoader('templates'))
		Dockerfile = env.get_template('Dockerfile.j2')
		content = Dockerfile.render(vms=vms)
		file.write(content)

if __name__ == "__main__":
	pass