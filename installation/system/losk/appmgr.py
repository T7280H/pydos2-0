import os
import shutil
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def appmgr_command(switch, app_name):
    """
    مدیریت برنامه‌های PyDOS (نصب، حذف و نمایش اطلاعات)
    """
    current_dir = os.getcwd()
    app_dir = os.path.join(current_dir, 'installation')
    info_path = os.path.join(app_dir, 'info.txt')
    install_path = os.path.join(app_dir, app_name)
    apps_dir = os.path.join(current_dir, 'system', 'application', app_name)

    if not os.path.exists(app_dir):
        console.print(f"[bold red]Error:[/bold red] Installation directory does not exist.")
        return

    if switch == '-v':
        # نصب برنامه
        if os.path.exists(install_path):
            if os.path.exists(info_path):
                with open(info_path, 'r') as info_file:
                    console.print(f"[bold cyan]App Information for {app_name}:[/bold cyan]\n")
                    console.print(info_file.read())

                if os.path.exists(apps_dir):
                    console.print(f"[bold yellow]Warning:[/bold yellow] {app_name} is already installed.")
                else:
                    confirm = Confirm.ask("Do you want to install this app?")
                    if confirm:
                        shutil.copy(install_path, apps_dir)
                        console.print(f"[bold green]App {app_name} installed successfully.[/bold green]")
                    else:
                        console.print("[bold yellow]Installation cancelled.[/bold yellow]")
            else:
                console.print(f"[bold red]Error:[/bold red] Info file for {app_name} not found.")
        else:
            console.print(f"[bold red]Error:[/bold red] Install file for {app_name} not found.")

    elif switch == '-t':
        # نمایش اطلاعات برنامه
        if os.path.exists(info_path):
            with open(info_path, 'r') as info_file:
                console.print(f"[bold cyan]App Information for {app_name}:[/bold cyan]\n")
                console.print(info_file.read())
        else:
            console.print(f"[bold red]Error:[/bold red] Info file for {app_name} not found.")

    elif switch == '-d':
        # حذف برنامه
        if os.path.exists(apps_dir):
            confirm = Confirm.ask(f"Are you sure you want to remove {app_name}?")
            if confirm:
                shutil.rmtree(apps_dir)
                console.print(f"[bold green]App {app_name} removed successfully.[/bold green]")
            else:
                console.print("[bold yellow]Removal cancelled.[/bold yellow]")
        else:
            console.print(f"[bold red]Error:[/bold red] {app_name} is not installed.")

    else:
        console.print(f"[bold red]Invalid switch:[/bold red] {switch}")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS Application Manager[/bold cyan]")
    switch = Prompt.ask("Enter the switch (-v: Install, -t: Info, -d: Remove)")
    app_name = Prompt.ask("Enter the app name")
    appmgr_command(switch, app_name)