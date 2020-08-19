"""
Configurations for conductor.
"""

# Standard packages
import os


### Versioning
VERSION = '0'


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
CONFIG_FILE = "configure.cfg"
NS_FILE = "../outputs/NSfile"
VAGRANT_FILE = "../outputs/Vagrantfile"
HOSTS_FILE = "../outputs/hosts"
ANSIBLE_FILE = "../outputs/ansible.yml"
CLIENT_FILE = "../outputs/client.xml"

### Ansible config
PING_PLAYBOOK_PATH = 'component/ansible/playbooks/ping.yml'


### File versions
DEFAULT = 'default'
META = 'meta'


### Meta
LOCAL = 'local'
REMOTE = 'remote'
