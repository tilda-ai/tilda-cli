import os

def get_project_root_path(current_dir):
    """
    Traverse up from the current directory until the 'tildaconfig.toml' file is found,
    indicating the project root directory.
    
    :param current_dir: The starting directory, typically the directory where the script is run.
    :return: The path to the project root directory or None if not found.
    """
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

# if __name__ == "__main__":
#     # Start searching from the current working directory
#     current_working_directory = os.getcwd()
#     root_directory = get_project_root_path(current_working_directory)
    
#     if root_directory:
#         print(f"Project root found at: {root_directory}")
#     else:
#         print("Project root not found.")