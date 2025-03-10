import os
from rich.console import Console
from rich.table import Table

console = Console()

def dir_command(path="."):
    try:
        files = os.listdir(path)
        table = Table(title=f"Contents of {os.path.abspath(path)}", show_header=True, header_style="bold cyan")
        table.add_column("Name", style="bold white")
        table.add_column("Type", style="bold yellow")

        for file in files:
            file_path = os.path.join(path, file)
            file_type = "Directory" if os.path.isdir(file_path) else "File"
            table.add_row(file, file_type)

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    dir_command()