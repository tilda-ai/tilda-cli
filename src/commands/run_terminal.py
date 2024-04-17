import logging

from src.agents import terminal

def run_terminal(args):
    logging.info(f"Running tilda terminal agent with prompt: {args.prompt} | scope: {args.scope}")
    response = terminal.execute(args.prompt, args)

    #TODO: return the response to the user and let him choose to run in with enter key
    print(response)
    