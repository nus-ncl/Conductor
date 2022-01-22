import os
import requests
from shutil import copyfile
import jinja2
from jinja2 import Environment
from config import default

def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def renderer(output_dir, virtual_env, project_name, experiment_name, node_name):
    loader = jinja2.FileSystemLoader([default.TEMPLATE_PATH, default.SERVICE_PATH])
    with open(f"{output_dir}/playbook.yml", 'w') as file:
        # ansible file header '---'
        file.write("---\n")
        env = Environment(loader=loader)
        for vm in virtual_env['instance']:
            # For one vm entry:

            # First, ansiblefile_header.j2, with vm as input
            # ansiblefile_header.j2 will traverse vm['services'], all services for one vm, get all their parameters customized by users,
            # list then under 'vars:' or no parameter like 'vars: null'
            # so that the [service]_ansible.j2 under 'tasks' can
            # access their own service parameter directly by {{ [service]_[option] }}
            ansiblefile = env.get_template('ansiblefile_header.j2')
            content = ansiblefile.render(vm=vm)
            file.write(content)
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
            if vm['dependency']:
                for dependency in vm['dependency']:
                    ansiblefile = env.get_template(f"{dependency}/ansible/{dependency}.j2")
                    # if the dependency has parameter file [dependency].yml
                    if os.path.isfile(f"{default.SERVICE_PATH}/{dependency}/{dependency}.yml"):
                        copyfile(f"{default.SERVICE_PATH}/{dependency}/{dependency}.yml",
                                 f"{output_dir}/{vm['name']}_vars/{dependency}.yml")
                        content = ansiblefile.render(vars_file_path=f"/proj/{project_name}/{experiment_name}/{node_name}/{vm['name']}_vars")
                    # get ansible template file of specific service
                    # if 'parameter' in service:

                    # load specification(YAML-style) file of specific service the configuration/parameter/metadata yaml file of the service

                    # service_metadata = yaml_parser.yaml_file_load(
                    #     f"{root_path}/services/{service}/{service}.yml")

                    # the ansible file after rendering
                    else:
                        content = ansiblefile.render()
                    file.write(content)
                    file.write('\n\n')
            else:
                continue
            if vm['resource']:
                # conductor download resources to output_dir
                download_url(f"{vm['resource'][0]}",
                             f"{output_dir}/deploy.zip")
                # if os.path.isfile(f"{default.SERVICE_PATH}/{dependency}/{dependency}.yml"):
                #     copyfile(f"{default.SERVICE_PATH}/{dependency}/{dependency}.yml",
                #              f"{output_dir}/{vm['name']}_vars/{dependency}.yml")
                # and then complement the playbook with 'ansible.builtin.copy'
                ansiblefile = env.get_template(f"unarchive/ansible/unarchive.j2")
                # content = ansiblefile.render(unarchive_local_file_path=f"/proj/{project_name}/{experiment_name}/{node_name}/deploy.zip", unarchive_remote_directory_path='/tmp')
                content = ansiblefile.render(unarchive_local_file_path=f"/proj/{project_name}/{experiment_name}/{node_name}/deploy.zip", unarchive_remote_directory_path='"{{ ansible_facts[\'user_dir\'] }}/Desktop"')
                file.write(content)
            else:
                continue
    print('playbook done!')
