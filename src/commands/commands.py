from .init_command.runner import InitCommandRunner
from .terminal_command.runner import TerminalCommandRunner

commands = {
    'init': {
        'help': 'Inits the tilda cli in the current directory',
        'function': InitCommandRunner().run,
        'args': {'--sync': {'help': 'run the init command in sync mode'}}
    },
    'terminal': {
        'help': 'Execute a specific terminal command',
        'function': TerminalCommandRunner().run,
        'args': {'prompt': {'help': 'a prompt describing the terminal command to execute'}}
    },
}
