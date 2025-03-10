import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()

def date_command():
    """
    نمایش تاریخ و زمان فعلی با فرمت زیبا
    """
    now = datetime.datetime.now()
    
    formatted_date = now.strftime("%A, %d %B %Y")  # مثال: Monday, 19 February 2024
    formatted_time = now.strftime("%I:%M:%S %p")  # ساعت ۱۲ ساعته + AM/PM

    panel = Panel(f"[bold cyan]Date:[/bold cyan] {formatted_date}\n[bold yellow]Time:[/bold yellow] {formatted_time}",
                  title="[bold green]Current Date & Time[/bold green]", expand=False)
    
    console.print(panel)

if __name__ == "__main__":
    date_command()