import zipfile
import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def unzip_command(zip_file, destination):
    """
    استخراج فایل ZIP در مسیر مشخص‌شده
    """
    try:
        if not os.path.exists(zip_file):
            console.print(f"[bold red]Error:[/bold red] File '{zip_file}' does not exist.")
            return

        if not zipfile.is_zipfile(zip_file):
            console.print(f"[bold red]Error:[/bold red] '{zip_file}' is not a valid ZIP file.")
            return

        with zipfile.ZipFile(zip_file, 'r') as zipf:
            console.print("[bold cyan]Contents of ZIP file:[/bold cyan]")
            for file in zipf.namelist():
                console.print(f" - {file}")
            
            confirm = Prompt.ask("Do you want to extract these files? (Y/N)", default="Y").strip().lower()
            if confirm != "y":
                console.print("[bold yellow]Extraction cancelled.[/bold yellow]")
                return

            os.makedirs(destination, exist_ok=True)  # ایجاد مسیر در صورت نبود آن
            zipf.extractall(destination)
            console.print(f"[bold green]ZIP file '{zip_file}' extracted to '{destination}' successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS ZIP Extractor[/bold cyan]")
    zip_file = Prompt.ask("Enter the zip file path").strip()
    destination = Prompt.ask("Enter the destination directory path").strip()
    unzip_command(zip_file, destination)