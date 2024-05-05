import subprocess
import json
import time
import sys

from rich.console import Console

from src.logger import logger
from src.config import Config
from src.common import SingletonMeta
from .agent import TerminalAgent
from .types import TerminalCommandArgs
from .tui import print_command, prompt_command_action, prompt_error_resolution, print_command_output, print_command_error

class TerminalRunner(metaclass=SingletonMeta):
    def __init__(self):
        self.console = Console()
        self.config = Config()

    def run_terminal(self, args: TerminalCommandArgs):
        logger.info("[run_terminal]: Running tilda terminal agent with args %s", args)

        if args.dry:
            self.console.print('[bold]Dry-run mode enabled, no inference made.[/bold]')
            return

        if args.mock:
            with self.console.status("[bold green]Processing...[/bold green]", spinner="dots"):
                time.sleep(1)
                commands = json.loads(self.config.get_terminal_command_mock_response())
        else:
            # execute terminal agent inference to generate commands
            with self.console.status("[bold green]Processing...[/bold green]", spinner="dots"):
                commands = TerminalAgent().execute(args)

        self.render_commands(commands)

    def render_commands(self, commands):
        for command in sorted(commands, key=lambda x: x['executionOrder']):
            self.console.print()
            print_command(command, len(commands))
            action = prompt_command_action()

            if action == 'Run':
                self.run_command(command['shellScript'], is_last=command['executionOrder'] == len(commands))
                
            if action == 'Edit':
                self.console.print("[grey50]└── Command edit feature not yet implemented.[/grey50]")
                continue
            
            if action == 'Explain':
                self.console.print("[grey50]└── Command explain feature not yet implemented.[/grey50]")
                continue
                
            if action == 'Skip':
                self.console.print("[grey50]└── Command skipped.[/grey50]")
                continue

            if action == 'Terminate':
                self.console.print("[grey50]└── Terminating...[/grey50]")
                self.console.print("\n[green bold]Process Terminated.[/green bold]")
                sys.exit(1)

    def run_command(self, command, is_last=False):
        try:
            with self.console.status("[grey50]Running...[/grey50]", spinner="dots", spinner_style="grey50"):
                time.sleep(1)
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

            if result.stdout:
                print_command_output(output=result.stdout)
            else:
                self.console.print("[grey50]└── No output returned.[/grey50]")

        except subprocess.CalledProcessError as error:
            print_command_error(error.stderr)
            resolution = prompt_error_resolution()
            
            if resolution == 'Edit':
                manual_command = self.console.input("[grey50][Insert command manually]:[/grey50]\n[deep_sky_blue1]❯_[/deep_sky_blue1] ")
                # Run the manual command
                self.run_command(manual_command, is_last)
            
            if resolution == 'Skip':
                self.console.print("[grey50]└── Resolution skipped.[/grey50]")
                # if is_last:
                #     self.console.print("\n[green bold]Process Completed.[/green bold]")
                return
                
            elif resolution == 'Terminate':
                self.console.print("\n[green bold]Process Terminated.[/green bold]")
                sys.exit(1)
