from pathlib import Path

from ..types import TerminalCommandArgs
from src import config
from src.llms import LLM
from src.utils import get_jinja_env


class TerminalAgent:
    def __init__(self):
        self.llm = LLM(model_id=config.get_terminal_command_base_model())
        self.template = get_jinja_env().get_template('terminal/agent/agent_prompt.jinja2')
        self.tokenizer = config.get_terminal_tokenizer()

    def render(self, args: TerminalCommandArgs) -> str:
        return self.template.render(
            prompt=args.prompt, 
            scope=args.scope,
            user_os=config.get_user_os(),
            project_tree=config.get_project_tree(),
            dev_env_context=config.get_dev_env_context(),
            project_config_files=config.get_project_config_files(),
            working_directory=config.get_working_directory(),
            commands_history=config.get_commands_history(),
        )

    def execute(self, args: TerminalCommandArgs) -> str:
        prompt = self.render(args)
        # response = self.llm.inference(prompt, self.tokenizer)

        # return response
        return prompt