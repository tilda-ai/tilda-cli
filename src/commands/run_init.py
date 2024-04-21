# src/commands/run_init.py

import logging
import os
from src.utils import append_to_file, configure_command_output_logging
from src.utils.jinja_setup import get_jinja_env

def touch_tildaconfig():
    if not os.path.exists("tildaconfig.toml"):
        env = get_jinja_env()
        sample_config = env.get_template('tildaconfig.jinja2').render()

        # save the sample config to tildaconfig.toml
        with open("tildaconfig.toml", "w") as file:
            file.write(sample_config)

        logging.info("tildaconfig.toml created successfully.")

def run_init():
    # create a tildaconfig.toml file if it does not exist
    touch_tildaconfig()

    # add tildaconfig.toml to .gitignore
    append_to_file(".gitignore", "\n\ntildaconfig.toml")

    # configure shell command output logging
    configure_command_output_logging()

    logging.info("Initialization complete. Run `tilda --help` to start using the cli.")

    

