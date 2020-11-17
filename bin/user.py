import sys
sys.path.append("../defaults")
from defaults import default
import yaml
import components

# metadata
metadadta = components.metadata()
metadadta.set_teamname('NCLSecurity')
metadadta.set_experimentname('Enterprise')
metadadta.set_lans_num('1')
metadadta.set_nodes_num('2')
metadadta.set_vms_num('2')
metadadta.set_reserved_nodes('pc2a,pc35g')
output_metadadta_dict = {'metadata': metadadta.output()}

# lan
output_lan = []

lan1 = components.lan()
lan1.set_name('lan1')
lan1.add_endpoints('n1', '172.16.10.101', '255.255.255.0')
lan1.add_endpoints('n2', '172.16.10.102', '255.255.255.0')
output_lan.append(lan1.output())
# output_lan = {'lan': [output_lan1]}

lan2 = components.lan()
lan2.set_name('lan2')
lan2.add_endpoints('n3', '172.16.11.101', '255.255.255.0')
lan2.add_endpoints('n4', '172.16.11.102', '255.255.255.0')
output_lan.append(lan2.output())

output_lan_dict = {'lan': output_lan}

# node
output_node = []
node1 = components.node()
node1.set_name('n1')
node1.set_os_dict(
	{'type': 'node', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'})
node1.set_services_rough(['apt', 'build-essentials'])
node1.add_services_rough('ansible')
# output_node1 = node1.output()
output_node.append(node1.output())

node2 = components.node()
node2.set_name('n2')
node2.set_os_dict(
	{'type': 'node', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'})
node2.add_network('hostonly', 'vboxnet1', '172.16.1.1', '255.255.255.0')
node2.add_network('hostonly', 'vboxnet2', '172.16.2.1', '255.255.255.0')
node2.add_services_rough('nginx')
node2.add_services_rough('attribution')
# output_node2 = node2.output()
output_node.append(node2.output())

node3 = components.node()
node3.set_name('n3')
node3.set_os_dict(
	{'type': 'node', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'})
node3.set_network({
	"hostonly_network": [{"name": "vboxnet1", "ip": "172.16.1.1", "netmask": "255.255.255.0"},
	                     {"name": 'vboxnet2', "ip": "172.16.2.1", "netmask": "255.255.255.0"}],
	"internal_network": [{"name": "vboxnet3", "ip": "172.16.3.1", "netmask": "255.255.255.0"},
	                     {"name": 'vboxnet4', "ip": "172.16.4.1", "netmask": "255.255.255.0"}]
})
node3.set_services_detailed([{}])
# output_node3 = node3.output()
output_node.append(node3.output())

node4 = components.node()
node4.set_name('n4')
node4.set_os_dict(
	{'type': 'node', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'})
node4.add_network('hostonly', 'vboxnet1', '172.16.1.1', '255.255.255.0')
node4.add_network('hostonly', 'vboxnet2', '172.16.2.1', '255.255.255.0')
node4.set_services_detailed([{'service': 'nginx', 'parameter': {'nginx_version': '1.4.0', 'nginx_port': '80'}}, {
	'service': 'php', 'parameter': {'php_version': '1.1'}}])
# output_node4 = node4.output()
output_node.append(node4.output())

output_node_dict = {'node': output_node}

# vm
output_vm = []

vm1 = components.vm()
vm1.set_name('VM1')
vm1.set_node('n1')
vm1.set_provider('virtualbox')
vm1.set_os_dict(
	{'type': 'vagrant', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'})
vm1.add_network('vboxnet1', '172.16.1.101', '255.255.255.0', 'hostonly')
vm1.set_vrde_dict({'enabled': True, 'port': '12346'})
vm1.set_port_forwarding_dict({'guest_port': '22,80', 'host_port': '2200,8080'})
vm1.set_services_rough(['apt', 'build-essentials'])
vm1.add_services_rough('nginx')
# output_vm1 = vm1.output()
output_vm.append(vm1.output())

vm2 = components.vm()
vm2.set_name('VM2')
vm2.set_node('n2')
vm2.set_provider('virtualbox')
vm2.set_os_dict(
	{'type': 'vagrant', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'})
vm2.add_network('vboxnet1', '172.16.1.102', '255.255.255.0', 'hostonly')
vm2.add_network('vboxnet2', '172.16.2.101', '255.255.255.0', 'hostonly')
vm2.set_vrde_dict({'enabled': True, 'port': '12346'})
vm2.set_port_forwarding_dict({'guest_port': '22', 'host_port': '2203'})
# vm2.add_services_rough('nginx')
# output_vm2 = vm2.output()
output_vm.append(vm2.output())

vm3 = components.vm()
vm3.set_name('VM3')
vm3.set_node('n3')
vm3.set_provider('docker')
vm3.set_os_dict(
	{'type': 'docker', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'})
vm3.set_network_dict_list([
	{"gateway": "vboxnet1", "ip": "172.16.1.1", "netmask": "255.255.255.0", "type": "hostonly"},
	{"gateway": "vboxnet2", "ip": "172.16.2.1", "netmask": "255.255.255.0", "type": "hostonly"},
	{"gateway": "vboxnet3", "ip": "172.16.3.1", "netmask": "255.255.255.0", "type": "internal"}
])
vm3.set_vrde_dict({'enabled': True, 'port': '12346'})
vm3.set_port_forwarding_dict({'guest_port': '22', 'host_port': '2203'})
output_vm.append(vm3.output())

vm4 = components.vm()
vm4.set_name('VM4')
vm4.set_node('n4')
vm4.set_provider('docker')
vm4.set_os_dict(
	{'type': 'docker', 'platform': 'Linux', 'release': 'ubuntu', 'version': '16.04', 'architecture': 'amd64'})
vm4.set_network_dict_list([
	{"gateway": "vboxnet1", "ip": "172.16.1.1", "netmask": "255.255.255.0", "type": "hostonly"},
	{"gateway": "vboxnet2", "ip": "172.16.2.1", "netmask": "255.255.255.0", "type": "hostonly"},
	{"gateway": "vboxnet3", "ip": "172.16.3.1", "netmask": "255.255.255.0", "type": "internal"}
])
vm4.set_vrde_dict({'enabled': True, 'port': '12346'})
vm4.set_port_forwarding_dict({'guest_port': '22', 'host_port': '2203'})
output_vm.append(vm4.output())

output_vm_dict = {'vm': output_vm}

# merge output
output = {'version': default.VERSION}
output.update(output_metadadta_dict)
output.update(output_lan_dict)
output.update(output_node_dict)
output.update(output_vm_dict)

# output speciation file
with open('output.yml', 'w') as file:
	yaml.dump(output, file, default_flow_style=False, explicit_start=True, allow_unicode=True, sort_keys=False)
