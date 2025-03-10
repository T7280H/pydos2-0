import os
import sys
from colorama import Fore, Style, init
from rich.console import Console

# فعال‌سازی Colorama
init(autoreset=True)
console = Console()

def cd_command(directory):
    try:
        # پشتیبانی از `cd ~` برای رفتن به home
        if directory == "~":
            directory = os.path.expanduser("~")
        
        # تغییر دایرکتوری
        os.chdir(directory)
        console.print(f"[bold green]Changed directory to:[/bold green] {os.getcwd()}")
    
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] The directory '{directory}' does not exist.")
    except PermissionError:
        console.print(f"[bold red]Error:[/bold red] You do not have permission to access '{directory}'.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    directory = input(Fore.CYAN + "Enter the directory path: " + Style.RESET_ALL).strip()
    cd_command(directory)