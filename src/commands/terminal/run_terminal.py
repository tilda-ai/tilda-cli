# src/commands/run_terminal.py
from src.logger import logger
from .agent import TerminalAgent
from .types import TerminalCommandArgs


def run_terminal(args: TerminalCommandArgs):
    logger.info("Running tilda terminal agent...")

    # print args
    logger.debug("args: %s", args)

    terminal_agent = TerminalAgent()
    response = terminal_agent.execute(args)

    #TODO: return the response to the user and let him choose to run in with enter key
    # return response

    print(response)

    pass
    