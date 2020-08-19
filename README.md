# Conductor
Testbed Orchestration Tool
## usage
Specify what services you want to deploy, by adding it into 'service' option of each specific VM, in configuration configure.cfg under bin/

The services list are under services/templates

And then, go to the conductor binary, which is under bin/, enable what many file generation you want to get.

For NSfile, NSFILE = 1

For hosts file, HOSTS = 1

For Vagrantfile, VAGRANTFILE = 1

For ansiblefile, ANSIBLEFILE = 1

For clientfile, CLIENTFILE = 1

run it!!!

You'll get output files under /outputs
## doing
1. Interact with VIndex to get user options from its interface, and then make my services templates more soft-coded
2. Design the network/topology functions
3. Design activity module
4. Configuration files generation debug and soft coding
