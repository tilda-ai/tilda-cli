from subprocess import run, PIPE, CalledProcessError

def is_file_in_git(file_path):
    """Check if a file is tracked or untracked in git."""
    try:
        # Check if the file is tracked in git
        run(['git', 'ls-files', '--error-unmatch', file_path], check=True, stdout=PIPE, stderr=PIPE)
        return True
    except CalledProcessError:
        # If the file is not tracked, check if it's an untracked file
        result = run(['git', 'ls-files', '--others', '--exclude-standard', file_path], stdout=PIPE, stderr=PIPE)
        return bool(result.stdout.strip())