import os
from rich.console import Console

console = Console()

def mkdir_command(directory_name):
    """
    ایجاد یک دایرکتوری جدید
    """
    try:
        if os.path.exists(directory_name):
            console.print(f"[bold yellow]Warning:[/bold yellow] Directory '{directory_name}' already exists.")
        else:
            os.makedirs(directory_name)
            console.print(f"[bold green]Directory created:[/bold green] {directory_name}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    dir_name = input("Enter directory name to create: ").strip()
    mkdir_command(dir_name)