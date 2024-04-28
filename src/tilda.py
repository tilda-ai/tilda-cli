#!/usr/bin/env python3

import argparse
import sys

from src.logger import logger
from src.commands import commands


def configure_parser():
    """Configure and return the main argument parser with subparsers for commands."""
    parser = argparse.ArgumentParser(description="The AI CLI")
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--dry', action='store_true', help="Execute the command in dry mode (without model inference).")
    parent_parser.add_argument('--mock', action='store_true', help="Respond with mock data found in .tilda/mock_responses/<COMMAND_NAME>.json")
    
    # Subparser setup
    subparsers = parser.add_subparsers(dest='subcommand', required=True, help='Sub-command help')

    for cmd, cmd_opts in commands.items():
        sub_parser = subparsers.add_parser(cmd, parents=[parent_parser], help=cmd_opts['help'])
        # Add command-specific arguments
        for arg, arg_opts in cmd_opts.get('args', {}).items():
            sub_parser.add_argument(arg, help=arg_opts['help'])

    return parser

def main():
    parser = configure_parser()
    args = parser.parse_args()

    # Call the corresponding function based on the subcommand
    if args.subcommand:
        commands[args.subcommand]['function'](args)
    else:
        logger.error("Unknown command")
        sys.exit(1)
