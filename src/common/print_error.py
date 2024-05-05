from rich.panel import Panel
from rich.console import Console

console = Console()

def print_error(error, message, file, operation, custom_output=None, cli_args=None):
    """Print error message in a panel."""
    text = (
        f"{message}\n\n"
        f"[grey58]File: `{file}`\n"
        f"Operation: `{operation}`\n"
        f"Error: {error}"
        f"{f'\n{custom_output}' if custom_output else ''}"
        f"{f'\n{cli_args}' if cli_args else ''}[/grey58]\n\n"
        # f"{args}[/grey58]\n\n"
        "If this issue persists, stop by our discord channel or open an issue on github."
    )
    panel = Panel(text, title="[bold red]Error[/bold red]", padding=(1, 2), expand=False, title_align="left")
    console.print(panel)