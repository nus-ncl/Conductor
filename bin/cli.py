"""
Contains variables & methods for conductor's CLI.
"""
import user_commands
import copy

### Versioning
VERSION = '1.0'

### Logging

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

### CLI display
Conductor_PROMPT = 'Conductor > '
NewExperiment_PROMPT = 'NewExperiment > '
ModifyExperiment_PROMPT = 'ModifyExperiment > '
ShowExperiment_PROMPT = 'ShowExperiment > '
ListExperiments_PROMPT = 'ListExperiments > '
DeployExperiment_PROMPT = 'DeployExperiment > '

Experiment_Menu = ['teamname: ', 'experimentname: ', 'lans_num: ', 'nodes_num: ', 'vms_num: ']
Lan_Menu = ['name: ', 'endpoints: ']
Node_Menu = ['name: ', 'lan: ', 'lan_node_ip: ', 'hostonly_network_ip: ', 'service: ']
VM_Menu = ['hostname: ', 'node: ', 'hostonly_ip: ', 'vrdeport: ', 'service: ']
Service_Menu = []

# all description parameters with some defaults
Experiment_dict = {'teamname': '', 'experimentname': '', 'lans_num': '', 'nodes_num': '', 'vms_num': '',
                   'reserve_nodes': ''}
LAN_dict = {'name': '', 'endpoints': ''}
Node_dict = {'name': '', 'connectivity': '', 'lan': '', 'lan_node_ip': '', 'lan_node_netmask': '',
             'hostonly_network_name': '', 'hostonly_network_ip': '', 'hostonly_network_netmask': '', 'service': ''}
VM_dict = {'node': '', 'hostname': '', 'provider': '', 'hostonly_network': '', 'hostonly_ip': '', 'image': '',
           'service': '', 'activity': '', 'vrdeport': '', 'guest_port_forward': '', 'host_port_forward': ''}

LAN_dict_list = []
Node_dict_list = []
VM_dict_list = []

WIDTH = 70  # width of CLI in characters

commands = {"NewExperiment": user_commands.NewExperiment,
            "ModifyExperiment": user_commands.ModifyExperiment,
            "ShowExperiment": user_commands.ShowExperiment,
            "ListExperiments": user_commands.ListExperiments,
            "DeployExperiment": user_commands.DeployExperiment,
            "LoadTemplateExperiment": user_commands.LoadTemplateExperiment,
            "ls": user_commands.ls,
            "cd": user_commands.cd
            }


def input_with_prompt(prompt):
	"""
	Display a prompt and capture input
	"""
	return input(prompt)


def Experiment_prompt():
	'''
	Prompt for defining an experiment
	'''
	print_title('Experiment')
	exp_dict = copy.deepcopy(Experiment_dict)
	for option in Experiment_Menu:
		cmd = input_with_prompt(NewExperiment_PROMPT + option)
		if cmd == 'skip':
			return
		exp_dict[option[:-2]] = cmd

	return exp_dict


def Lan_prompt():
	'''
	Prompt for defining an experiment
	'''
	print_title('LAN')
	lan_dict = copy.deepcopy(LAN_dict)
	for option in Lan_Menu:
		cmd = input_with_prompt(NewExperiment_PROMPT + option)
		if cmd == 'skip':
			return
		lan_dict[option[:-2]] = cmd

	return lan_dict


def Node_prompt():
	'''
	Prompt for defining an experiment
	'''
	print_title('Node')
	node_dict = copy.deepcopy(Node_dict)
	for option in Node_Menu:
		cmd = input_with_prompt(NewExperiment_PROMPT + option)
		if cmd == 'skip':
			return
		node_dict[option[:-2]] = cmd

	return node_dict


def VM_prompt():
	'''
	Prompt for defining an experiment
	'''
	print_title('VM')
	vm_dict = copy.deepcopy(VM_dict)
	for option in VM_Menu:
		cmd = input_with_prompt(NewExperiment_PROMPT + option)
		if cmd == 'skip':
			return
		vm_dict[option[:-2]] = cmd

	return vm_dict

def Service_prompt():
	'''
	Prompt for defining a service
	'''
	print_title('Service')
	vm_dict = copy.deepcopy(VM_dict)
	for option in VM_Menu:
		cmd = input_with_prompt(NewExperiment_PROMPT + option)
		if cmd == 'skip':
			return
		vm_dict[option[:-2]] = cmd

	return vm_dict

def print_banner():
	"""
	Print the banner.
	"""
	print('=' * WIDTH)
	print(' ' * 15 + color('Conductor', status=False, bold=True) + ' | [Version]: LoadTemplateExperiment nginx_admin ' + VERSION)
	print('=' * WIDTH + '\n')


def print_title(title):
	'''
	print title
	'''
	print('\n' + '=' * WIDTH)
	print(' ' * 30 + title)
	print('=' * WIDTH)


def print_help():
	"""
	Print help message.
	"""
	print('\n' + '=' * WIDTH)
	print(' ' * 30 + 'Help')
	print('=' * WIDTH)
	print("\nList of commands:")
	for key in commands.keys():
		user_commands.help_command(commands[key])

	print('\nFor help on specific command, Type: help <command>\n')
	print('Example - help NewExperiment\n')


def color(string, status=True, warning=False, bold=True, yellow=False):
	"""
	Change text color for the linux terminal, defaults to green.
	Set "warning=True" for red.
	"""
	attr = []
	if status:
		# green
		attr.append('32')
	if warning:
		# red
		attr.append('31')
	if bold:
		attr.append('1')
	if yellow:
		attr.append('33')
	return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
