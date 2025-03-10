from rich.console import Console
from rich.panel import Panel

console = Console()

def ver_command():
    """
    نمایش نسخه‌ی PyDOS به همراه اطلاعات تکمیلی
    """
    version = "2.0 FINAL"
    developer = "T7280H"
    year = "2024"

    panel = Panel(
        f"[bold cyan]PyDOS Version:[/bold cyan] {version}\n"
        f"[bold yellow]Developer:[/bold yellow] {developer}\n"
        f"[bold magenta]Year:[/bold magenta] {year}",
        title="[bold green]PyDOS Information[/bold green]", expand=False
    )
    
    console.print(panel)

if __name__ == "__main__":
    ver_command()