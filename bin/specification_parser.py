'''
input: specification.yml
output: various configuration files
'''
import sys
import os
import copy
import yaml
import jinja2
from jinja2 import Environment, PackageLoader
from .yaml_utility import yaml_parser
import operating_system
from config import default
sys.path.append('./bin/renderer')
# from renderer import *
import NSfile_renderer, Vagrantfile_renderer, hosts_renderer, deter_exp_bootstrap, deter_node_bootstrap, ansible_playbook_renderer, node_script_renderer


def os_parser(vm):
    provider = vm['provider']
    platform = vm['os']['platform']
    release = vm['os']['release']
    version = vm['os']['version']
    bit = vm['os']['bit']
    return operating_system.os[provider][platform][release][version][bit]



# TODO: specify pack version and 'route add -net' & 'hostonlyif'
def nodesfile_renderer(nodes, node_virtualbox_version):
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
            content = nodefile.render(node=node, node_virtualbox_version=node_virtualbox_version,
                                      yaml_service_load=yaml_parser.yaml_service_load)
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
    header = 0
    services = {}
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
                    header = 1
                # one docker one service, so here specify vm['services'][0], cuz vm['services'] is 1-element list
                with open(f"{default.DOCKERFILE_TEST_FILE}_{vm['hostname']}_{vm['services'][0]['name']}", 'w') as file:
                    # get docker template file of specific service
                    dockerfile = env.get_template(f"{vm['services'][0]['name']}/{vm['services'][0]['name']}_docker.j2")
                    # load specification(YAML-style) file of specific service
                    try:
                        with open(
                                f"{default.CONDUCTOR_PATH}/services/{vm['services'][0]['name']}/{vm['services'][0]['name']}.yml",
                                'r') as stream:
                            service = yaml.safe_load(stream)
                            services[f"{vm['services'][0]['name']}"] = copy.deepcopy(service)
                        # print('service->')
                        # print(service)
                        content = dockerfile.render(vm=vm, service=service)
                        # content = ansiblefile.render(vm=vm, USER='{{ ansible_env.USER }}', conductor_path=ROOT_DIR, service=service)
                        file.write(content)
                        print(
                            f"{default.DOCKERFILE_TEST_FILE}_{vm['hostname']}_{vm['services'][0]['name']} is generated!")
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


def parser(path_to_file):
    # filename = os.path.basename(path_to_file).split('.')[0]
    content = yaml_parser.yaml_file_load(path_to_file)
    platform = yaml_parser.get_platform(content)
    project_name = yaml_parser.get_project_name(content)
    print(project_name)
    print(f"Platform is {platform}")
    output_dir = f"{default.OUTPUT_PATH}/{project_name}"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    else:
        print(f"{output_dir} already exists!")

    print(f"Starting")
    if platform == 'deter':
        # experiment_number = yaml_parser.get_instance_number(content)
        experiments_list = yaml_parser.get_instance_list(content)
        for index, experiment in enumerate(experiments_list):
            if not os.path.isdir(f"{output_dir}/{experiment['name']}"):
                os.mkdir(f"{output_dir}/{experiment['name']}")
            print('------------')
            print(f"Generating necessary config file for Experiment: '{experiment['name']}'")
            # NSfile_renderer.renderer(f"{output_dir}/{experiment['name']}", experiment)
            # deter_exp_bootstrap.renderer(f"{output_dir}/{experiment['name']}", experiment, project_name)
            for node in experiment['node']:
                if not os.path.isdir(f"{output_dir}/{experiment['name']}/{node['name']}"):
                    os.mkdir(f"{output_dir}/{experiment['name']}/{node['name']}")
                else:
                    print(f"{output_dir}/{experiment['name']}/{node['name']} already exists!")
                # node_script_renderer.renderer(f"{output_dir}/{experiment['name']}/{node['name']}", node)
                for vm in node['virtual_env']['instance']:
                    if not os.path.isdir(f"{output_dir}/{experiment['name']}/{node['name']}/{vm['name']}_vars"):
                        os.mkdir(f"{output_dir}/{experiment['name']}/{node['name']}/{vm['name']}_vars")
                    else:
                        print(f"{output_dir}/{experiment['name']}/{node['name']}/{vm['name']}_vars already exists!")
                # Vagrantfile_renderer.renderer(f"{output_dir}/{experiment['name']}/{node['name']}", node['virtual_env'])
                # hosts_renderer.renderer(f"{output_dir}/{experiment['name']}/{node['name']}", node['virtual_env'])
                # currently only supports 1 node lan
                # deter_node_bootstrap.renderer(f"{output_dir}/{experiment['name']}/{node['name']}", project_name, experiment['name'], node['name'], experiment['network'][0]['gateway'])
                ansible_playbook_renderer.renderer(f"{output_dir}/{experiment['name']}/{node['name']}", node, project_name, experiment['name'], node['name'])

            print(f"All Done! Plz Check Directory: {output_dir}/{experiment['name']}/")

    elif yaml_parser.get_platform(content) == 'openstack':
        pass


# if __name__ == "__main__":
    # for index, value in sys.argv:
    #     print(f"{index}->{value}")
    # parser(f"{default.SPECIFICATION_PATH}/log4shell/deter_vm_baremetal_flavor.yml")
# specification_content = yaml_parser.yaml_file_load(f"{specification_path}/apt32_specification_complicated.yml")
# print(specification_content)
# vagrantfile_renderer(specification_content['vm'])
# hosts_renderer(specification_content['vm'])
# NSfile_renderer(specification_content['lan'], specification_content['metadata'],specification_content['node'])

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
