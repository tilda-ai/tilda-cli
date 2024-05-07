import datetime
import os
from pathlib import Path
import sys
import json

from rich.console import Console

from src.config import Config
from src.common.llm_inference_client import LLMInferenceClient
from src.common import print_error

from src.utils.get_jinja_env import get_jinja_env
from src.utils.get_project_config_files import get_project_config_files
from src.utils.get_project_root import get_project_root_folder_name, get_project_root_path
from src.utils.get_project_tree import get_project_tree
from src.utils.get_reducted_path import get_reducted_path
from src.utils.read_cmd_history import read_cmd_history
from src.utils.write_log_file import write_log_file

from ..types import TerminalCommandArgs

class TerminalAgent:
    def __init__(self):
        self.console = Console()
        self.config = Config()
        self.llm = LLMInferenceClient(model_id=self.config.get_terminal_command_base_model())
        self.template = get_jinja_env().get_template('terminal_command/agent/agent_prompt.jinja2')
        self.tokenizer = self.config.get_terminal_tokenizer()

    def render(self, args: TerminalCommandArgs) -> str:
        rendered_prompt = self.template.render(
            prompt=args.prompt,
            user_os=os.name,
            dev_env_context=self.config.get_dev_env_context(),
            project_tree=get_project_tree(),
            project_config_files=get_project_config_files(),
            working_directory=get_reducted_path(Path.cwd()),
            commands_history=read_cmd_history(),
            project_root_folder_name=get_project_root_folder_name(),
            project_root_path=get_reducted_path(get_project_root_path()),
            current_date=datetime.date.today().strftime('%Y-%m-%d')
        )

        # save the rendered prompt to a file for debugging purposes
        # default destination: {project_root}/.tilda/logs/ directory
        write_log_file('command-terminal-prompt.md', rendered_prompt)

        return rendered_prompt

    def execute(self, args: TerminalCommandArgs) -> str:
        rendered_prompt = self.render(args)
        
        if args.dry:
            self.console.print('[bold]Dry-run mode enabled, no inference made.[/bold]')
            sys.exit(0)
        
        with self.console.status("[bold green]Processing...[/bold green]", spinner="dots"):
            response = self.llm.inference(rendered_prompt, self.tokenizer)

        try:
            json_response = json.loads(response)
            return json_response
        except json.JSONDecodeError as error:
            print_error(
                error,
                "[red]Error parsing agent response to json, [underline]please try again or check your arguments.[/underline][/red]",
                "src/commands/terminal/agent/agent.py",
                "TerminalAgent.execute",
                custom_output=f"response: {response}",
                cli_args=args,
            )
            sys.exit(1)
