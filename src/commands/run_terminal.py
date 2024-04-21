# src/commands/run_terminal.py

import logging

from src.agents import TerminalAgent, TerminalCommandArgs

def run_terminal(args: TerminalCommandArgs):
    logging.info(f"Running tilda terminal agent with prompt: {args.prompt} | scope: {args.scope}")

    terminal_agent = TerminalAgent()
    response = terminal_agent.execute(args)

    #TODO: return the response to the user and let him choose to run in with enter key
    print(response)
    