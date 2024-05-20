import datetime
import json
import os
from pathlib import Path
import sys

from rich.console import Console
from rich.panel import Panel

from src.config import Config
from src.lib.llm_client.client import LLMClient

from src.lib.utils.get_jinja_env import get_jinja_env
from src.lib.utils.get_project_config_files import get_project_config_files
from src.lib.utils.get_project_root import (
    get_project_root_folder_name,
    get_project_root_path,
)
from src.lib.utils.get_project_tree import get_project_tree
from src.lib.utils.get_reducted_path import get_reducted_path
from src.lib.utils.get_shell_history import read_cmd_history
from src.lib.utils.write_log_file import write_log_file

from ..types import TerminalCommandArgs
from .tools.get_project_file_contents_tool import get_project_file_contents_tool
from .tools.terminal_command_tools_mapping import terminal_command_tools_mapping
from .templates.examples import examples


class TerminalAgent:
    def __init__(self):
        self.console = Console()
        self.config = Config()
        self.llm = LLMClient(tools_mapping=terminal_command_tools_mapping)
        self.template = get_jinja_env().get_template(
            "terminal_command/agent/templates/system_prompt.jinja2"
        )

    def render_system_prompt(self, args: TerminalCommandArgs) -> str:
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
            current_date=datetime.date.today().strftime("%Y-%m-%d"),
        )

        # save the rendered prompt to a file for debugging purposes
        # default destination: {project_root}/.tilda/logs/ directory
        # TODO: disable if not in dev mode
        write_log_file("command-terminal-system-prompt.md", rendered_prompt)

        return rendered_prompt

    def generate_commands(self, args: TerminalCommandArgs) -> str:
        rendered_system_prompt = self.render_system_prompt(args)

        if args.dry:
            self.console.print("[bold]Dry-run mode enabled, no inference made.[/bold]")
            sys.exit(0)

        inference = self.llm.inference(
            model_id=self.config.get_terminal_command_base_model(),
            messages=[
                {
                    "role": "system",
                    "name": "system_prompt",
                    "content": rendered_system_prompt,
                },
                *examples,
                {
                    "role": "user",
                    "name": "software_developer",
                    "content": args.prompt.strip(),
                },
            ],
            tools=[get_project_file_contents_tool],
        )

        if inference["status"] == "error":
            self.console.print()
            panel = Panel(
                f"{inference["message"]}",
                title="[bold red]Inference Error[/bold red]",
                padding=(1, 2),
                expand=True,
                title_align="left",
                border_style="grey50",
            )
            self.console.print(panel)
            self.console.print()
            sys.exit(1)

        return json.loads(inference["message"]).get("completions")