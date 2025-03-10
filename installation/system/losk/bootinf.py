import sys
import time
from datetime import datetime
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel

# فعال‌سازی Colorama
init(autoreset=True)
console = Console()

def animate_text(text, color=Fore.YELLOW, delay=0.1):
    """ نمایش متن به‌صورت انیمیشنی """
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def bootinf_command():
    console.clear()
    
    # نمایش اطلاعات بوت
    banner = Panel(
        "[bold cyan]XC-GRUB BOOTLOADER VER:1.0[/bold cyan]\n"
        "[bold magenta]Created by T7280H[/bold magenta]\n"
        f"[bold green]Boot Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold green]",
        title="[bold red]BOOT INFO[/bold red]", expand=False
    )
    
    console.print(banner)
    time.sleep(2)

if __name__ == "__main__":
    bootinf_command()
