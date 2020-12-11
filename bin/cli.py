"""
Contains everything regarding conductor"s CLI.
"""
import sys
sys.path.append('../defaults')
import user_commands
import copy
import yaml_parser
import default

# Versioning
VERSION = "1.0"

# Logging
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# CLI display
Conductor_PROMPT = "Conductor > "
NewExperiment_PROMPT = "NewExperiment > "
ModifyExperiment_PROMPT = "ModifyExperiment > "
ShowExperiment_PROMPT = "ShowExperiment > "
ListExperiments_PROMPT = "ListExperiments > "
DeployExperiment_PROMPT = "DeployExperiment > "

# Metadata_Menu = ["teamname: ", "experimentname: ", "lans_num: ", "nodes_num: ",
#                  "vms_num: ", "reserved_nodes: "]
# Lan_Menu = [f"name(tip: {default.TIP_LAN_NAME}): ", f"endpoints(tip: {default.TIP_ENDPOINT_INQUIRY}): "]
# Endpoint_Menu = [f"name(tip: {default.TIP_ENDPOINT_NAME}): ", "ip: ", f"netmask(default: {default.TIP_NETMASK}): "]
# Node_Menu = [f"OS(default: {default.TIP_NODE_OS}): ", "network: ", "service: "]
# OS_Menu = [f"type(tip: {default.TIP_TYPE}): ", f"platform(tip: {default.TIP_PLATFORM}): ",
#            f"release(tip: {default.TIP_RELEASE}): ", f"version(tip: {default.TIP_VERSION}): ",
#            f"architecture(tip: {default.TIP_ARCHITECTURE}): "]
# Node_Network_Menu = ["hostonly_network: ", "internal_network: "]
# VM_Network_Menu = [f"gateway(tip: {default.TIP_VM_NETWORK_GATEWAY}): ", "ip: ",
#                    f"netmask(tip: {default.TIP_NETMASK}): "]
# Hostonly_Network_Menu = [f"name(tip: {default.TIP_HOSTONLY_NETWORK_NAME}): ", "ip",
#                          f"netmask(default: {default.TIP_NETMASK}): "]
# Internal_Network_Menu = []
# Vrde_Menu = [f"enabled(tip: {default.TIP_VRDE_ENABLED}): ", f"port(default: {default.TIP_VRDE_PORT}): "]
# Port_Forwarding_Menu = [f"guest_port(tip: {default.TIP_GUEST_PORT}): ", f"host_port(tip: {default.TIP_HOST_PORT}): "]
# Service_Menu = []
# VM_Menu = [f"name(tip: {default.TIP_VM_NAME}): ", "node: ", f"provider(tip: {default.TIP_PROVIDER}): ",
#            f"OS(default: {default.TIP_VM_OS}): " "vrde: ", "port_forwarding: ", "service: "]
#
# # all description parameters with some defaults
# # Metadata_dict = {"teamname": '', "experimentname": '', "lans_num": '', "nodes_num": '', "vms_num": '', "reserved_nodes": ''}
# LAN_dict = {"name": '', "endpoints": ''}
# Node_dict = {"name": '', "os": '', "network": '', "service": ''}
# VM_dict = {"node": '', "hostname": '', "provider": '', "hostonly_network": '', "hostonly_ip": '', "image": '',
#            "service": '', "activity": '', "vrdeport": '', "guest_port_forward": '', "host_port_forward": ''}

# LAN_dict_list = []
# Node_dict_list = []
# VM_dict_list = []
# width of CLI in characters
WIDTH = 70

# CLI-command pairs
commands = {
	"NewExperiment": user_commands.NewExperiment,
	"ModifyExperiment": user_commands.ModifyExperiment,
	"ShowExperiment": user_commands.ShowExperiment,
	"ListExperiments": user_commands.ListExperiments,
	"DeployExperiment": user_commands.DeployExperiment,
	"LoadExperiment": user_commands.LoadExperiment,
	"LoadTemplateExperiment": user_commands.LoadTemplateExperiment,
	"ls": user_commands.ls,
	"cd": user_commands.cd
}


def input_with_prompt(prompt):
	"""
	Display a prompt and capture input
	"""
	return input(prompt)


'''
Disciplines:
In a component
	if one key's value's type is a variable list, we should have an inquiry loop in that 'parent' component-level prompt.
	if one key's value's type is a dict, we call that specific key_prompt.
	if one key's value's type is string, get user input via input directly.
	
If we want to set default:
	if one key's value's type is a variable list, we set it in that 'child' component-level prompt.
	if one key's value's type is a dict, we set it in specific key_prompt.
	if one key's value's type is string, we set it via input directly.

'''


def Metadata_prompt():
	'''
	Prompt for defining an experiment
	'''
	Metadata_key = ["teamname", "experimentname", "lans_num", "nodes_num", "vms_num", "reserved_nodes"]
	inputs = []
	print_title("Metadata")
	for option in Metadata_key:
		cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['metadata'][option]}: ")
		inputs.append(cmd)
	Metadata_dict = dict(zip(Metadata_key, inputs))
	return Metadata_dict


def Endpoint_prompt():
	'''
	Prompt for defining one endpoint
	'''
	Endpoint_key = ["name", "ip", "netmask"]
	inputs = []
	print_title("Endpoint")
	for option in Endpoint_key:
		cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['lan']['endpoints'][option]}: ")
		if option == "netmask" and cmd in ['Yes', 'yes', 'Y', 'y', '']:
			inputs.append('255.255.255.0')
		else:
			inputs.append(cmd)
	print("=" * WIDTH + "\n")
	Endpoint_dict = dict(zip(Endpoint_key, inputs))
	return Endpoint_dict


def Lan_prompt():
	'''
	Prompt for defining an experiment
	'''
	Lan_key = ["name", "endpoints"]
	inputs = []
	endpoints_list = []
	print_title("LAN")
	for option in Lan_key:
		if option == "endpoints":
			while True:
				cmd = input_with_prompt(
					f"{NewExperiment_PROMPT}{option},{default.TIPS['lan']['endpoints']['inquiry']}: ")
				if cmd in ['Yes', 'yes', 'Y', 'y', '']:
					endpoint_dict = Endpoint_prompt()
					endpoints_list.append(endpoint_dict)
				else:
					inputs.append(endpoints_list)
					break
		else:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['lan'][option]}: ")
			inputs.append(cmd)

	Lan_dict = dict(zip(Lan_key, inputs))
	return Lan_dict


def Node_OS_prompt():
	Node_OS_key = ["type", "platform", "release", "version", "architecture"]
	inputs = []
	cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['node']['os']['inquiry']}")
	if cmd in ['Yes', 'yes', 'Y', 'y', '']:
		inputs = ["node", "Linux", "ubuntu", "16.04", "amd64"]
	else:
		for option in Node_OS_key:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['node']['os'][option]}: ")
			inputs.append(cmd)
	Node_OS_dict = dict(zip(Node_OS_key, inputs))
	return Node_OS_dict


def Node_Hostonly_Network_prompt():
	Hostonly_Network_key = ["name", "ip", "netmask"]
	inputs = []
	for option in Hostonly_Network_key:
		cmd = input_with_prompt(
			f"{NewExperiment_PROMPT}{option}{default.TIPS['node']['network']['hostonly_network'][option]}: ")
		if option == "netmask" and cmd in ['Yes', 'yes', 'Y', 'y', '']:
			inputs.append('255.255.255.0')
		else:
			inputs.append(cmd)
	Node_Hostonly_Network_dict = dict(zip(Hostonly_Network_key, inputs))
	return Node_Hostonly_Network_dict


def Node_Internal_Network_prompt():
	Internal_Network_key = ["name", "ip", "netmask"]
	inputs = []
	for option in Internal_Network_key:
		cmd = input_with_prompt(
			f"{NewExperiment_PROMPT}{option}{default.TIPS['node']['network']['internal_network'][option]}: ")
		if option == "netmask" and cmd in ['Yes', 'yes', 'Y', 'y', '']:
			inputs.append('255.255.255.0')
		else:
			inputs.append(cmd)
	Node_Internal_Network_dict = dict(zip(Internal_Network_key, inputs))
	return Node_Internal_Network_dict


def Node_Network_prompt():
	Node_Network_key = ["hostonly_network", "internal_network"]
	inputs = []
	Hostonly_Network_list = []
	Internal_Network_list = []
	while True:
		cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['node']['network']['inquiry']}: ")
		if cmd in ['Yes', 'yes', 'Y', 'y', '']:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['node']['network']['type_inquiry']}: ")
			if cmd in ['hostonly', 'Hostonly', 'Y', 'y', '']:
				Node_Hostonly_Network_dict = Node_Hostonly_Network_prompt()
				Hostonly_Network_list.append(Node_Hostonly_Network_dict)
			elif cmd in ['internal', 'Internal','N','n']:
				Node_Internal_Network_dict = Node_Internal_Network_prompt()
				Internal_Network_list.append(Node_Internal_Network_dict)
			else:
				pass
		elif cmd in ['No', 'no', 'N', 'n']:
			break
		else:
			pass
	inputs.append(Hostonly_Network_list)
	inputs.append(Internal_Network_list)
	Node_Network_dict = dict(zip(Node_Network_key, inputs))

	# Take format as reference
	# Node_Network_dict = {"hostonly_network": [{"name": "vboxnet1", "ip": "172.16.1.1", "netmask": "255.255.255.0"},
	#                                           {"name": 'vboxnet2', "ip": "172.16.2.1", "netmask": "255.255.255.0"}],
	#                      "internal_network": [{"name": "vboxnet3", "ip": "172.16.3.1", "netmask": "255.255.255.0"},
	#                                           {"name": 'vboxnet4', "ip": "172.16.4.1", "netmask": "255.255.255.0"}]
	#                      }
	return Node_Network_dict


def Services_prompt_rough():
	inputs = []
	while True:
		cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['services']['inquiry']}: ")
		if cmd in ['Yes', 'yes', 'Y', 'y', '']:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['services']['name']}: ")
			inputs.append(cmd)
		elif cmd in ['No', 'no', 'N', 'n']:
			break
		else:
			pass
	return inputs


def Services_prompt_detailed(service):
	Service_key = ["service", "parameter"]
	if service == '':
		service_list = [None, {}]
	else:
		# parse the [service].yml file
		yaml_content = yaml_parser.yaml_file_load(f"{default.conductor_path}/services/{service}/{service}")
		# hard copy, one used as default, one updated by user input
		if not bool(yaml_content):
			yaml_content['service']=service
			parameters = {'Error': 'No Such Service'}
		elif 'parameter' not in yaml_content:
			parameters = {}
		else:
			parameters = copy.deepcopy(yaml_content['parameter'])
			for key, value in yaml_content['parameter'].items():
				cmd = input_with_prompt(f"{yaml_content['service']} -> {key}(default:{value}): ")
				if cmd in ['Yes', 'yes', 'Y', 'y', '']:
					pass
				else:
					parameters[key] = cmd

		service_list = [yaml_content['service'], parameters]
	Service_dict = dict(zip(Service_key, service_list))
	return Service_dict


def Node_prompt():
	'''
	Prompt for defining an experiment
	'''
	Node_key = ["name", "os", "network", "services"]
	inputs = []
	print_title("Node")
	for option in Node_key:
		if option == "os":
			OS_dict = Node_OS_prompt()
			inputs.append(OS_dict)
		elif option == "network":
			Node_Network_dict = Node_Network_prompt()
			inputs.append(Node_Network_dict)
		elif option == "services":
			service_list = Services_prompt_rough()
			inputs.append(service_list)
		else:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['node'][option]}: ")
			inputs.append(cmd)

	Node_dict = dict(zip(Node_key, inputs))
	return Node_dict


def VM_OS_prompt():
	VM_OS_key = ["type", "platform", "release", "version", "architecture"]
	inputs = []
	cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['vm']['os']['inquiry']}")
	if cmd in ['Yes', 'yes', 'Y', 'y', '']:
		inputs = ["vagrant", "Linux", "ubuntu", "16.04", "amd64"]
	else:
		for option in VM_OS_key:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['vm']['os'][option]}: ")
			inputs.append(cmd)
	VM_OS_dict = dict(zip(VM_OS_key, inputs))
	return VM_OS_dict


def VM_hostonly_Network_prompt():
	Hostonly_Network_key = ["gateway", "ip", "netmask"]
	inputs = []
	for option in Hostonly_Network_key:
		cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['vm']['network'][option]}: ")
		if option == "netmask" and cmd in ['Yes', 'yes', 'Y', 'y', '']:
			inputs.append('255.255.255.0')
		else:
			inputs.append(cmd)
	Hostonly_Network_dict = dict(zip(Hostonly_Network_key, inputs))
	Hostonly_Network_dict['type'] = 'hostonly'

	# Take format as reference
	# Hostonly_Network_dict={"gateway":"vboxnet1", "ip":"172.16.1.1", "netmask":"255.255.255.0","type":"hostonly"}
	return Hostonly_Network_dict


def VM_internal_Network_prompt():
	Internal_Network_key = ["gateway", "ip", "netmask"]
	inputs = []
	for option in Internal_Network_key:
		cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['vm']['network'][option]}: ")
		if option == "netmask" and cmd in ['Yes', 'yes', 'Y', 'y', '']:
			inputs.append('255.255.255.0')
		else:
			inputs.append(cmd)
	Internal_Network_dict = dict(zip(Internal_Network_key, inputs))
	Internal_Network_dict['type'] = 'internal'

	# Take format as reference
	# Internal_Network_dict={"gateway":"vboxnet2", "ip":"172.16.2.1", "netmask":"255.255.255.0","type":"internal"}
	return Internal_Network_dict


def VM_Network_prompt():
	vm_networks_list = []
	while True:
		cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['vm']['network']['inquiry']}: ")
		if cmd in ['Yes', 'yes', 'Y', 'y', '']:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['vm']['network']['type_inquiry']}: ")
			if cmd in ['hostonly', 'Hostonly', 'Y', 'y', '']:
				VM_hostonly_Network_dict = VM_hostonly_Network_prompt()
				vm_networks_list.append(VM_hostonly_Network_dict)
			elif cmd in ['internal', "Internal"]:
				VM_internal_Network_dict = VM_internal_Network_prompt()
				vm_networks_list.append(VM_internal_Network_dict)
			else:
				pass
		elif cmd in ['No', 'no', 'N', 'n']:
			break
		else:
			pass

	# Take format as reference
	# vm_networks_list = [
	# 	                  {"gateway": "vboxnet1", "ip": "172.16.1.1", "netmask": "255.255.255.0", "type": "hostonly"},
	#                     {"gateway": "vboxnet1", "ip": "172.16.1.1", "netmask": "255.255.255.0", "type": "hostonly"},
	#                     {"gateway": "vboxnet2", "ip": "172.16.2.1", "netmask": "255.255.255.0", "type": "internal"}
	#                    ]
	return vm_networks_list


def VRDE_prompt():
	vrde_key = ['enabled', 'port']
	inputs = []
	for option in vrde_key:
		cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['vm']['vrde'][option]}: ")
		if option == "enabled":
			if cmd in ['True', 'true', 'Yes', 'yes', 'Y', 'y', '']:
				inputs.append(True)
			else:
				inputs.append(False)
				inputs.append('')
				break
		else:
			if cmd in ['Yes', 'yes', 'Y', 'y', '']:
				inputs.append("12345")
			else:
				inputs.append(cmd)
	vrde_dict = dict(zip(vrde_key, inputs))
	return vrde_dict


def Port_forwarding_prompt():
	port_forwarding_key = ['guest_port', 'host_port']
	inputs = []
	cmd = input_with_prompt(f"{NewExperiment_PROMPT}{default.TIPS['vm']['port_forwarding']['inquiry']}")
	if cmd in ['Yes', 'yes', 'Y', 'y', '']:
		for option in port_forwarding_key:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['vm']['port_forwarding'][option]}: ")
			inputs.append(cmd)
	else:
		inputs = ['','']

	port_forwarding_dict = dict(zip(port_forwarding_key, inputs))
	return port_forwarding_dict


def VM_prompt():
	'''
	Prompt for defining an experiment
	'''
	VM_key = ["name", "node", "provider", "os", "network", "vrde", "port_forwarding", "services"]
	inputs = []
	print_title("VM")
	for option in VM_key:
		if option == "os":
			OS_dict = VM_OS_prompt()
			inputs.append(OS_dict)
		elif option == "network":
			VM_Network_list = VM_Network_prompt()
			inputs.append(VM_Network_list)
		elif option == "vrde":
			vrde_dict = VRDE_prompt()
			inputs.append(vrde_dict)
		elif option == 'port_forwarding':
			port_forwarding_dict = Port_forwarding_prompt()
			inputs.append(port_forwarding_dict)
		elif option == "services":
			service_list = Services_prompt_rough()
			inputs.append(service_list)
		else:
			cmd = input_with_prompt(f"{NewExperiment_PROMPT}{option}{default.TIPS['vm'][option]}: ")
			inputs.append(cmd)
	VM_dict = dict(zip(VM_key, inputs))
	return VM_dict


def print_banner():
	"""
	Print the banner.
	"""
	print("=" * WIDTH)
	print(" " * 15 + color("Conductor", status=False, bold=True) + " | [Version]: LoadExperiment " + VERSION)
	print("=" * WIDTH + "\n")


def print_title(title):
	'''
	print title
	'''
	print("\n" + "=" * WIDTH)
	print(" " * 30 + title)
	print("=" * WIDTH)


def print_subtitle(title):
	'''
	print title
	'''
	print("\n" + "-" * WIDTH)
	print(" " * 30 + title)
	print("-" * WIDTH)


def print_help():
	"""
	Print help message.
	"""
	print("\n" + "=" * WIDTH)
	print(" " * 30 + "Help")
	print("=" * WIDTH)
	print("\nList of commands:")
	for key in commands.keys():
		user_commands.help_command(commands[key])

	print("\nFor help on specific command, Type: help <command>\n")
	print("Example - help NewExperiment\n")


def color(string, status=True, warning=False, bold=True, yellow=False):
	"""
	Change text color for the linux terminal, defaults to green.
	Set "warning=True" for red.
	"""
	attr = []
	if status:
		# green
		attr.append("32")
	if warning:
		# red
		attr.append("31")
	if bold:
		attr.append("1")
	if yellow:
		attr.append("33")
	return "\x1b[%sm%s\x1b[0m" % (";".join(attr), string)
