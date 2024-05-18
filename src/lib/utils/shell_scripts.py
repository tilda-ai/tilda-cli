import os
from subprocess import CalledProcessError, call

from src.lib.logger import Logger

from .file_system import backup_file, restore_file_from_backup, get_user_home_directory
from .user_interactions import user_confirmation

logger = Logger().get_logger()

def validate_shell_script(shell_path, shell):
    """ Validate the shell script using the specified shell. """
    command = f"{shell} -n {shell_path}"
    try:
        return_code = call(command, shell=True)
        return return_code == 0
    except CalledProcessError as e:
        logger.error(f"Shell script validation failed: {e}")
        return False

def append_script_to_shell_rc(shell, script, user_confirmation_prompt):
    """ Append a script to the shell's rc file after user confirmation. """
    home = get_user_home_directory()
    shell_rc_path = os.path.join(home, f".{shell}rc")
    if not os.path.exists(shell_rc_path):
        logger.warning(f"{shell}rc does not exist; skipping modifications.")
        return

    logger.info(f"Ready to modify {shell}rc with new settings.")
    if not user_confirmation(user_confirmation_prompt):
        logger.info("Changes canceled by user.")
        return

    backup_file(shell_rc_path)
    try:
        with open(shell_rc_path, 'r+', encoding="utf-8") as file:
            content = file.read()
            if script.strip() in content:
                logger.info(f"Changes are already applied in {shell}rc")
                return
            file.write(script)
            logger.info(f"Changes were appended to {shell}rc")
    except IOError as e:
        logger.error(f"Failed to modify {shell}rc: {e}")
        restore_file_from_backup(shell_rc_path)

    if not validate_shell_script(shell_rc_path, shell):
        logger.error(f"Error: {shell}rc has syntax errors after appending rt_history_script.")
        logger.info("Restoring from backup...")
        restore_file_from_backup(shell_rc_path)
