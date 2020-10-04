import os
import yaml
from defaults import default
#
#
# file_path=os.path.dirname(os.path.realpath(__file__))
# conductor_path = os.path.dirname(file_path)
import yaml
import components

# metadata
metadadta = components.metadata()
metadadta.set_teamname('NCLSecurity')
metadadta.set_experimentname('Enterprise')
metadadta.set_lans_num('1')
metadadta.set_nodes_num('2')
metadadta.set_vms_num('2')
output_metadadta = metadadta.output()

# lan
lan1 = components.lan()
lan1.set_name('lan1')
lan1.add_endpoints('n1', '172.16.10.101', '255.255.255.0')
lan1.add_endpoints('n2', '172.16.10.102', '255.255.255.0')
output_lan1 = lan1.output()
output_lan = {'lan': [output_lan1]}

# node
node1 = components.node()
node1.set_name('n1')
node1.set_os('node', 'Linux', 'ubuntu', '16.04', 'amd64')
node1.add_services_v1('ansible')
output_node1 = node1.output()

node2 = components.node()
node2.set_name('n2')
node2.set_os('node', 'Linux', 'ubuntu', '16.04', 'amd64')
node2.add_network('hostonly', 'vboxnet1', '172.16.1.1', '255.255.255.0')
node2.add_network('hostonly', 'vboxnet2', '172.16.2.1', '255.255.255.0')
node2.add_services_v1('nginx')
node2.add_services_v1('attribution')
output_node2 = node2.output()
output_node = {'node': [output_node1, output_node2]}

# vm
vm1 = components.vm()
vm1.set_name('VM1')
vm1.set_node('n2')
vm1.set_provider('virtualbox')
vm1.set_os('vagrant', 'Linux', 'ubuntu', '16.04', 'amd64')
vm1.add_network('vboxnet1', 'hostonly', '172.16.1.101', '255.255.255.0')
vm1.set_vrde(True, '12345')
vm1.set_port_forwarding('22,80', '2202,8080')
vm1.add_services_v1('nginx')
output_vm1 = vm1.output()

vm2 = components.vm()
vm2.set_name('VM2')
vm2.set_node('n2')
vm2.set_provider('virtualbox')
vm2.set_os('vagrant', 'Linux', 'ubuntu', '16.04', 'amd64')
vm2.add_network('vboxnet1', 'hostonly', '172.16.1.102', '255.255.255.0')
vm2.add_network('vboxnet2', 'hostonly', '172.16.2.101', '255.255.255.0')
vm2.set_vrde(True, '12346')
vm2.set_port_forwarding('22', '2203')
# vm2.add_services_v1('nginx')
output_vm2 = vm2.output()
output_vm = {'vm': [output_vm1, output_vm2]}

output = {'version': default.VERSION}
output.update(output_metadadta)
output.update(output_lan)
output.update(output_node)
output.update(output_vm)

# output speciation file
with open('output.yml', 'w') as file:
	yaml.dump(output, file, default_flow_style=False, explicit_start=True, allow_unicode=True, sort_keys=False)

