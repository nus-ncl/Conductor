"""
Default configurations for conductor.
"""

# Standard packages
import os

### Conductor path
file_path=os.path.dirname(os.path.realpath(__file__))
conductor_path = os.path.dirname(file_path)
### Versioning
VERSION = '1.0'


### Logging

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


### CLI display
PROMPT = 'Conductor > '
WIDTH = 70 # width of CLI in characters


### File paths

SERVICE_DIRECTORY = os.path.join('service')
ACTIVITY_DIRECTORY = os.path.join('activity')
TEMPLATE_DIRECTORY = os.path.join('templates','templates')
# TMP_DIRECTORY_BASE = os.path.join('component', 'ansible', 'tmp')

### Files locations
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
DOCKER_TEST_FILE = "../outputs/test/dockerfile"

### Ansible config
PING_PLAYBOOK_PATH = 'component/ansible/playbooks/ping.yml'


### File versions
DEFAULT = 'default'
META = 'meta'


### Meta
LOCAL = 'local'
REMOTE = 'remote'
