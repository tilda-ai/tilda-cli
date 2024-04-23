import os
import logging

from src.utils import append_script_to_shell_rc


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
    # Auto-generated by tilda cli: command history configuration
    shopt -s histappend
    PROMPT_COMMAND="history -a; $PROMPT_COMMAND"
    """,
    'zsh': """
    # Auto-generated by tilda cli: command history configuration
    setopt APPEND_HISTORY
    setopt INC_APPEND_HISTORY
    setopt SHARE_HISTORY
    precmd() { history -a }
    """,
    'fish': """
    # Auto-generated by tilda cli: command history configuration
    function save_history --on-event fish_preexec
        history --save
    end
    """,
}

def configure_cmd_real_time_history():
    shell = os.path.basename(os.environ.get('SHELL', ''))
    rt_history_script = shell_rt_history_scripts.get(shell)
    if rt_history_script:
        append_script_to_shell_rc(shell, rt_history_script, user_confirmation_prompt)
    else:
        logging.info(f"No specific configuration available for {shell}. Skipping modifications.")