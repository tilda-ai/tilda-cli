import subprocess

def get_command_history(n: str = '10'):
    # Using subprocess to execute the `history` command and capture the output
    result = subprocess.run(['history', n], shell=True, text=True, capture_output=True)
    if result.stdout:
        return result.stdout.strip().split('\n')
    else:
        return []