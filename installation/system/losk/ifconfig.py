import psutil
import socket
from rich.console import Console
from rich.table import Table

console = Console()

def ifconfig_command():
    """
    نمایش اطلاعات کامل شبکه شامل IP، MAC Address و وضعیت اینترفیس‌ها
    """
    interfaces = psutil.net_if_addrs()
    table = Table(title="Network Interfaces", show_header=True, header_style="bold cyan")
    table.add_column("Interface", style="bold white")
    table.add_column("IP Address", style="bold yellow")
    table.add_column("MAC Address", style="bold magenta")

    for interface, addresses in interfaces.items():
        ip_address = "N/A"
        mac_address = "N/A"

        for addr in addresses:
            if addr.family == socket.AF_INET:
                ip_address = addr.address
            elif addr.family == psutil.AF_LINK:
                mac_address = addr.address

        table.add_row(interface, ip_address, mac_address)

    console.print(table)

if __name__ == "__main__":
    ifconfig_command()