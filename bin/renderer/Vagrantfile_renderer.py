import sys
# sys.path.append('../operating_system')
import jinja2
from jinja2 import Environment
from config import default
import operating_system

def renderer(output_dir, virtual_env):
    loader = jinja2.FileSystemLoader(default.TEMPLATE_PATH)
    with open(f"{output_dir}/Vagrantfile", 'w') as file:
        env = Environment(loader=loader)
        Vagrantfile = env.get_template('Vagrantfile.j2')
        content = Vagrantfile.render(virtual_env=virtual_env, os_dict=operating_system.os_dict)
        file.write(content)
    print('Vagrantfile done!')
