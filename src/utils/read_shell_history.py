import os
import platform

#TODO: fix get os type
#TODO: remove main function call

def get_os_type():
    return platform.system().lower()  # 'linux', 'darwin' (macOS), 'windows'

def get_history_file():
    os_type = get_os_type()
    home = os.path.expanduser('~')

    # Default to Bash for Unix-like systems
    history_files = {
        'linux': {
            'yash': f'{home}/.yash_history',
            'ksh': f'{home}/.ksh_history',
            'bash': f'{home}/.bash_history',
            'zsh': f'{home}/.zsh_history'
            # Add more shells as needed
        },
        'darwin': {
            'yash': f'{home}/.yash_history',
            'ksh': f'{home}/.ksh_history',
            'bash': f'{home}/.bash_history',
            'zsh': f'{home}/.zsh_history'
            # macOS often uses Zsh by default now
        },
        'windows': {
            'powershell': f'{home}/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt'
            # Command Prompt does not store history in a file by default
        }
    }

    shell = os.getenv('SHELL', 'bash').split('/')[-1]  # Default to Bash if SHELL env var is not set
    return history_files.get(os_type, {}).get(shell, None)

def read_shell_command_history():
    history_file = get_history_file()
    if not history_file:
        return "Unsupported shell or OS for history retrieval."

    try:
        # Open the file with UTF-8 encoding and ignore errors
        with open(history_file, 'r', encoding='utf-8', errors='ignore') as file:
            history = file.readlines()
        return history[-10:]  # Last 10 commands
    except FileNotFoundError:
        return "History file not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    last_commands = read_history()
    if isinstance(last_commands, list):
        for command in last_commands:
            print(command.strip())
    else:
        print(last_commands)

if __name__ == "__main__":
    main()