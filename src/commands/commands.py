from .init_command import run_init_command
from .terminal_command import run_terminal_command

commands = {
    'init': {
        'help': 'Inits the tilda cli in the current directory',
        'function': run_init_command,
        'args': {'--skip-auto-config': {'help': 'run the init command in sync mode', 'action': 'store_true'}}
    },
    'terminal': {
        'help': 'Execute a specific terminal command',
        'function': run_terminal_command,
        'args': {'prompt': {'help': 'a prompt describing the terminal command to execute'}}
    },
}
