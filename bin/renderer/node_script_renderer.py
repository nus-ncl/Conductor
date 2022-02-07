import jinja2
from jinja2 import Environment
from config import default

def renderer(output_dir, node):
    loader = jinja2.FileSystemLoader(default.TEMPLATE_PATH)
    with open(f"{output_dir}/node_script", 'w') as file:
        env = Environment(loader=loader)
        node_script = env.get_template('node_script.j2')
        content = node_script.render(node=node, NODE_VIRTUALBOX_VERSION=default.NODE_VIRTUALBOX_VERSION)
        file.write(content)
    print('node_script done!')