import jinja2
from jinja2 import Environment
from config import default


def renderer(output_dir, instance, project_name, platform):
    loader = jinja2.FileSystemLoader(default.TEMPLATE_PATH)
    with open(f"{output_dir}/client.xml", 'w') as file:
        env = Environment(loader=loader)
        client = env.get_template(f"client_{platform}.j2")
        print(instance)
        print(project_name)
        content = client.render(instance=instance, project_name=project_name, deter_node_delay=default.DETER_NODE_OS)
        file.write(content)
    print('client.xml done!')
