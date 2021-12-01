'''
input: activity.yml, specification.yml
output: ansible.yml
'''
import os
import yaml
import default
import jinja2
from jinja2 import Environment
import yaml_parser

dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(dir_path)


def ansiblefile_renderer(dir, activity, specification):
		templates_path = [f"{root_path}/templates", f"{root_path}/services"]
		loader = jinja2.FileSystemLoader(templates_path)
		activity_file = activity['file']
		with open(f"{root_path}/activity/{dir}/ansible.yml", 'w') as file:
				# ansible file header '---'
				file.write("---\n\n")
				env = Environment(loader=loader)
				last_activity_subject = ''
				for activity_entry in activity['activity']:
						# For one vm entry:
						if (activity_entry['subject'] is not None) and (activity_entry['subject'] != last_activity_subject):
								# First, ansiblefile_header.j2, with vm as input
								# ansiblefile_header.j2 will traverse vm['services'], all services for one vm, get all their parameters customized by users,
								# list then under 'vars:' or no parameter like 'vars: null'
								# so that the [service]_ansible.j2 under 'tasks' can
								# access their own service parameter directly by {{ [service]_[option] }}
								ansiblefile = env.get_template('ansiblefile_header.j2')
								content = ansiblefile.render(host=activity_entry)
								file.write(content)
								last_activity_subject = activity_entry['subject']

								# 	# Second, [service]_ansible.j2, with vm,service_yml_content as input
								# 	# For each service for one vm
								# 	# [service]_ansible.j2 will get this [service] configured
								# 	# It will access their own service users' parameter input via {{ [service]_[option] }} enclosed by {% raw %}-{% endraw %} block
								# 	# provided by ansiblefile_header.j2(if no parameter, no such reference)
								# 	# and
								# 	# use service['parameter']['service_option'] in jinja2 template
								# 	# and
								# 	# access their own service other configurations info by service_yml_content['*configuration_key*'], no need to enclose by {% raw %}-{% endraw %} blcok
								# 	# provided by [service].yml
								#
								if activity_entry['event']:
										for event_entry in activity_entry['event']:
												# get ansible template file of specific service
												# if 'parameter' in service:
												if '[' in event_entry.split(' ')[-1]:
														task = event_entry.split(' ')[0]
														service = event_entry.split(' ')[1]
														subtask = event_entry.split(' ')[2]
														parameter_list = event_entry.split(' ')[-1]
														ansiblefile = env.get_template(f"{service}/ansible/{task}.j2")
														# load specification(YAML-style) file of specific service
														# the configuration/parameter/metadata yaml file of the service
														service_metadata = yaml_parser.yaml_file_load(f"{root_path}/services/{service}/{service}.yml")
														# the ansible file after rendering
														content = ansiblefile.render(service=service, conductor_path=f"{root_path}",
														                             service_metadata=service_metadata, subtask=subtask,
														                             parameter_list=parameter_list, specification=specification,
														                             subject=activity_entry['subject'],activity_file=activity_file)
												else:
														service = event_entry.split(' ')[-1]
														task = event_entry.split(' ')[0]
														ansiblefile = env.get_template(f"{service}/ansible/{task}.j2")
														# load specification(YAML-style) file of specific service
														# the configuration/parameter/metadata yaml file of the service
														service_metadata = yaml_parser.yaml_file_load(f"{root_path}/services/{service}/{service}.yml")
														print(service_metadata)
														# the ansible file after rendering
														content = ansiblefile.render(service=service, conductor_path=f"{root_path}",
														                             service_metadata=service_metadata, specification=specification,
														                             subject=activity_entry['subject'],activity_file=activity_file)
												# content = ansiblefile.render(vm=vm, USER='{{ ansible_env.USER }}', conductor_path=ROOT_DIR, service=service)
												file.write(content)
												# file.write('\n\n')


def yaml_load_from_activity(dir):
		try:
				with open(f"{root_path}/activity/{dir}/activity.yml", 'r') as steam:
						return yaml.safe_load(steam)
		except OSError:
				print(f"No Such Activity Directory: {dir}")
				return {}


def yaml_load_from_specification(dir):
		try:
				with open(f"{root_path}/specification/{dir}/specification.yml", 'r') as steam:
						return yaml.safe_load(steam)
		except OSError:
				print(f"No Such Specification Directory: {dir}")
				return {}


def yaml_templatefile_load(filename):
		with open(f"{default.CONDUCTOR_PATH}/template/{filename}", 'r') as stream:
				return yaml.safe_load(stream)


if __name__ == '__main__':
		specification_output = {}

		activity_content = yaml_load_from_activity('apt32')
		specification_content = yaml_load_from_specification('apt32')
		# activity
		ansiblefile_renderer('apt32', activity_content, specification_content)
# activity
