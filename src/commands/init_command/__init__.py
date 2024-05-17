from .runner import InitCommandRunner
from .types import InitCommandArgs

def run_init_command(args: InitCommandArgs):
    """
    Run the init command with the given args.

    :param args: The init command arguments.
    """
    InitCommandRunner().run(args)