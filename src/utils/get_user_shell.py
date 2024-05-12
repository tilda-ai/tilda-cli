import os
import subprocess

from src.common.logger import Logger

logger = Logger().get_logger()

def get_shell_from_env():
    """Get shell from the SHELL environment variable."""
    shell_path = os.environ.get('SHELL')
    if shell_path:
        return os.path.basename(shell_path)
    return None

def detect_shell():
    """Detect the shell by examining the current process."""
    try:
        # This command attempts to get the command line for the current process
        # Adjust the command according to your system and needs
        result = subprocess.check_output('ps -p $$ -oargs=', shell=True, text=True)
        return result.strip().split()[0]  # Split and return the first part to avoid extra args
    except Exception as e:
        logger.error(f"Error detecting shell: {e}")
        return None

def get_user_shell():
    """Determine the shell using environment variables or fallback to detection."""
    shell_name = get_shell_from_env()
    if shell_name:
        return shell_name
    else:
        # If the SHELL environment variable is not set, fall back to detection
        shell_name = detect_shell()
        if shell_name:
            return shell_name
        else:
            # Final fallback if no method works
            return ''
