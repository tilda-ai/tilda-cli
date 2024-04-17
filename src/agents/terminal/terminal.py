import logging
from jinja2 import Environment, BaseLoader

from src.llms import LLM

PROMPT = open("src/agents/terminal/prompt.j2").read().strip()

class Terminal:
    def __init__(self, base_model: str):
        self.llm = LLM(model_id=base_model)

    def render(self, prompt: str, args) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(prompt=prompt, args=args)

    def execute(self, prompt: str, args) -> str:
        prompt = self.render(prompt, args)
        response = self.llm.inference(prompt)

        return response