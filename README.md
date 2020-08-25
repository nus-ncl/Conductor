# Conductor
Testbed Orchestration Tool
## usage
1. First, you should run `generate_configure.py` under `/bin`, then you can get a configuration file called `gen_configure.cfg` under `/config`.
2. Second, you can specify what services you want to deploy, by adding it into `service` option of each specific VM, in `gen_configure.cfg`. Actually the generated configration file has some initial values.
3. Third, You can look up `/services` to check how many and what services you can specify.
4. Fourth, run `conductor.py` under `/bin` where you can enable what output files you want to get by setting their switch to 1, like below:

|    Switch   | Value |                Description                |                    Usage                   |
|:-----------:|:-----:|:-----------------------------------------:|:------------------------------------------:|
|    NSFILE   |  0/1  |          Generate NSfile for NCL          |      NCL Node & Network initialization     |
|    HOSTS    |  0/1  | Generate hosts inventory file for Ansible |           Ansible hosts inventory          |
| VAGRANTFILE |  0/1  |      Generate Vagrantfile for Vagrant     |   Construction file of Virtual machines    |
| ANSIBLEFILE |  0/1  |    Generate provision file for Ansible    |     Provision file of Virtual machines     |
|  CLIENTFILE |  0/1  |    Generate client configuration file     | RDP remote access file of Virtual machines |

Finally, You'll get output files under /outputs

## doing
1. Interact with VIndex to get user options from its interface, and then make my services templates more soft-coded
2. Design the network/topology functions
3. Design activity module
4. Configuration files generation debug and soft coding
