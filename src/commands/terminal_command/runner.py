import subprocess
import json
import time
import sys

from rich.console import Console

from src.lib_pkg.logger import Logger
from src.config import Config

from .agent import TerminalAgent
from .types import TerminalCommandArgs
from .tui.print_command import print_command
from .tui.prompt_command_action import prompt_command_action
from .tui.prompt_error_resolution import prompt_error_resolution
from .tui.print_command_output import print_command_output
from .tui.print_command_error import print_command_error


class TerminalCommandRunner:
    def __init__(self):
        self.console = Console()
        self.config = Config()
        self.logger = Logger().get_logger()

    def run(self, args: TerminalCommandArgs):
        self.logger.info(
            "[run_terminal]: Running tilda terminal agent with args %s", args
        )

        if args.mock:
            with self.console.status(
                "[bold green]Processing...[/bold green]\n", spinner="dots"
            ):
                time.sleep(1)
                commands = json.loads(self.config.get_terminal_command_mock_response())
        else:
            with self.console.status(
                "[bold green]Processing...[/bold green]\n", spinner="dots"
            ):
                commands = TerminalAgent().generate_commands(args)

        self.render(commands)

    def render(self, commands):
        for command in sorted(commands, key=lambda x: x["executionOrder"]):
            self.console.print()
            print_command(command, len(commands))
            action = prompt_command_action()

            if action == "Run":
                self.run_command(
                    command["shellScript"],
                    is_last=command["executionOrder"] == len(commands),
                )

            if action == "Skip":
                self.console.print(
                    "[grey50]└── Command skipped.[/grey50]"
                )
                continue

            if action == "Edit":
                self.console.print(
                    "[grey50]└── Command edit feature not yet implemented.[/grey50]"
                )
                continue

            if action == "Explain":
                self.console.print(
                    "[grey50]└── Command explain feature not yet implemented.[/grey50]"
                )
                continue

            if action == "Terminate":
                self.console.print("[grey50]└── Terminating...[/grey50]")
                self.console.print("\n[green bold]Process Terminated.[/green bold]")
                sys.exit(0)

    def run_command(self, command, is_last=False):
        try:
            with self.console.status(
                "[grey50]Running...[/grey50]", spinner="dots", spinner_style="grey50"
            ):
                time.sleep(1)
                result = subprocess.run(
                    command, shell=True, check=True, text=True, capture_output=True
                )

            if result.stdout:
                print_command_output(output=result.stdout)
            else:
                self.console.print("[grey50]└── No output returned.[/grey50]")

        except subprocess.CalledProcessError as error:
            print_command_error(error.stderr)
            resolution = prompt_error_resolution()

            if resolution == "Edit":
                manual_command = self.console.input(
                    "[grey50][Insert command manually]:[/grey50]\n[deep_sky_blue1]❯_[/deep_sky_blue1] "
                )
                # Run the manual command
                self.run_command(manual_command, is_last)

            elif resolution == "Terminate":
                self.console.print("[grey50]└── Terminating...[/grey50]")
                self.console.print("\n[green bold]Process Terminated.[/green bold]")
                sys.exit(0)
