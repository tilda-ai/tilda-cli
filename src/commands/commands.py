# Define command configurations in a structured way for extensibility
from .run_terminal import run_terminal

commands = {
    'terminal': {
        'help': 'Execute a specific terminal command',
        'function': run_terminal,
        'args': {'prompt': {'help': 'a prompt describing the terminal command to execute'}}
    }
}