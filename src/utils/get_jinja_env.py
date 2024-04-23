# src/utils/jinja_setup.py

from jinja2 import Environment, PackageLoader, select_autoescape

def get_jinja_env():
    env = Environment(
        loader=PackageLoader('src', 'commands'),
        autoescape=select_autoescape(['jinja2'])
    )
    return env