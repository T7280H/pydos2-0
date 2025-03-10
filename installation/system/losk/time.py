import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()

def time_command():
    """
    نمایش تاریخ و زمان فعلی به‌صورت زیباتر
    """
    now = datetime.datetime.now()
    formatted_date = now.strftime("%A, %d %B %Y")  # نمایش روز، ماه و سال (مثال: Monday, 19 February 2024)
    formatted_time_24h = now.strftime("%H:%M:%S")  # نمایش زمان به فرمت 24 ساعته
    formatted_time_12h = now.strftime("%I:%M:%S %p")  # نمایش زمان به فرمت 12 ساعته با AM/PM
    timezone = now.astimezone().tzinfo  # نمایش منطقه زمانی
    
    panel = Panel(
        f"[bold cyan]Date:[/bold cyan] {formatted_date}\n"
        f"[bold yellow]Time (24h):[/bold yellow] {formatted_time_24h}\n"
        f"[bold yellow]Time (12h):[/bold yellow] {formatted_time_12h}\n"
        f"[bold magenta]TimeZone:[/bold magenta] {timezone}",
        title="[bold green]Current Date & Time[/bold green]", expand=False
    )
    
    console.print(panel)

if __name__ == "__main__":
    time_command()