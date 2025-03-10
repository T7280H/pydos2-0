import time
import threading
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def reminder_command(message, delay):
    """
    ایجاد یک یادآوری بعد از مدت مشخص
    """
    def reminder():
        for i in range(delay, 0, -1):
            console.print(f"[bold yellow]Reminder in {i} seconds...[/bold yellow]", end="\r")
            time.sleep(1)
        console.print(f"\n[bold green]Reminder:[/bold green] {message}")

    threading.Thread(target=reminder, daemon=True).start()

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS Reminder Utility[/bold cyan]")
    message = Prompt.ask("Enter the reminder message").strip()
    
    try:
        delay = int(Prompt.ask("Enter the delay in seconds"))
        reminder_command(message, delay)
        console.print("[bold green]Reminder set successfully![/bold green]")
    except ValueError:
        console.print("[bold red]Error:[/bold red] Please enter a valid number for delay.")