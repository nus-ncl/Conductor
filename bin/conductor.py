import os
import configparser
from jinja2 import Environment, PackageLoader
from defaults import default


def print_configure_file(config_file):
		conf = configparser.ConfigParser()
		conf.read(config_file)
		# print all sections and key-values
		for section in conf.sections():
				print('---------------------')
				print('[%s]' % (section))
				for key in conf[section]:
						print("%s:%s" % (key, conf[section][key]))
				print('---------------------')


def vagrantfile_renderer(hostname, image, ip):
		file = open(default.VAGRANT_FILE, 'w')
		env = Environment(loader=PackageLoader('templates'))
		Vagrantfile = env.get_template('Vagrantfile.j2')
		content = Vagrantfile.render(hostname=hostname, image=image, ip=ip)
		file.write(content)
		file.close()


def hosts_renderer(hostname, ip):
		file = open(default.HOSTS_FILE, 'w')
		env = Environment(loader=PackageLoader('templates'))
		hostsfile = env.get_template('hosts.j2')
		content = hostsfile.render(hostname=hostname, ip=ip)
		file.write(content)
		file.close()


def ansiblefile_header_renderer(hostname):
		file = open(default.ANSIBLE_FILE, 'a')
		env = Environment(loader=PackageLoader('templates'))
		ansiblefile = env.get_template('ansiblefile_header.j2')
		content = ansiblefile.render(hostname=hostname)
		file.write(content)
		# file.write('\n')
		file.close()


def ansiblefile_renderer(service, hostname):
		# dir = os.path.dirname(__file__)
		file = open(default.ANSIBLE_FILE, 'a')
		env = Environment(loader=PackageLoader('services'))
		ansiblefile = env.get_template(service + '.j2')
		# content = ansiblefile.render(path=dir + '/../services/' + service)
		content = ansiblefile.render(host_name=hostname, USER='{{ ansible_env.USER }}')
		file.write(content)
		file.write('\n\n')
		file.close()


def NSfile_renderer():
		file = open(default.NS_FILE, 'w')
		env = Environment(loader=PackageLoader('templates'))
		NSfile = env.get_template('NSfile.j2')
		content = NSfile.render(node_num=2)
		file.write(content)
		file.close()


def Clientfile_renderer(hostname):
		file = open(default.CLIENT_FILE, 'w')
		env = Environment(loader=PackageLoader('templates'))
		Clientfile = env.get_template('Client.j2')
		content = Clientfile.render(hostname=hostname)
		file.write(content)
		file.close()


if __name__ == "__main__":
		PRINT = 0
		NSFILE = 0
		HOSTS = 0
		VAGRANTFILE = 0
		ANSIBLEFILE = 1
		CLIENTFILE = 0

		conf = configparser.ConfigParser()
		conf.read(default.CONFIG_FILE)

		hostname = conf.get("VM1", "hostname")
		image = conf.get("VM1", "image")
		ip = conf.get("VM1", "ip")
		service = conf.get("VM1", "service")
		service_list = service.split(',')

		print(hostname)
		print(image)
		print(ip)
		print(service)
		print(service_list)

		# print configure.cfg
		if (PRINT):
				print_configure_file(default.CONFIG_FILE)

		# generate NSfile
		if (NSFILE):
				NSfile_renderer()

		# generate hosts file
		if (HOSTS):
				hosts_renderer(hostname, ip)

		# generate vagrantfile
		if (VAGRANTFILE):
				vagrantfile_renderer(hostname, image, ip)

		# generate ansible file
		if (ANSIBLEFILE):
			ansiblefile_header_renderer(hostname)
			for i in service_list:
				ansiblefile_renderer(i, hostname)

		# generate clientfile
		if(CLIENTFILE):
				Clientfile_renderer(hostname)



