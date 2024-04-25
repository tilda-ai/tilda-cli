# src/commands/commands.py

from src.commands.init import run_init
from src.commands.terminal import run_terminal

commands = {
    'init': {
        'help': 'Inits the tilda cli in the current directory',
        'function': run_init,
        'args': {'--sync': {'help': 'run the init command in sync mode'}}
    },
    'terminal': {
        'help': 'Execute a specific terminal command',
        'function': run_terminal,
        'args': {'prompt': {'help': 'a prompt describing the terminal command to execute'}}
    },
}