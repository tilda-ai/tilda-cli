# Define command configurations in a structured way for extensibility
from src.agents import run_terminal_agent

commands = {
    'terminal': {
        'help': 'Execute a specific terminal command',
        'function': run_terminal_agent,
        'args': {'prompt': {'help': 'a prompt describing the terminal command to execute'}}
    }
}