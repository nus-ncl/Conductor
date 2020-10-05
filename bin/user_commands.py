import os
import cli
import components
import yaml_parser
import renderer_test
from defaults import default

metadata_set_function = {"teamname": components.metadata.set_teamname,
                         "experimentname": components.metadata.set_experimentname,
                         "lans_num": components.metadata.set_lans_num,
                         "nodes_num": components.metadata.set_nodes_num,
                         "vms_num": components.metadata.set_vms_num,
                         "reserved_nodes": components.metadata.set_reserved_nodes}
lan_set_function = {"name": components.lan.set_name, "endpoints": components.lan.set_endpoints_dict_list}
node_set_function = {"name": components.node.set_name, "os": components.node.set_os_dict,
                     "network": components.node.set_network, "services": components.node.set_services_v1,
                     "complement_services": components.node.set_services_v2}
vm_set_function = {"name": components.vm.set_name, "node": components.vm.set_node,
                   "provider": components.vm.set_provider, "os": components.vm.set_os_dict,
                   "network": components.vm.set_network_list, "vrde": components.vm.set_vrde_dict,
                   "port_forwarding": components.vm.set_port_forwarding_dict, "services": components.vm.set_services_v1,
                   "complement_services": components.vm.set_services_v2}


def help_command(command):
	print(f"{command.__doc__}")


def Complement_Service(yaml_file):
	pass


def NewExperiment(args):
	'''
	NewExperiment: Create a new experiment.
	'''
	''' Metadata '''
	# metadata component #
	Metadata = components.metadata()
	Metadata_dict = cli.Experiment_prompt()
	# print(Metadata_dict)
	for key, value in Metadata_dict.items():
		metadata_set_function[key](Metadata, value)
	output_metadata = {'metadata': Metadata.output()}
	''' Lan '''
	lan_list = []
	output_lan_entry = []
	for i in range(Metadata.get_lans_num()):
		# lan component #
		lan = components.lan()
		lan_dict = cli.Lan_prompt()
		# print(lan_dict)
		for key, value in lan_dict.items():
			lan_set_function[key](lan, value)
		# lan component list #
		lan_list.append(lan)
	for lan in lan_list:
		output_lan_entry.append(lan.output())
	output_lan = {'lan': output_lan_entry}
	# {'lan': [{'name': 'lan1', 'endpoints': [{'name': 'n1', 'ip': '172.16.1.101', 'netmask': '255.255.255.0'}]}]}
	# print(output_lan)
	''' Node '''
	node_list = []
	output_node_entry = []
	for i in range(Metadata.get_nodes_num()):
		# node component #
		node = components.node()
		node_dict = cli.Node_prompt()
		# print(node_dict)
		for key, value in node_dict.items():
			node_set_function[key](node, value)
		node_list.append(node)
	# for node in node_list:
	# 	output_node_entry.append(node.output())
	# output_node = {'node': output_node_entry}
	# print(output_node)
	''' VM '''
	vm_list = []
	output_vm_entry = []
	for i in range(Metadata.get_vms_num()):
		# VM component
		vm = components.vm()
		vm_dict = cli.VM_prompt()
		# print(vm_dict)
		for key, value in vm_dict.items():
			vm_set_function[key](vm, value)
		vm_list.append(vm)
	# for vm in vm_list:
	# 	output_vm_entry.append(vm.output())
	# output_vm = {'vm': output_vm_entry}

	output = {'version': default.VERSION}
	output.update(output_metadata)
	output.update(output_lan)
	# complement services
	for node in node_list:
		complement_service_list = []
		if node.get_services() == []:
			pass
		else:
			for service in node.get_services():
				complement_service_dict = cli.Services_prompt_v2(service)
				# print(complement_service_dict)
				complement_service_list.append(complement_service_dict)
			node_set_function["complement_services"](node, complement_service_list)
	for node in node_list:
		output_node_entry.append(node.output())
	output_node = {'node': output_node_entry}
	output.update(output_node)

	# complement services
	for vm in vm_list:
		complement_service_list = []
		if vm.get_services() == []:
			pass
		else:
			for service in vm.get_services():
				complement_service_dict = cli.Services_prompt_v2(service)
				# print(complement_service_dict)
				complement_service_list.append(complement_service_dict)
			vm_set_function["complement_services"](vm, complement_service_list)
	for vm in vm_list:
		output_vm_entry.append(vm.output())
	output_vm = {'vm': output_vm_entry}
	output.update(output_vm)
	print(output)

	yaml_parser.yaml_file_dump(output, 'output')


# for key, value in vm_dict.items():
# 	vm_set_function[key](vm, value)
# vm_list.append(vm)


#
# metadata.pp()
# for lan in lan_list:
# 	lan.pp()
# for node in node_list:
# 	node.pp()
# for vm in vm_list:
# 	vm.pp()


def ModifyExperiment(args):
	'''
	ModifyExperiment <Experiment>: Modify an existed experiment
	'''
	pass


def ShowExperiment(args):
	'''
	ShowExperiment <Experiment>: Show a specific experiment description.
	'''
	print(type(args))
	if len(args) == 0:
		help_command(ShowExperiment)
	else:
		print(args)


def ListExperiments(args):
	'''
	ListExperiments: Show all current experiments.
	'''


def DeployExperiment(args):
	'''
	DeployExperiment <Experiment>: Output all configuration files for experiment deployment.
	'''
	if len(args) == 0:
		help_command(DeployExperiment)
	else:
		print('pass')


def LoadTemplateExperiment(args):
	'''
	LoadTemplateExperiment <Experiment>: Load all configuration of an experiment
	'''

	yaml_content = yaml_parser.yaml_templatefile_load(args[0])
	vms, lans, nodes = yaml_parser.yaml_content_parser(yaml_content)
	if default.debug:
		print('vms->')
		print(vms)
	# print('lans->')
	# print(lans)
	# print('nodes->')
	# print(nodes)
	# renderer_test.vagrantfile_renderer(vms)
	# renderer_test.hosts_renderer(vms)
	# renderer_test.nodesfile_renderer(nodes)
	# renderer_test.NSfile_renderer(lans,nodes)
	renderer_test.ansiblefile_renderer(vms)


# renderer_test.clientfile_renderer(experiment_metadata, vms)
# renderer_test.dockerfile_renderer()


def ls(args):
	'''
	ls: list current directory
	'''
	os.system("ls")


def cd(args):
	'''
	cd <directory>: change dir
	'''
	os.chdir(args[0])
