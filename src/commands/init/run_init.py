# src/commands/run_init.py
from pathlib import Path

from src.logger import logger
from src.utils import append_to_file

from .scripts import configure_cmd_real_time_history, touch_tildaconfig, setup_llm_provider_api_key_configuration


def run_init(args):
    logger.info("Initializing tilda...")

    # print args
    logger.debug("args: %s", args)

    # print welcome message
    logger.info("Welcome to ~tilda! An AI command-line tool for developers.")

    current_directory_path = Path.cwd()

    # create a tildaconfig.toml file if it does not exist
    touch_tildaconfig(current_directory_path)

    # add tildaconfig.toml to .gitignore
    append_to_file(f"{current_directory_path}/.gitignore", "\n\ntildaconfig.toml\n\n")

    result = setup_llm_provider_api_key_configuration(current_directory_path)
    print(result)

    # configure shell command output logger
    configure_cmd_real_time_history()

    logger.info("Initialization complete. Run `tilda --help` to start using the cli.")
