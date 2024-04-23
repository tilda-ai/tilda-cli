import logging
import os

def configure_cmd_output_logging():
    shell = os.getenv('SHELL', '')
    print(f"Detected shell: {shell}")
    config_file = get_shell_config_file(shell)
    if not config_file:
        print("No shell .rc file detected")
        print("NOTICE: You will need to pass the cmd and error message to the 'tilda solve' command manually using the '--cmd' and '--error' flags.")
        return

    home = os.path.expanduser('~')
    config_path = os.path.join(home, config_file)

    script_content = get_script_content(shell)

    print(f"NOTICE: This will modify your {config_file}.")
    print("Options:")
    print("1: Append logging functionality (can affect shell behavior and performance).")
    print("2: Remove logging functionality (reverts changes made previously).")
    choice = input("Please choose an option (1 / 2): ")

    if choice not in ['1', '2']:
        logging.error("Invalid choice.")
        return

    confirm = input(f"Are you sure you want to proceed with option {choice}? (yes/no): ").lower()
    if confirm != 'yes':
        print("Operation cancelled.")
        return

    try:
        with open(config_path, 'r+') as file:
            contents = file.read()
            update_file(contents, choice, config_file, script_content, file, shell)
    except FileNotFoundError:
        logging.error(f"{config_file} not found. Ensure you are on a system with {shell.split('/')[-1]} installed.")
    except IOError as e:
        logging.error(f"Error accessing file {config_path}: {e}")

def get_shell_config_file(shell):
    shell_type = shell.split('/')[-1]
    shell_map = {
        'bash': '.bashrc', 'zsh': '.zshrc', 'fish': 'config.fish',
        'csh': '.cshrc', 'ksh': '.kshrc', 'tcsh': '.tcshrc',
    }

    config_file = shell_map.get(shell_type, '')
    if not config_file:
        logging.error(f"Unsupported shell type - {shell}. No changes made.")
        print("NOTICE: You will need to pass the cmd and error message to the 'tilda solve' command manually using the '--cmd' and '--error' flags.")
        return None

    return config_file

def get_script_content(shell):
    shell_type = shell.split('/')[-1]
    if shell_type in ['bash', 'zsh', 'ksh']:
        return """
            cleanup_log() {
                if [ -f "$(pwd)/.tilda/cmd_output_temp.txt" ]; then
                    rm "$(pwd)/.tilda/cmd_output_temp.txt"
                    echo "Log file removed."
                fi
            }

            log_command_output() {
                if [ -d "$(pwd)/.tilda" ]; then
                    last_command=$(fc -ln -1)
                    echo "Executing: $last_command" | tee -a "$(pwd)/.tilda/cmd_output_temp.txt"
                fi
            }

            trap 'cleanup_log' EXIT
            trap 'log_command_output' DEBUG
        """
    elif shell_type in ['fish']:
        return """
            function cleanup_log --on-event=exit
                if test -f (pwd)/.tilda/cmd_output_temp.txt
                    rm (pwd)/.tilda/cmd_output_temp.txt
                    echo "Log file removed."
                end
            end

            function log_command_output --on-event=preexec
                if test -d (pwd)/.tilda
                    set last_command (history | tail -1)
                    echo "Executing: $last_command" | tee -a (pwd)/.tilda/cmd_output_temp.txt
                end
            end
        """
    elif shell_type in ['csh', 'tcsh']:
        return """
            alias precmd 'if (-d (pwd)/.tilda) then; set last_command=`history -h 1`; echo "Executing: $last_command" | tee -a (pwd)/.tilda/cmd_output_temp.txt; endif'
            alias logout 'if (-f (pwd)/.tilda/cmd_output_temp.txt) then; rm (pwd)/.tilda/cmd_output_temp.txt; echo "Log file removed."; endif'
        """
    return ""

def update_file(contents, choice, config_file, script_content, file, shell):
    if choice == '1':
        append_cmd_logging(contents, config_file, script_content, file)
    elif choice == '2':
        remove_cmd_logging(contents, config_file, script_content, file)

def append_cmd_logging(contents, config_file, script_content, file):
    if 'cleanup_log' in contents and 'log_command_output' in contents:
        logging.info(f"Logging and cleanup are already configured in {config_file}.")
    else:
        file.write(script_content)
        logging.info(f"Logging and cleanup functionality appended to {config_file}. Please restart your terminal.")

def remove_cmd_logging(contents, config_file, script_content, file):
    if 'cleanup_log' in contents and 'log_command_output' in contents:
        contents = contents.replace(script_content, '')
        file.seek(0)
        file.truncate()
        file.write(contents)
        logging.info(f"Logging and cleanup functionality removed from {config_file}. Please restart your terminal.")
    else:
        logging.info(f"No logging functionality found in {config_file}. No changes needed.")
