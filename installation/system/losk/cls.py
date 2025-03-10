import os
import time
from rich.console import Console

console = Console()

def cls_command():
    """ پاک کردن صفحه نمایش در ترمینال """
    console.print("[bold cyan]Clearing screen...[/bold cyan]")
    time.sleep(0.5)  # افکت زمانی کوتاه برای زیبایی
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    cls_command()