from rich.panel import Panel
from rich.console import Console

console = Console()

def print_command_error(error):
    title="[red bold]Error:[/red bold]"
    text = (
        f"{error.strip()}"
    )
    subtitle = "[bold]shell[/bold]"
    panel = Panel(
        text,
        title=title,
        padding=(1, 2),
        expand=True,
        title_align="left",
        subtitle=subtitle,
        subtitle_align="right",
        border_style="grey50",
    )
    console.print(panel)
