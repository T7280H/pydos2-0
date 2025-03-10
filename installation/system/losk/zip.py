import zipfile
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

console = Console()

def zip_command(source, destination):
    """
    فشرده‌سازی فایل یا پوشه به ZIP
    """
    try:
        if not os.path.exists(source):
            console.print(f"[bold red]Error:[/bold red] The source '{source}' does not exist.")
            return

        with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isdir(source):
                file_list = []
                for root, _, files in os.walk(source):
                    for file in files:
                        file_list.append(os.path.join(root, file))

                # نمایش نوار پیشرفت هنگام فشرده‌سازی
                with Progress() as progress:
                    task = progress.add_task("[cyan]Compressing...", total=len(file_list))
                    for file in file_list:
                        zipf.write(file, os.path.relpath(file, os.path.join(source, '..')))
                        progress.update(task, advance=1)

                console.print(f"[bold green]Directory '{source}' compressed to '{destination}' successfully.[/bold green]")

            elif os.path.isfile(source):
                zipf.write(source, os.path.basename(source))
                console.print(f"[bold green]File '{source}' compressed to '{destination}' successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS ZIP Compressor[/bold cyan]")
    source = Prompt.ask("Enter the source file/directory path").strip()
    destination = Prompt.ask("Enter the destination zip file path").strip()
    zip_command(source, destination)