import logging
from jinja2 import Environment, BaseLoader

from src.llms import LLM

def run_terminal_agent(args):
    """Execute a terminal command with optional permissive settings."""
    if args.careless:
        logging.info(f"Executing terminal command with careless settings: {args.prompt}")
    else:
        logging.info(f"Executing terminal command: {args.prompt}")

PROMPT = open("src/agents/terminal/prompt.jinja2").read().strip()

class Terminal:
    def __init__(self, base_model: str):
        self.llm = LLM(model_id=base_model)

    def render(self, prompt: str) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(prompt=prompt)
    
    def validate_response(self, response: str) -> bool:
        return True
    
    def parse_response(self, response: str):
        # strip response from the string prefix '```bash' and string suffix '```'
        result = response[7:-3]

        return result    

    def execute(self, prompt: str, project_name: str) -> str:
        prompt = self.render(prompt)
        response = self.llm.inference(prompt, project_name)

        print(response)
        # return response
