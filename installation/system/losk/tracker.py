import subprocess
import os
from rich.console import Console

console = Console()

def tracker_command():
    """
    اجرای IP Tracker در PyDOS
    """
    tracker_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'application', 'iptracker.py'))
    
    if os.path.exists(tracker_path):
        console.print("[bold cyan]Running IP Tracker...[/bold cyan]")
        try:
            subprocess.run(['python3', tracker_path], check=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error executing IP Tracker:[/bold red] {e}")
    else:
        console.print(f"[bold red]Error:[/bold red] File not found: {tracker_path}")

if __name__ == "__main__":
    tracker_command()