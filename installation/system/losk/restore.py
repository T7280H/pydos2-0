import shutil
import os
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def restore_command(backup_path, restore_path):
    """
    بازگردانی فایل یا پوشه از بکاپ به مسیر مشخص‌شده
    """
    try:
        if not os.path.exists(backup_path):
            console.print(f"[bold red]Error:[/bold red] The backup source '{backup_path}' does not exist.")
            return

        if os.path.exists(restore_path):
            console.print(f"[bold yellow]Warning:[/bold yellow] Destination '{restore_path}' already exists.")
            confirm = Confirm.ask("Do you want to overwrite it?")
            if not confirm:
                console.print("[bold yellow]Restore cancelled.[/bold yellow]")
                return

        if os.path.isfile(backup_path):
            shutil.copy2(backup_path, restore_path)
            console.print(f"[bold green]File '{backup_path}' restored to '{restore_path}' successfully.[/bold green]")
        elif os.path.isdir(backup_path):
            shutil.copytree(backup_path, restore_path)
            console.print(f"[bold green]Directory '{backup_path}' restored to '{restore_path}' successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS Restore Utility[/bold cyan]")
    backup_path = Prompt.ask("Enter the backup file/directory path").strip()
    restore_path = Prompt.ask("Enter the restore destination path").strip()
    restore_command(backup_path, restore_path)