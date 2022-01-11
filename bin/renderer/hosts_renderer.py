import jinja2
from jinja2 import Environment
from config import default

def renderer(output_dir, virtual_env):
    loader = jinja2.FileSystemLoader(default.TEMPLATE_PATH)
    with open(f"{output_dir}/hosts", 'w') as file:
        env = Environment(loader=loader)
        hosts = env.get_template('hosts.j2')
        content = hosts.render(virtual_env=virtual_env)
        file.write(content)
    print('hosts done!')