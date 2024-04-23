import logging
import os
from src.utils import get_jinja_env


def touch_tildaconfig():
    if not os.path.exists("tildaconfig.toml"):
        env = get_jinja_env()
        sample_config = env.get_template('tildaconfig.jinja2').render()

        # save the sample config to tildaconfig.toml
        with open("tildaconfig.toml", "w") as file:
            file.write(sample_config)

        logging.info("tildaconfig.toml created successfully.")