"""Function to get the reducted path of a file or directory."""
import os
from pathlib import Path

def get_reducted_path(path: Path) -> Path:
    """Get the reducted path of a file or directory."""
    # Get the user's home directory
    home = os.path.expanduser('~')
    
    # Convert path to string for manipulation
    path_str = str(path)
    
    # Replace the home directory path in path with '~'
    if path_str.startswith(home):
        return Path(path_str.replace(home, '~'))

    return path