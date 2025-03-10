import os
from rich.console import Console

console = Console()

def defpath_command():
    """
    نمایش مسیر فعلی کاربر در سیستم
    """
    try:
        current_location = os.getcwd()
        console.print(f"[bold cyan]Current Path:[/bold cyan] {current_location}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    defpath_command()