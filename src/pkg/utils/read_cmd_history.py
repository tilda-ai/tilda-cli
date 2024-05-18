import os

from src.lib_pkg.logger import Logger

from .file_system import get_user_home_directory
from .get_user_shell import get_user_shell

logger = Logger().get_logger()

def get_history_file_path():
    home = get_user_home_directory()
    history_files_map = {
        'bash': os.path.join(home, '.bash_history'),
        'zsh': os.path.join(home, '.zsh_history'),
        'fish': os.path.join(home, '.fish_history'),
    }
    user_shell = get_user_shell()
    return history_files_map.get(user_shell)

def read_last_commands(history_file, num_commands=30):
    if not history_file:
        logger.info("Unsupported shell for history retrieval.")
        return "Unsupported shell for history retrieval."

    try:
        with open(history_file, 'r', encoding='utf-8', errors='ignore') as file:
            # Efficiently read only the last 'num_commands' lines
            history = file.readlines()[-num_commands:]
        return history
    except FileNotFoundError:
        logger.error(f"History file not found: {history_file}")
        return "History file not found."
    except Exception as e:
        logger.error("An unexpected error occurred.")
        return f"An error occurred: {str(e)}"

def read_cmd_history():
    history_file = get_history_file_path()
    return read_last_commands(history_file)