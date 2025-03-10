import os
import sys

from rich.console import Console

console = Console()

def touch_command(args):
    if len(args) != 1:
        console.print("[bold red]Usage:[/bold red] touch <filename>")
        return

    filename = args[0]

    if os.path.exists(filename):
        console.print(f"[bold yellow]Warning:[/bold yellow] '{filename}' already exists.")
    else:
        try:
            with open(filename, 'w'):
                pass
            console.print(f"[bold green]Created:[/bold green] {filename}")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            
if __name__ == "__main__":
    touch_command(sys.argv[1:])