import subprocess
import os
import sys
from rich.console import Console

console = Console()

def edit_command():
    # مسیر فایل Editor در فولدر apps
    editor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'application', 'editor.py'))
    
    if os.path.exists(editor_path):
        try:
            console.print("[bold cyan]Opening Pydos Editor...[/bold cyan]")
            subprocess.run(['python3', editor_path], check=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error executing Pydos Editor:[/bold red] {e}")
            sys.exit(1)
    else:
        console.print(f"[bold red]Error:[/bold red] File not found: {editor_path}")
        sys.exit(1)

if __name__ == "__main__":
    edit_command()