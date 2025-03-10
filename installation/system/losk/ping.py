import subprocess
import platform
from rich.console import Console

console = Console()

def ping_command(host):
    """
    تست پینگ برای بررسی دسترسی به هاست و نمایش زمان پاسخ
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", host], capture_output=True, text=True, check=True)
        console.print(f"[bold green]{host} is up![/bold green]")
        
        # استخراج زمان پاسخ از خروجی پینگ
        if "time=" in result.stdout:
            response_time = result.stdout.split("time=")[-1].split(" ")[0]
            console.print(f"[bold yellow]Response Time:[/bold yellow] {response_time}")
    
    except subprocess.CalledProcessError:
        console.print(f"[bold red]{host} is down![/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold cyan]PyDOS Ping Utility[/bold cyan]")
    host = input("Enter the host to ping: ").strip()
    
    if host:
        ping_command(host)
    else:
        console.print("[bold red]Error:[/bold red] No host entered!")