import jinja2
from jinja2 import Environment
from config import default


def renderer(output_dir, experiment, project_name):
    loader = jinja2.FileSystemLoader(default.TEMPLATE_PATH)
    with open(f"{output_dir}/bootstrap.sh", 'w') as file:
        env = Environment(loader=loader)
        NSfile = env.get_template('deter_exp_bootstrap.j2')
        content = NSfile.render(experiment=experiment, project_name=project_name)
        file.write(content)
    print('bootstrap.sh done!')
