from flask import Flask, request, render_template_string
import pyfiglet
from termcolor import colored
import time
import os
import subprocess
import platform

try:
    from pyngrok import ngrok
    NGROK_AVAILABLE = True
except ImportError:
    NGROK_AVAILABLE = False

# تنظیمات اولیه
PORT = 5050
LINK_PATH = "/dev/zx"
NGROK_PATH = os.path.expanduser("~/.config/ngrok/ngrok")

app = Flask(__name__)

# بررسی و نصب خودکار ngrok
def install_ngrok():
    global NGROK_AVAILABLE
    
    print(colored("Ngrok not found! Installing...", 'yellow', attrs=['bold']))
    os.makedirs(os.path.dirname(NGROK_PATH), exist_ok=True)
    
    # تشخیص معماری سیستم
    arch = platform.machine()
    if arch in ["aarch64", "arm64"]:
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-arm64.tgz"
    elif arch in ["arm", "armv7l"]:
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-arm.tgz"
    elif arch in ["x86_64"]:
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-amd64.tgz"
    else:
        print(colored("Unsupported architecture!", 'red'))
        return
    
    # دانلود و استخراج فایل ngrok
    os.system(f"curl -o /tmp/ngrok.tgz {ngrok_url}")
    os.system(f"tar -xvzf /tmp/ngrok.tgz -C {os.path.dirname(NGROK_PATH)}")
    os.system(f"chmod +x {NGROK_PATH}")

    # بررسی نصب
    if os.path.exists(NGROK_PATH):
        NGROK_AVAILABLE = True
        print(colored("Ngrok installed successfully!", 'green', attrs=['bold']))
    else:
        print(colored("Ngrok installation failed!", 'red', attrs=['bold']))

# نمایش بنر
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format("IP TRACKER")
    
    for char in banner:
        print(colored(char, 'cyan'), end="", flush=True)
        time.sleep(0.002)
    
    print(colored("\n1- CREATE A LOCALHOST LINK", 'yellow', attrs=['bold']))
    print(colored("2- CREATE A NGROK LINK", 'green', attrs=['bold']) if NGROK_AVAILABLE else "")
    print(colored("3- EXIT", 'red', attrs=['bold']))
    print(colored("=" * 50, 'cyan'))

# ایجاد لینک محلی
def create_local_link():
    print(colored("Creating local link...", 'yellow', attrs=['bold']))
    print(colored("Please wait...", 'yellow', attrs=['bold']))
    time.sleep(2)

    local_url = f"http://127.0.0.1:{PORT}{LINK_PATH}"
    print(colored(f"Your Localhost Link: {local_url}", 'green', attrs=['bold']))
    print(colored("Waiting for users...", 'cyan'))
    print(colored("=" * 50, 'cyan'))

    app.run(port=PORT)

# ایجاد لینک Ngrok
def create_ngrok_link():
    if not NGROK_AVAILABLE:
        install_ngrok()
        if not NGROK_AVAILABLE:
            return

    print(colored("Creating ngrok link...", 'green', attrs=['bold']))
    print(colored("Please wait...", 'green', attrs=['bold']))
    time.sleep(2)

    public_url = ngrok.connect(PORT).public_url + LINK_PATH
    print(colored(f"Your Ngrok Link: {public_url}", 'green', attrs=['bold']))
    print(colored("Waiting for users...", 'cyan'))
    print(colored("=" * 50, 'cyan'))

    app.run(port=PORT)

# مسیر دریافت آی‌پی
@app.route(LINK_PATH)
def track_ip():
    user_ip = request.remote_addr
    print(colored(f"\nUser Found!", 'green', attrs=['bold']))
    print(colored(f"IP Address: {user_ip}", 'green', attrs=['bold']))
    print(colored("=" * 50, 'cyan'))
    
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>User IP Tracker</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; background-color: #282c34; color: white; padding: 50px; }
                h1 { font-size: 3em; }
                .ip-box { background: #61dafb; padding: 20px; border-radius: 10px; display: inline-block; color: black; }
            </style>
        </head>
        <body>
            <h1>✅ IP Address Found!</h1>
            <p class="ip-box">
                <h2>{{ user_ip }}</h2>
            </p>
        </body>
        </html>
    """, user_ip=user_ip)

# اجرای برنامه
if __name__ == "__main__":
    if not NGROK_AVAILABLE:
        install_ngrok()

    while True:
        print_banner()
        choice = input(colored("Enter your choice: ", 'yellow', attrs=['bold']))
        
        if choice == "1":
            create_local_link()
        elif choice == "2" and NGROK_AVAILABLE:
            create_ngrok_link()
        elif choice == "3":
            print(colored("Exiting...", 'red', attrs=['bold']))
            time.sleep(2)
            os.system('clear')
            break
        else:
            print(colored("Invalid choice, try again!", 'red', attrs=['bold']))