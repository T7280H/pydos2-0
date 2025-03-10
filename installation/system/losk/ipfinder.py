import subprocess
import os
import sys
from rich.console import Console

console = Console()

def ipfinder_command():
    # مسیر فایل IP FINDER
    ip_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'application', 'IPFINDER.py'))
    
    if os.path.exists(ip_path):
        try:
            console.print("[bold cyan]Running IP Finder...[/bold cyan]")
            subprocess.run(['python3', ip_path], check=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error executing IP Finder:[/bold red] {e}")
            sys.exit(1)
    else:
        console.print(f"[bold red]Error:[/bold red] File not found: {ip_path}")
        sys.exit(1)

if __name__ == "__main__":
    ipfinder_command()