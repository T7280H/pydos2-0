import shutil
import os
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def xcopy_command(source, destination):
    """
    کپی فایل یا پوشه به مقصد مشخص‌شده
    """
    try:
        if not os.path.exists(source):
            console.print(f"[bold red]Error:[/bold red] The source '{source}' does not exist.")
            return

        if os.path.exists(destination):
            console.print(f"[bold yellow]Warning:[/bold yellow] Destination '{destination}' already exists.")
            confirm = Confirm.ask("Do you want to overwrite it?")
            if not confirm:
                console.print("[bold yellow]Copy cancelled.[/bold yellow]")
                return

        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
            console.print(f"[bold green]Directory '{source}' copied to '{destination}' successfully.[/bold green]")
        elif os.path.isfile(source):
            shutil.copy2(source, destination)
            console.print(f"[bold green]File '{source}' copied to '{destination}' successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS XCOPY Utility[/bold cyan]")
    source = Prompt.ask("Enter the source file/directory path").strip()
    destination = Prompt.ask("Enter the destination path").strip()
    xcopy_command(source, destination)