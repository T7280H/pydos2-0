import sys
from rich.console import Console

console = Console()

def echo_command(message):
    """
    چاپ پیام ورودی با فرمت زیباتر
    """
    if message.strip():
        console.print(f"[bold cyan]{message}[/bold cyan]")
    else:
        console.print("[bold yellow]Warning: Empty message![/bold yellow]")

if __name__ == "__main__":
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter the message to echo: ").strip()
    echo_command(message)