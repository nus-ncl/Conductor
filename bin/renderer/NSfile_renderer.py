import jinja2
from jinja2 import Environment
from config import default

def renderer(output_dir, experiment):
    loader = jinja2.FileSystemLoader(default.TEMPLATE_PATH)
    with open(f"{output_dir}/NSfile", 'w') as file:
        env = Environment(loader=loader)
        NSfile = env.get_template('NSfile.j2')
        content = NSfile.render(experiment=experiment, deter_node_os=default.DETER_NODE_OS, deter_node_bandwidth=default.DETER_BANDWIDTH, deter_node_delay=default.DETER_DELAY)
        file.write(content)
    print('NSfile done!')