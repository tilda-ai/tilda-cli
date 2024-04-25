import os
import logging

from src.utils import append_script_to_shell_rc, get_user_shell

# Define user confirmation prompt
user_confirmation_prompt = """
    The ~tilda CLI tool improves command suggestions by analyzing your most recent commands. To enable this:
    - It will update shell settings to save your command history in real time.
    - This has minimal impact on system performance.
    - A backup of your current settings will be created before rt_history_script.

    Do you want to proceed with these updates? (yes/no): 
"""

# Define shell-specific rt_history_script
shell_rt_history_scripts = {
    'bash': """
    
# Auto-generated by `~tilda` cli: real-time command history
# Function to check if the command is 'tilda' or starts with 'tilda'
function check_command_and_save_history {
    # Use 'history 1' to get the last command entered
    local last_command=$(history 1)
    last_command=${last_command#*[0-9]*  }  # Remove the leading numbers from the history command output

    # Check if the last command starts with 'tilda'
    if [[ "$last_command" == tilda* ]]; then
        history -a >/dev/null 2>&1
    fi
}

# Append this function to PROMPT_COMMAND with a safeguard to not add it multiple times
if [[ ":$PROMPT_COMMAND:" != *":check_command_and_save_history:"* ]]; then
    PROMPT_COMMAND="check_command_and_save_history; $PROMPT_COMMAND"
fi

    """,
    'zsh': """

# Auto-generated by `~tilda` cli: real-time command history
# Function to check if the command is 'tilda' or starts with 'tilda'
function check_command_and_save_history {
    # Use $1, the first argument to this function, to check the command
    if [[ $1 == tilda* ]]; then
        history -a >/dev/null 2>&1
    fi
}

# Use the 'preexec' hook in Zsh, which provides the command string as an argument
autoload -Uz add-zsh-hook
add-zsh-hook preexec check_command_and_save_history

    """,
    'fish': """

# Auto-generated by `~tilda` cli: real-time command history
function save_history --on-event fish_preexec
    # Extract the first word of the command to see if it's 'tilda'
    set -l command (string split " " -- $argv[1] | string trim)
    if [ "$command[1]" = "tilda" ]
        history --save
    end
end

    """,
}

def configure_cmd_real_time_history():
    shell = get_user_shell()
    rt_history_script = shell_rt_history_scripts.get(shell)
    if rt_history_script:
        append_script_to_shell_rc(shell, rt_history_script, user_confirmation_prompt)
    else:
        logging.info(f"No specific configuration available for {shell}. Skipping modifications.")
