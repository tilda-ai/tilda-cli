import os

from src.lib.logger import Logger

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

def read_last_commands(history_file, num_commands=15):
    if not history_file:
        logger.info("Unsupported shell for history retrieval.")
        return "Unsupported shell for history retrieval."
    
    try:
        with open(history_file, 'r', encoding='utf-8', errors='ignore') as file:
            # Read all lines from the file
            all_lines = file.readlines()
            
            # Ensure num_commands is not greater than the number of lines in the file
            if num_commands > len(all_lines):
                logger.info(f"Requested number of commands ({num_commands}) is greater than available lines in history file ({len(all_lines)}). Returning all available lines.")
                num_commands = len(all_lines)
            
            # Extract the last 'num_commands' lines
            history = all_lines[-num_commands:]
            
            # Clean history lines from prefix pattern ': XXXXXXXXXX:0;'
            history = [line.split(';', 1)[1] for line in history if ';' in line]
        
        return history
    except FileNotFoundError:
        logger.error(f"History file not found: {history_file}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred. {str(e)}")
        return None

def read_cmd_history():
    history_file = get_history_file_path()
    return read_last_commands(history_file)