# src/utils/jinja_setup.py

from jinja2 import Environment, PackageLoader, select_autoescape

def get_jinja_env():
    env = Environment(
        loader=PackageLoader('src', 'templates'),
        autoescape=select_autoescape(['html', 'xml', 'jinja2'])
    )
    return env