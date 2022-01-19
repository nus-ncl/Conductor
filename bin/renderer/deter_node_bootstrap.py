import jinja2
from jinja2 import Environment
from config import default


def renderer(output_dir, project_name, experiment_name, node_name, node_gateway):
    loader = jinja2.FileSystemLoader(default.TEMPLATE_PATH)
    with open(f"{output_dir}/node.sh", 'w') as file:
        env = Environment(loader=loader)
        NSfile = env.get_template('deter_node_bootstrap.j2')
        content = NSfile.render(project_name=project_name, experiment_name=experiment_name, node_name=node_name, node_gateway=node_gateway)
        file.write(content)
    print('bootstrap.sh done!')
