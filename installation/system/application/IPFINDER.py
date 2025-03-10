import requests
import pyfiglet
import os
import sys
import time
import subprocess
from colorama import Fore, Back, Style, init

# Initialize colodef run_pydos():
    pydos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shell', 'pydos.py'))
    if os.path.exists(pydos_path):
        subprocess.run([sys.executable, pydos_path])
    else:
        print(f"File not found: {pydos_path}")rama
init(autoreset=True)

# نمایش بنر
def display_banner():
    banner = pyfiglet.figlet_format("IP FINDER")
    print(Back.RED + Fore.WHITE + banner)

# دریافت اطلاعات IP
def get_ip_info(ip=""):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "success":
            print(Back.RED + Fore.WHITE + "-" * 40)
            print(Back.RED + Fore.YELLOW + f"IP Address: {Fore.WHITE}{data['query']}")
            print(Back.RED + Fore.YELLOW + f"Country: {Fore.WHITE}{data['country']}")
            print(Back.RED + Fore.YELLOW + f"City: {Fore.WHITE}{data['city']}")
            print(Back.RED + Fore.YELLOW + f"Geographical Location: {Fore.WHITE}{data['lat']}, {data['lon']}")
            print(Back.RED + Fore.YELLOW + f"Mobile Operator (ISP): {Fore.WHITE}{data['isp']}")
            print(Back.RED + Fore.WHITE + "-" * 40)
        else:
            print(Back.RED + Fore.WHITE + "Error: Unable to fetch IP information")
    except requests.exceptions.RequestException as e:
        print(Back.RED + Fore.WHITE + f"HTTP Request failed: {e}")

# تأیید خروج
def confirm_exit():
    choice = input("\nReturn to Pydos (Y/N)? ").strip().lower()
    if choice == 'y':
        print("Returning to Pydos...\n")
        time.sleep(2)
        os.system('clear')
        sys.exit(0)
    else:
        print("Operation canceled.\n")

if __name__ == "__main__":
    display_banner()
    
    # گرفتن IP از کاربر
    user_ip = input(Back.RED + Fore.WHITE + "Enter your IP (leave blank for your public IP): ").strip()
    get_ip_info(user_ip)
    
    # نمایش پیام برای خروج
    confirm_exit()