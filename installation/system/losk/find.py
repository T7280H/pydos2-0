import os
from rich.console import Console
from rich.table import Table

console = Console()

def find_command(file_name, path="."):
    found_files = []
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file_name.lower() in file.lower():  # جستجوی فایل‌های مشابه
                found_files.append(os.path.join(root, file))

    if found_files:
        table = Table(title="Search Results", show_header=True, header_style="bold cyan")
        table.add_column("File Path", style="bold yellow")

        for file_path in found_files:
            table.add_row(file_path)

        console.print(table)
    else:
        console.print("[bold red]File not found![/bold red]")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS File Finder[/bold cyan]")
    file_name = input("Enter the file name to search for: ").strip()
    path = input("Enter the directory path to search in (default: current directory): ").strip() or "."

    if not os.path.exists(path):
        console.print("[bold red]Error:[/bold red] Directory does not exist!")
    else:
        find_command(file_name, path)