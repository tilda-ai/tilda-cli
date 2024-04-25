# src/commands/run_init.py
import logging

from src.commands.init.scripts import configure_cmd_real_time_history, touch_tildaconfig
from src.utils import append_to_file


def run_init():
    # create a tildaconfig.toml file if it does not exist
    touch_tildaconfig()

    # add tildaconfig.toml to .gitignore
    append_to_file(".gitignore", "\n\ntildaconfig.toml")

    # configure shell command output logging
    configure_cmd_real_time_history()

    logging.info("Initialization complete. Run `tilda --help` to start using the cli.")

    

