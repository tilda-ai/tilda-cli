from .runner import TerminalCommandRunner
from .types import TerminalCommandArgs

def run_terminal_command(args: TerminalCommandArgs):
    """
    Run the terminal command with the given args.

    :param args: The terminal command arguments.
    """
    TerminalCommandRunner().run(args)