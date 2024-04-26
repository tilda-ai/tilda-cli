import datetime
from pathlib import Path

from ..types import TerminalCommandArgs
from src.config import Config
from src.llms import LLM
from src.utils import get_jinja_env, get_project_root_path


class TerminalAgent:
    def __init__(self):
        self.config = Config()
        self.llm = LLM(model_id=self.config.get_terminal_command_base_model())
        self.template = get_jinja_env().get_template('terminal/agent/agent_prompt.jinja2')
        self.tokenizer = self.config.get_terminal_tokenizer()

    def render(self, args: TerminalCommandArgs) -> str:
        rendered_prompt = self.template.render(
            prompt=args.prompt, 
            scope=args.scope,
            user_os=self.config.get_user_os(),
            project_tree=self.config.get_project_tree(),
            dev_env_context=self.config.get_dev_env_context(),
            project_config_files=self.config.get_project_config_files(),
            working_directory=self.config.get_working_directory(),
            commands_history=self.config.get_commands_history(),
            project_root='tilda',
            current_date=datetime.date.today().strftime('%Y-%m-%d')
        )

        # save the rendered prompt to a file in the project's root directory
        # in a a folder called .tilda/logs/command-terminal-prompt.md
        # TODO: enable only in debug mode
        # TODO: extract logging to a separate module
        # TODO: extract the logs directory to a config file
        logs_dir = Path(get_project_root_path(Path.cwd())) / '.tilda' / 'logs'
        logs_dir.mkdir(parents=True, exist_ok=True)
        with open(logs_dir / 'command-terminal-prompt.md', 'w', encoding="utf-8") as file:
            file.write(rendered_prompt)

        return rendered_prompt

    def execute(self, args: TerminalCommandArgs) -> str:
        prompt = self.render(args)
        response = self.llm.inference(prompt, self.tokenizer)

        return response
