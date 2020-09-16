import os
import cli
import components


def NewExperiment(args):
	'''
	NewExperiment: Create a new experiment.
	'''
	exp = components.Experiment()
	exp_dict = cli.Experiment_prompt()
	if exp_dict['teamname'] != '':
		exp.set_teamname(exp_dict['teamname'])
	if exp_dict['experimentname'] != '':
		exp.set_experimentname(exp_dict['experimentname'])
	if exp_dict['lans_num'] != '':
		exp.set_lans_num(exp_dict['lans_num'])
	if exp_dict['nodes_num'] != '':
		exp.set_nodes_num(exp_dict['nodes_num'])
	if exp_dict['vms_num'] != '':
		exp.set_vms_num(exp_dict['vms_num'])
	# exp.pp()
	if exp.get_lans_num() == 0:
		print('No Lan')
	else:
		lan_list = []
		for i in range(exp.get_lans_num()):
			lan = components.Lan()
			lan_dict = cli.Lan_prompt()
			if lan_dict['name'] != '':
				lan.set_name(lan_dict['name'])
			if lan_dict['endpoints'] != '':
				lan.set_endpoints(lan_dict['endpoints'])
			lan_list.append(lan)
	if exp.get_nodes_num() == 0:
		print('No node')
	else:
		node_list = []
		for i in range(exp.get_nodes_num()):
			node = components.Node()
			node_dict = cli.Node_prompt()
			if node_dict['name'] != '':
				node.set_node_name(node_dict['name'])
			if node_dict['connectivity'] != '':
				node.set_node_connectivity(node_dict['connectivity'])
			if node_dict['lan'] != '':
				node.set_node_lan(node_dict['lan'])
			if node_dict['lan_node_ip'] != '':
				node.set_node_lan_node_ip(node_dict['lan_node_ip'])
			if node_dict['lan_node_netmask'] != '':
				node.set_node_lan_node_netmask(node_dict['lan_node_netmask'])
			if node_dict['hostonly_network_name'] != '':
				node.set_node_host_network_name(node_dict['hostonly_network_name'])
			if node_dict['hostonly_network_ip'] != '':
				node.set_node_host_network_ip(node_dict['hostonly_network_ip'])
			if node_dict['hostonly_network_netmask'] != '':
				node.set_node_host_network_netmask(node_dict['hostonly_network_netmask'])
			if node_dict['service'] != '':
				node.set_node_service(node_dict['service'])
			node_list.append(node)
	if exp.get_vms_num() == 0:
		print('No VM')
	else:
		vm_list = []
		for i in range(exp.get_vms_num()):
			vm = components.VM()
			vm_dict = cli.VM_prompt()
			if vm_dict['node'] != '':
				vm.set_vm_node(vm_dict['node'])
			if vm_dict['hostname'] != '':
				vm.set_vm_hostname(vm_dict['hostname'])
			if vm_dict['provider'] != '':
				vm.set_vm_provider(vm_dict['provider'])
			if vm_dict['hostonly_network'] != '':
				vm.set_vm_hostonly_network(vm_dict['hostonly_network'])
			if vm_dict['hostonly_ip'] != '':
				vm.set_vm_hostonly_ip(vm_dict['hostonly_ip'])
			if vm_dict['image'] != '':
				vm.set_vm_image(vm_dict['image'])
			if vm_dict['activity'] != '':
				vm.set_vm_activity(vm_dict['activity'])
			if vm_dict['vrdeport'] != '':
				vm.set_vm_vrdeport(vm_dict['vrdeport'])
			if vm_dict['guest_port_forward'] != '':
				vm.set_vm_guest_port_forward(vm_dict['guest_port_forward'])
			if vm_dict['host_port_forward'] != '':
				vm.set_vm_host_port_forward(vm_dict['host_port_forward'])
			vm_list.append(vm)

	exp.pp()
	for lan in lan_list:
		lan.pp()
	for node in node_list:
		node.pp()
	for vm in vm_list:
		vm.pp()


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


def help_command(command):
	print(f'{command.__doc__}')
