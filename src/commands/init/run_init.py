# src/commands/run_init.py
from pathlib import Path

from .enums.provider import Provider
from .scripts.configure_provider_init import configure_provider_init
from .scripts.ask_which_provider import ask_which_provider_to_use
from src.logger import logger
from src.utils import append_to_file

from .scripts import configure_cmd_real_time_history, touch_tildaconfig


def run_init(args):
    logger.info("Initializing tilda...")

    # print args
    logger.debug(f"args: {args}")

    # print welcome message
    logger.info("Welcome to Tilda! An AI command-line tool for developers.")

    root_path = Path.cwd()
    
    # create a tildaconfig.toml file if it does not exist
    touch_tildaconfig(root_path)

    # add tildaconfig.toml to .gitignore
    append_to_file(f"{root_path}/.gitignore", "\n\ntildaconfig.toml\n\n")

    selectedProvider:Provider = ask_which_provider_to_use()
    
    configure_provider_init(selectedProvider, root_path)
    
    logger.info('Testing!')

    # configure shell command output logger
    configure_cmd_real_time_history()

    logger.info("Initialization complete. Run `tilda --help` to start using the cli.")

    

