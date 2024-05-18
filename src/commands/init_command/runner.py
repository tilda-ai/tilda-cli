# src/commands/run_init.py
from pathlib import Path
from rich.console import Console

from src.lib_pkg.utils import append_to_file

# from .scripts.configure_cmd_real_time_history import configure_cmd_real_time_history
from .scripts.touch_tildaconfig import touch_tildaconfig
# from .scripts.setup_llm_provider_api_key_configuration import setup_llm_provider_api_key_configuration


class InitCommandRunner:
    def __init__(self):
        self.console = Console()

    def run(self, args):
        self.console.print("[gray58]Initializing ~tilda. An AI powered command-line tool for us developers. Welcome to the party![/gray58]\n")

        current_directory_path = Path.cwd()

        # create a tildaconfig.toml file if it does not exist
        touch_tildaconfig(current_directory_path)

        # add tildaconfig.toml to .gitignore
        append_to_file(
            f"{current_directory_path}/.gitignore", "\n\ntildaconfig.toml\n\n"
        )

        # result = setup_llm_provider_api_key_configuration(current_directory_path)
        # print(result)

        # configure shell command output logger
        # configure_cmd_real_time_history()

        self.console.print("[green]Initialization complete.[/green]\n")
        self.console.print("Run `tilda --help` to start using the cli.")
