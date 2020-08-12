import os
import configparser

CONFIG_FILE = "configure.cfg"
host = "172.16.1.1"
hostname = "VM1"
image = "generic/ubuntu1910"
service = "blx,zara"

if __name__ == "__main__":

		cfg_file=open(CONFIG_FILE,'w')
		conf = configparser.ConfigParser()
		conf.add_section("host")
		conf.add_section("service")
		conf.set("host","IP",host)
		conf.set("host","hostname",hostname)
		conf.set("host","image",image)
		conf.set("service","name",service)

		conf.write(cfg_file)
		cfg_file.close()
