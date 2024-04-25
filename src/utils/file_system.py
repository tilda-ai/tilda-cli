from fnmatch import fnmatch
import logging
import os
import shutil

def get_user_home_directory():
    return os.path.expanduser('~')

def append_to_file(filename, entry):
    if os.path.exists(filename):
        with open(filename, 'r+', encoding="utf-8") as file:
            content = file.read()
            if entry in content:
                logging.info(f"{entry} is already listed in {filename}.")
            else:
                file.write(f"\n\n{entry}")
                logging.info(f"{entry} added to {filename} successfully.")
    else:
        logging.info(f"Could not find {filename}.")

def backup_file(file_path):
    """ Create a backup of the file if it doesn't already exist. """
    backup_path = f"{file_path}.backup"
    try:
        if not os.path.exists(backup_path):
            shutil.copyfile(file_path, backup_path)
            logging.info(f"Backup created at {backup_path}")
        else:
            logging.info(f"Backup already exists at {backup_path}")
    except IOError as e:
        logging.error(f"Failed to create backup: {e}")

def restore_file_from_backup(file_path):
    """ Restore a file from its backup if available. """
    backup_path = f"{file_path}.backup"
    try:
        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, file_path)
            logging.info(f"Restored from backup at {backup_path}")
        else:
            logging.info(f"No backup found at {backup_path}")
    except IOError as e:
        logging.error(f"Failed to restore backup: {e}")

def is_in_file(filename, entry):
    if os.path.exists(filename):
        with open(filename, 'r', encoding="utf-8") as file:
            content = file.read()
            if entry in content:
                return True
            else:
                # break the content into a list of lines
                content = content.split("\n")
                # check if the entry matches the line utilize shell-style wildcard matching
                # TODO: match case is too loose, if there's a line with src, the entire src will be matched and ignored in later scripts
                for line in content:
                    if line:
                        if fnmatch(entry.strip('/'), line.strip('/')):
                            return True
                return False
    else:
        return False