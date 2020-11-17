"""
Default configurations for conductor.
"""
import os

# debug
debug = 1

# Conductor path
file_path = os.path.dirname(os.path.realpath(__file__))
conductor_path = os.path.dirname(file_path)

# Versioning
VERSION = '1.0'
NODE_VIRTUALBOX_VERSION = '6.0.16'

# Logging
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# File paths
SERVICE_DIRECTORY = os.path.join('service')
ACTIVITY_DIRECTORY = os.path.join('activity')
TEMPLATE_DIRECTORY = os.path.join('templates', 'templates')

# Files locations
CONFIG_FILE = "../config/sherlock/configure.cfg"
GENERATED_CONFIG_FILE = "../config/sherlock/gen_configure.cfg"
NS_FILE = "../outputs/sherlock/NSfile"
VAGRANT_FILE = "../outputs/sherlock/Vagrantfile"
HOSTS_FILE = "../outputs/sherlock/hosts"
ANSIBLE_FILE = "../outputs/sherlock/ansible.yml"
NODES_PATH = "../outputs/sherlock/"
CLIENT_FILE = "../outputs/sherlock/client.xml"
DOCKER_FILE = "../outputs/sherlock/dockerfile"

CONFIG_TEST_FILE = "../config/test/configure_test.cfg"
GENERATED_TEST_CONFIG_FILE = "../config/test/gen_test_configure.cfg"
NS_TEST_FILE = "../outputs/test/NSfile_test"
VAGRANT_TEST_FILE = "../outputs/test/Vagrantfile_test"
HOSTS_TEST_FILE = "../outputs/test/hosts_test"
ANSIBLE_TEST_FILE = "../outputs/test/ansible_test.yml"
CLIENT_TEST_FILE = "../outputs/test/client_test.xml"
NODES_TEST_PATH = "../outputs/test/"
DOCKERFILE_TEST_FILE = "../outputs/test/Dockerfile"
DOCKERCOMPOSE_TEST_FILE = "../outputs/test/docker-compose.yml"

# TIPS
TIP_LAN_NAME = ',(lan[1,2,3,...])'
TIP_ENDPOINT_NAME = ',(n[1,2,3,...])'
TIP_ENDPOINT_INQUIRY = 'Add one Endpoint?(Yes/No, y/n, default:Yes)'
TIP_NODE_NETWORK_INQUIRY = 'Add one Node Network? (Yes/No, y/n, default:Yes)'
TIP_NODE_NETWORK_TYPE_INQUIRY = "What's Node Network's type? ( hostonly/internal, default:hostonly)"
TIP_NODE_NETWORK_NAME = ',(vboxnet[1,2,3,...])'
TIP_NETMASK = '(default: 255.255.255.0)'
TIP_NODE_OS = 'Set Node OS, use default?(default: DeterNode Linux,Ubuntu,16.04,amd64, Yes/No, y/n, default:Yes)'
TIP_VM_PROVIDER = '[ Virtualbox | Docker ]'
TIP_VM_OS = 'Set VM OS, use default?(default: VagrantVirtualbox Linux,Ubuntu,16.04,amd64, Yes/No, y/n, default:Yes)'
TIP_VM_NETWORK_INQUIRY = 'Add one VM Network? (Yes/No, y/n, default:Yes)'
TIP_VM_NETWORK_TYPE_INQUIRY = "What's VM Network's type? ( hostonly/internal, default:hostonly)"
TIP_VM_NAME = ',(VM[1,2,3,...])'
TIP_VM_NODE = ', [Which node to deploy this VM? (eg: n[1,2,3,...])]'
TIP_VM_NETWORK_GATEWAY = ',(vboxnet[1,2,3,...])'
TIP_VM_NETWORK_TYPE = '[ hostonly | internal ]'
TIP_VRDE_ENABLED = ', [Enable VRDE on this VM?(Yes/No, y/n, default:Yes)]'
TIP_VRDE_PORT = ', [Which port on node for VRDE?(default:12345)]'
TIP_PORT_FORWARDING_INQUIRY = 'Set Port Forwarding on this VM?(Yes/No, y/n, default:Yes)'
TIP_PORT_FORWARDING = "[ ports delimited by comma(',') (eg: 22,80, default: '') ] "
TIP_OS_TYPE = '[ node | vagrant | docker ]'
TIP_OS_PLATFORM = '[ Linux | Windows | Darwin ]'
TIP_OS_RELEASE = '[ ubuntu | centos | redhat | win7 ]'
TIP_OS_VERSION = '[ 16.04 | 19.10 ]'
TIP_OS_ARCHITECTURE = '[ i386 | amd64 ]'
TIP_OS_VRDE_ENABLED = 'VRDE Enabled? [ True | False ]'
TIP_SERVICE_INQUIRY = 'Add one Service? (Yes/No, y/n, default:Yes)'
TIP_SERVICE_NAME = "What's service name?"

# Specification Configuration Tips
TIPS = {'metadata': {'teamname': '', 'experimentname': '', 'lans_num': '', 'nodes_num': '', 'vms_num': '',
                     'reserved_nodes': ''},
        'lan': {'name': TIP_LAN_NAME,
                'endpoints': {'inquiry': TIP_ENDPOINT_INQUIRY, 'name': TIP_ENDPOINT_NAME, 'ip': '',
                              'netmask': TIP_NETMASK}},
        'node': {'name': TIP_ENDPOINT_NAME,
                 'os': {'inquiry': TIP_NODE_OS, 'type': TIP_OS_TYPE, 'platform': TIP_OS_PLATFORM,
                        'release': TIP_OS_RELEASE, 'version': TIP_OS_VERSION,
                        'architecture': TIP_OS_ARCHITECTURE},
                 'network': {'inquiry': TIP_NODE_NETWORK_INQUIRY, 'type_inquiry': TIP_NODE_NETWORK_TYPE_INQUIRY,
                             'hostonly_network': {'name': TIP_NODE_NETWORK_NAME, 'ip': '', 'netmask': TIP_NETMASK},
                             'internal_network': {'name': TIP_NODE_NETWORK_NAME, 'ip': '', 'netmask': TIP_NETMASK}},
                 'services': {'inquiry': TIP_SERVICE_INQUIRY}},
        'vm': {'name': TIP_VM_NAME, 'node': TIP_VM_NODE, 'provider': TIP_VM_PROVIDER,
               'os': {'inquiry': TIP_VM_OS, 'type': TIP_OS_TYPE, 'platform': TIP_OS_PLATFORM, 'release': TIP_OS_RELEASE,
                      'version': TIP_OS_VERSION,
                      'architecture': TIP_OS_ARCHITECTURE},
               'network': {'inquiry': TIP_VM_NETWORK_INQUIRY, 'type_inquiry': TIP_VM_NETWORK_TYPE_INQUIRY,
                           'gateway': TIP_VM_NETWORK_GATEWAY, 'ip': '', 'netmask': TIP_NETMASK,
                           'type': TIP_VM_NETWORK_TYPE},
               'vrde': {'enabled': TIP_VRDE_ENABLED, 'port': TIP_VRDE_PORT},
               'port_forwarding': {'inquiry': TIP_PORT_FORWARDING_INQUIRY,'guest_port': TIP_PORT_FORWARDING, 'host_port': TIP_PORT_FORWARDING},
               'services': {'inquiry': TIP_SERVICE_INQUIRY}},
        'os': {'inquiry': TIP_NODE_OS, 'type': TIP_OS_TYPE, 'platform': TIP_OS_PLATFORM,
               'release': TIP_OS_RELEASE, 'version': TIP_OS_VERSION,
               'architecture': TIP_OS_ARCHITECTURE},
        'services': {'inquiry': TIP_SERVICE_INQUIRY, 'name': TIP_SERVICE_NAME}
        }

# Specification Configuration Default
# DEFAULT_LAN_NAME='lan[1,2,3,...]'
# DEFAULT_ENDPOINT_NAME='n[1,2,3,...]'
DEFAULT_NETMASK = '255.255.255.0'
DEFAULT_NODE_OS = 'Linux,Ubuntu,16.04,amd64'
# DEFAULT_PROVIDER='[ Virtualbox | Docker ]'
DEFAULT_VM_OS = 'Linux Ubuntu 16.04 amd64'
# DEFAULT_HOSTONLY_NETWORK_NAME='vboxnet'
# DEFAULT_VM_NAME='VM[1,2,3,...]'
DEFAULT_VRDE_PORT = '12345'
# DEFAULT_TYPE='[ node | vagrant | docker ]'
# DEFAULT_PLATFORM='[ Linux | Windows | Darwin ]'
# DEFAULT_RELEASE='[ ubuntu | centos | redhat | win7 ]'
# DEFAULT_VERSION='[ 16.04 | 19.10 ]'
# DEFAULT_ARCHITECTURE='[ i386 | amd64 ]'
