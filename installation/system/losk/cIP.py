import subprocess
import sys
from colorama import Fore, Style, init
from rich.console import Console

# فعال‌سازی رنگ‌ها
init(autoreset=True)
console = Console()

def cIP_command(new_ip, interface="wlan0"):
    """
    تغییر IP روی اینترفیس مشخص‌شده
    """
    if sys.platform.startswith("win"):
        console.print("[bold red]Error:[/bold red] This command only works on Linux!", style="bold red")
        return

    try:
        # تغییر IP با `ip addr`
        command_ip = f"sudo ip addr add {new_ip}/24 dev {interface}"
        subprocess.run(command_ip, shell=True, check=True)

        # فعال و غیرفعال کردن اینترفیس برای اعمال تغییرات
        subprocess.run(f"sudo ip link set {interface} down", shell=True, check=True)
        subprocess.run(f"sudo ip link set {interface} up", shell=True, check=True)

        # تنظیم Gateway
        gateway = '.'.join(new_ip.split('.')[:3]) + '.1'
        command_gateway = f"sudo ip route add default via {gateway} dev {interface}"
        subprocess.run(command_gateway, shell=True, check=True)

        console.print(f"[bold green]IP address changed to:[/bold green] {new_ip} on [bold cyan]{interface}[/bold cyan]")

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to change IP:[/bold red] {e}")

if __name__ == "__main__":
    console.print("[bold yellow]Change IP Address - PyDOS[/bold yellow]")
    new_ip = input(Fore.CYAN + "Enter the new IP address: " + Style.RESET_ALL).strip()
    interface = input(Fore.CYAN + "Enter the network interface (default: wlan0): " + Style.RESET_ALL).strip() or "wlan0"
    cIP_command(new_ip, interface)