import datetime
import os
from pathlib import Path

from src.config import Config
from src.llms import LLM
from src.utils import get_jinja_env, get_project_config_files, get_project_root_path, get_project_root_folder_name, get_reducted_path, read_cmd_history, get_project_tree
from ..types import TerminalCommandArgs


class TerminalAgent:
    def __init__(self):
        self.config = Config()
        self.llm = LLM(model_id=self.config.get_terminal_command_base_model())
        self.template = get_jinja_env().get_template('terminal/agent/agent_prompt.jinja2')
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

        # save the rendered prompt to a file in the project's root directory
        # in a a folder called .tilda/logs/command-terminal-prompt.md
        # TODO: enable only in debug mode
        # TODO: extract logging to a separate module
        # TODO: extract the logs directory to a config file
        logs_dir = Path(get_project_root_path()) / '.tilda' / 'logs'
        logs_dir.mkdir(parents=True, exist_ok=True)
        with open(logs_dir / 'command-terminal-prompt.md', 'w', encoding="utf-8") as file:
            file.write(rendered_prompt)

        return rendered_prompt

    def execute(self, args: TerminalCommandArgs) -> str:
        rendered_prompt = self.render(args)
        
        if args.dry:
            return 'No inference made. Dry run mode.'
        
        response = self.llm.inference(rendered_prompt, self.tokenizer)

        return response
