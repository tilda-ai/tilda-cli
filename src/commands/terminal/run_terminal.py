# src/commands/run_terminal.py
import logging

from .agent import TerminalAgent
from .types import TerminalCommandArgs


def run_terminal(args: TerminalCommandArgs):
    logging.info(f"Running tilda terminal agent...")

    # print args
    logging.debug(f"args: {args}")

    terminal_agent = TerminalAgent()
    response = terminal_agent.execute(args)

    #TODO: return the response to the user and let him choose to run in with enter key
    # return response

    pass
    