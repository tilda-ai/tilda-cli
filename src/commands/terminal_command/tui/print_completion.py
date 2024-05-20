from rich.panel import Panel
from rich.console import Console

console = Console()

def print_completion(command, commands_count):
    if command["responseType"] == "error":
        title = "Could not generate command"
        text = f"[deep_sky_blue1]❯_[/deep_sky_blue1] {command['errorMessage']}"
        subtitle = "[bold green]~tilda[/bold green]"
    else:
        title = f"Generated command [bold][{command['executionOrder']}/{commands_count}][/bold]"
        text = f"[deep_sky_blue1]❯_[/deep_sky_blue1] [bright_white bold]{command['shellScript']}[/bright_white bold]"
        subtitle = "[bold green]~tilda[/bold green]"

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
