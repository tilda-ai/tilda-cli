from jinja2 import Environment, BaseLoader

from src.agents.terminal.types import TerminalCommandArgs
from src.config.config import Config
from src.llms import LLM

PROMPT = open("src/agents/terminal/prompt.jinja2").read().strip()

class Terminal:
    def __init__(self):
        config = Config()
        self.base_model = config.get_terminal_base_model()
        self.tokenizer = config.get_terminal_tokenizer()
        self.llm = LLM(model_id=self.base_model)

    def render(self, args: TerminalCommandArgs) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(prompt=args.prompt, scope=args.scope)

    def execute(self, args: TerminalCommandArgs) -> str:
        prompt = self.render(args)
        response = self.llm.inference(prompt, self.tokenizer)

        return response