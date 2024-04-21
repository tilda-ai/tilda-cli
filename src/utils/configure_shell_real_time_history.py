import os
import shutil

def create_backup(file_path):
    # Create a backup of the file
    backup_path = f"{file_path}.backup"
    if not os.path.exists(backup_path):  # Only create a backup if it doesn't already exist
        shutil.copyfile(file_path, backup_path)
        print(f"Backup created at {backup_path}")
    else:
        print(f"Backup already exists at {backup_path}")

def validate_shell_script(shell_path):
    # Validate the shell script using the shell itself
    if 'bash' in shell_path:
        command = f"bash -n {shell_path}"
    elif 'zsh' in shell_path:
        command = f"zsh -n {shell_path}"
    else:
        return True  # If not bash or zsh, skip validation

    return_code = os.system(command)
    return return_code == 0  # Returns True if validation succeeds

def user_confirmation():
    changes_description = """
        This CLI tool improves command suggestions by analyzing your most recent commands. To enable this:
        - It will update shell settings to save your command history in real time.
        - This has minimal impact on system performance.
        - A backup of your current settings will be created before changes.

        Do you want to proceed with these updates? (yes/no): 
    """
    response = input(changes_description).lower()
    return response in ["yes", "y"]

def append_to_shell_rc(shell, changes):
    home = os.path.expanduser('~')
    shell_rc_path = os.path.join(home, f".{shell}rc")

    if not os.path.exists(shell_rc_path):
        print(f"{shell}rc does not exist; skipping modifications.")
        return

    # Ask for user confirmation before proceeding
    print(f"Ready to modify {shell}rc with new settings.")
    if not user_confirmation():
        print("Changes canceled by user.")
        return

    create_backup(shell_rc_path)

    with open(shell_rc_path, 'r+') as file:
        content = file.read()
        if changes.strip() in content:
            print(f"Changes are already applied in {shell}rc")
            return

        file.write(changes)
        print(f"Changes were appended to {shell}rc")

    if validate_shell_script(shell_rc_path):
        print(f"{shell}rc is valid after appending changes.")
    else:
        print(f"Error: {shell}rc has syntax errors after appending changes.")

# Define the changes for Bash and Zsh
changes = """
# Auto-generated: command history configuration
shopt -s histappend
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"
"""

# Bash-specific changes
bash_changes = changes + """
# Additional Bash-specific configuration if necessary
"""

# Zsh-specific changes
zsh_changes = changes + """
# Additional Zsh-specific configuration if necessary
setopt INC_APPEND_HISTORY
"""

# Apply changes
def configure_shell_history():
    append_to_shell_rc("bash", bash_changes)
    append_to_shell_rc("zsh", zsh_changes)
