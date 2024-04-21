import os

def configure_command_output_logging():
    home = os.path.expanduser('~')
    bashrc_path = os.path.join(home, '.bashrc')
    script_content = """
# Conditionally log every command's output if .tilda directory exists and cleanup on exit
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

    # Ensure the script isn't already in .bashrc
    try:
        with open(bashrc_path, 'r+') as file:
            contents = file.read()
            if 'cleanup_log' in contents and 'log_command_output' in contents:
                print("Logging and cleanup are already configured in .bashrc.")
            else:
                file.write(script_content)
                print("Logging and cleanup functionality appended to .bashrc. Please restart your terminal.")
    except FileNotFoundError:
        print(".bashrc not found. Ensure you are on a system with Bash installed.")
