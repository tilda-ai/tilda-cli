# src/commands/run_init.py
import logging
from pathlib import Path

from .scripts import configure_cmd_real_time_history, touch_tildaconfig
from src.utils import append_to_file


def run_init(args):
    logging.info("Initializing tilda...")

    # print args
    logging.debug(f"args: {args}")

    # print welcome message
    logging.info("Welcome to Tilda! An AI command-line tool for developers.")

    root_path = Path.cwd()
    
    # create a tildaconfig.toml file if it does not exist
    touch_tildaconfig(root_path)

    # add tildaconfig.toml to .gitignore
    append_to_file(f"{root_path}/.gitignore", "\n\ntildaconfig.toml\n\n")

    # configure shell command output logging
    configure_cmd_real_time_history()

    logging.info("Initialization complete. Run `tilda --help` to start using the cli.")

    

