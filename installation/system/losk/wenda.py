import subprocess
import os
from rich.console import Console
from rich.prompt import Confirm

console = Console()

def wenda_command():
    """
    اجرای Wenda Converter در PyDOS
    """
    wenda_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'application', 'wendaconverter.py'))
    
    if os.path.exists(wenda_path):
        confirm = Confirm.ask("Do you want to run Wenda Converter?")
        if confirm:
            console.print("[bold cyan]Running Wenda Converter...[/bold cyan]")
            try:
                subprocess.run(['python3', wenda_path], check=True)
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]Error executing Wenda Converter:[/bold red] {e}")
        else:
            console.print("[bold yellow]Execution cancelled.[/bold yellow]")
    else:
        console.print(f"[bold red]Error:[/bold red] File not found: {wenda_path}")

if __name__ == "__main__":
    wenda_command()