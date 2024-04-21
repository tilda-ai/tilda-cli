from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape

from src.agents.terminal.types import TerminalCommandArgs
from src.config.config import Config
from src.llms import LLM
from src.utils import get_tree, get_jinja_env


class TerminalAgent:
    def __init__(self):
        config = Config()
        self.user_os = config.get_user_os()
        self.tree = get_tree(Path.cwd())
        self.base_model = config.get_terminal_base_model()
        self.tokenizer = config.get_terminal_tokenizer()
        self.llm = LLM(model_id=self.base_model)
        self.env = get_jinja_env()
        self.template = self.env.get_template('terminal_agent_prompt.jinja2')

    def render(self, args: TerminalCommandArgs) -> str:
        return self.template.render(prompt=args.prompt, scope=args.scope)

    def execute(self, args: TerminalCommandArgs) -> str:
        prompt = self.render(args)
        # response = self.llm.inference(prompt, self.tokenizer)

        # return response
        return prompt