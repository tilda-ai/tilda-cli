# src/commands/commands.py

from src.commands import run_init, run_terminal

commands = {
    'terminal': {
        'help': 'Execute a specific terminal command',
        'function': run_terminal,
        'args': {'prompt': {'help': 'a prompt describing the terminal command to execute'}}
    },
    'init': {
        'help': 'Inits the tilda cli in your project directory',
        'function': run_init,
        'args': {'prompt': {'help': 'a prompt describing the terminal command to execute'}}
    }
}