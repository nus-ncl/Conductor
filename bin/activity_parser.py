'''
input: activity.yml
output: ansible.yml
'''
import os
import yaml
import default
import jinja2
from jinja2 import Environment, PackageLoader

dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(dir_path)
activity_path = f"{root_path}/activity"

def ansiblefile_renderer(vms):
	templates_path = [f"{root_path}/templates", f"{root_path}/services"]
	loader = jinja2.FileSystemLoader(templates_path)
	with open(f"{root_path}/outputs/ansible.yml", 'w') as file:
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


def yaml_load_from_activity(filename):
	try:
		with open(f"{root_path}/screenplay/{filename}", 'r') as steam:
			return yaml.safe_load(steam)
	except OSError:
		print(f"No Such Screenplay File: {filename}")
		return {}


def yaml_templatefile_load(filename):
	with open(f"{default.CONDUCTOR_PATH}/template/{filename}", 'r') as stream:
		return yaml.safe_load(stream)


if __name__ == '__main__':
	specification_output = {}

	screenplay_content = yaml_load_from_screenplay('apt32_screenplay_complicated.yml')

	# activity
	yaml_dump_to_activity(screenplay_content)
	# activity

