import os
import sys
from rich.console import Console

console = Console()

def mv_command(args):
    if len(args) != 2:
        console.print("[bold red]Usage:[/bold red] mv <source> <destination>")
        return

    source, destination = args

    if not os.path.exists(source):
        console.print(f"[bold red]Error:[/bold red] '{source}' does not exist.")
        return

    if os.path.isdir(destination): 
        destination = os.path.join(destination, os.path.basename(source))

    try:
        os.rename(source, destination)
        console.print(f"[bold green]Moved/Renamed:[/bold green] {source} -> {destination}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    mv_command(sys.argv[1:])