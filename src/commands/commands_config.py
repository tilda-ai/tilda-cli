from .init import run_init
from .terminal import TerminalRunner


commands = {
    'init': {
        'help': 'Inits the tilda cli in the current directory',
        'function': run_init,
        'args': {'--sync': {'help': 'run the init command in sync mode'}}
    },
    'terminal': {
        'help': 'Execute a specific terminal command',
        'function': TerminalRunner().run_terminal,
        'args': {'prompt': {'help': 'a prompt describing the terminal command to execute'}}
    },
}
