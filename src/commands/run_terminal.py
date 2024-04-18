import logging

from src.agents import terminal
from src.agents.terminal.terminal import Terminal
from src.agents.terminal.types import TerminalCommandArgs

def run_terminal(args: TerminalCommandArgs):
    logging.info(f"Running tilda terminal agent with prompt: {args.prompt} | scope: {args.scope}")

    terminal = Terminal()
    response = terminal.execute(args)

    #TODO: return the response to the user and let him choose to run in with enter key
    print(response)
    