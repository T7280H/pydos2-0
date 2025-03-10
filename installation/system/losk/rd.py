import os
import shutil
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def rd_command(path):
    """
    حذف فایل یا پوشه با تأییدیه کاربر
    """
    try:
        if not os.path.exists(path):
            console.print(f"[bold red]Error:[/bold red] Path '{path}' does not exist.")
            return

        confirm = Confirm.ask(f"Are you sure you want to delete '{path}'?")
        if not confirm:
            console.print("[bold yellow]Deletion cancelled.[/bold yellow]")
            return

        if os.path.isfile(path):
            os.remove(path)
            console.print(f"[bold green]File '{path}' deleted successfully.[/bold green]")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            console.print(f"[bold green]Directory '{path}' deleted successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS Remove Utility[/bold cyan]")
    path = Prompt.ask("Enter the file or directory to delete").strip()
    rd_command(path)