import subprocess
import os
from rich.console import Console

console = Console()

def pyrun_command(file_name):
    """
    اجرای فایل پایتونی
    """
    try:
        if not file_name.endswith('.py'):
            console.print("[bold red]Error:[/bold red] Please provide a valid Python file with .py extension.")
            return

        if os.path.exists(file_name):
            console.print(f"[bold cyan]Running:[/bold cyan] {os.path.abspath(file_name)}")
            subprocess.run(['python3', file_name])
        else:
            console.print(f"[bold red]Error:[/bold red] {file_name} not found.")
    
    except Exception as e:
        console.print(f"[bold red]An error occurred while running {file_name}:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS Python Runner[/bold cyan]")
    file_name = input("Enter the name of the Python file to run: ").strip()
    pyrun_command(file_name)