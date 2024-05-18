import os
from pathlib import Path

from .get_reducted_path import get_reducted_path

def get_project_root_folder_name():
    """
    Traverse up from the current directory until the 'tildaconfig.toml' file is found,
    indicating the project root directory.
    
    :return: The path to the project root directory or None if not found.
    """
    current_dir = Path.cwd()

    while True:
        # Check if 'tildaconfig.toml' exists in the current directory
        if 'tildaconfig.toml' in os.listdir(current_dir):
            # Return the name of the directory
            return os.path.basename(current_dir)
        # Move up one directory level
        parent_dir = os.path.dirname(current_dir)
        
        # If we are at the root of the filesystem, stop searching
        if parent_dir == current_dir:
            return None
        
        # Update the current directory to the parent directory
        current_dir = parent_dir

def get_project_root_path() -> Path:
    """
    Traverse up from the current directory until the 'tildaconfig.toml' file is found,
    indicating the project root directory.
    
    :param current_dir: The starting directory, typically the directory where the script is run.
    :return: The path to the project root directory or None if not found.
    """
    current_dir = Path.cwd()

    while True:
        # Check if 'tildaconfig.toml' exists in the current directory
        if 'tildaconfig.toml' in os.listdir(current_dir):
            return current_dir
        # Move up one directory level
        parent_dir = os.path.dirname(current_dir)
        
        # If we are at the root of the filesystem, stop searching
        if parent_dir == current_dir:
            return None
        
        # Update the current directory to the parent directory
        current_dir = parent_dir
