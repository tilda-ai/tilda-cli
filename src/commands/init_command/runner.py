# src/commands/run_init.py
from pathlib import Path

from src.common.logger import Logger
from src.utils import append_to_file

from .scripts.configure_cmd_real_time_history import configure_cmd_real_time_history
from .scripts.touch_tildaconfig import touch_tildaconfig
from .scripts.setup_llm_provider_api_key_configuration import setup_llm_provider_api_key_configuration

class InitCommandRunner:
    def __init__(self):
        self.logger = Logger().get_logger()
        
    def run(self, args):
        self.logger.info("Initializing tilda...")

        # print args
        self.logger.debug("args: %s", args)

        # print welcome message
        self.logger.info("Welcome to ~tilda! An AI command-line tool for developers.")

        current_directory_path = Path.cwd()

        # create a tildaconfig.toml file if it does not exist
        touch_tildaconfig(current_directory_path)

        # add tildaconfig.toml to .gitignore
        append_to_file(f"{current_directory_path}/.gitignore", "\n\ntildaconfig.toml\n\n")

        result = setup_llm_provider_api_key_configuration(current_directory_path)
        print(result)

        # configure shell command output logger
        configure_cmd_real_time_history()

        self.logger.info("Initialization complete. Run `tilda --help` to start using the cli.")