import curses
import os
import json

CONFIG_PATH = os.path.join("Config")
ACCOUNTS_FILE = os.path.join(CONFIG_PATH, "account.json")
BANNER_DIR = os.path.join("banner")

# ایجاد پوشه Config در صورت نبودن
if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

def save_accounts(username, password):
    """ذخیره حساب کاربری در فایل account.json"""
    account_data = {
        "login": username,
        "password": password
    }

    with open(ACCOUNTS_FILE, 'w') as file:
        json.dump(account_data, file, indent=4)

def load_accounts():
    """بارگذاری اطلاعات حساب کاربری"""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def create_account(stdscr):
    """ایجاد حساب جدید"""
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Create an Account", curses.color_pair(1))
    stdscr.addstr(1, 0, "Enter username: ")
    username = stdscr.getstr().decode('utf-8')
    stdscr.addstr(2, 0, "Enter password: ", curses.color_pair(1))
    password = stdscr.getstr().decode('utf-8')
    curses.noecho()

    save_accounts(username, password)
    draw_message_box(stdscr, "Account created successfully!")

def login_account(stdscr):
    """ورود به حساب کاربری"""
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Login to your Account", curses.color_pair(1))
    stdscr.addstr(1, 0, "Enter username: ")
    username = stdscr.getstr().decode('utf-8')
    stdscr.addstr(2, 0, "Enter password: ", curses.color_pair(1))
    password = stdscr.getstr().decode('utf-8')
    curses.noecho()

    account_data = load_accounts()
    if account_data.get("login") == username and account_data.get("password") == password:
        draw_message_box(stdscr, "Login successful!")
        return True

    draw_message_box(stdscr, "Login failed: Incorrect username or password.")
    return False

def change_banner(stdscr):
    """تغییر بنر PyDOS"""
    stdscr.clear()
    stdscr.addstr(0, 0, "Select a Banner", curses.color_pair(1))

    if not os.path.exists(BANNER_DIR):
        draw_message_box(stdscr, "Error: Banner folder not found!")
        return

    banners = [f for f in os.listdir(BANNER_DIR) if os.path.isfile(os.path.join(BANNER_DIR, f))]

    if not banners:
        draw_message_box(stdscr, "No banners found in the folder.")
        return

    for idx, banner in enumerate(banners, start=1):
        stdscr.addstr(idx, 0, f"{idx}. {banner}", curses.color_pair(1))

    stdscr.addstr(len(banners) + 1, 0, "Select a banner by ID: ", curses.color_pair(1))
    curses.echo()
    choice = stdscr.getstr().decode('utf-8')
    curses.noecho()

    try:
        selected_banner = banners[int(choice) - 1]
        with open(os.path.join(BANNER_DIR, 'current_banner.txt'), 'w') as file:
            file.write(selected_banner)
        draw_message_box(stdscr, f"Banner '{selected_banner}' selected successfully!")
    except (ValueError, IndexError):
        draw_message_box(stdscr, "Invalid choice! Please enter a valid number.")

def show_pydos_info(stdscr):
    """نمایش اطلاعات PyDOS"""
    stdscr.clear()
    stdscr.addstr(0, 0, "PyDOS System Information", curses.color_pair(1))
    stdscr.addstr(1, 0, "Version: 2.0 FINAL", curses.color_pair(1))
    stdscr.addstr(2, 0, "Developer: T7280H", curses.color_pair(1))
    stdscr.addstr(3, 0, "GitHub: https://github.com/T7280H", curses.color_pair(1))
    stdscr.addstr(5, 0, "Press any key to return to settings.", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()

def draw_message_box(stdscr, message):
    """نمایش یک پیام در صفحه"""
    h, w = stdscr.getmaxyx()
    box_height = 5
    box_width = len(message) + 4
    start_y = (h - box_height) // 2
    start_x = (w - box_width) // 2

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(start_y, start_x, "+" + "-" * (box_width - 2) + "+")
    stdscr.addstr(start_y + 1, start_x, "|" + " " * (box_width - 2) + "|")
    stdscr.addstr(start_y + 2, start_x, f"| {message} |")
    stdscr.addstr(start_y + 3, start_x, "|" + " " * (box_width - 2) + "|")
    stdscr.addstr(start_y + 4, start_x, "+" + "-" * (box_width - 2) + "+")
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()

def setting_command(stdscr):
    """منوی تنظیمات PyDOS"""
    options = [
        ("Create an Account", create_account),
        ("Login to your Account", login_account),
        ("Change PyDOS Banner", change_banner),
        ("Show PyDOS Info", show_pydos_info),
        ("Exit Settings", lambda stdscr: None)
    ]
    
    current_option = 0
    while True:
        stdscr.clear()
        stdscr.bkgd(' ', curses.color_pair(1))
        stdscr.addstr(0, 0, "PyDOS Settings", curses.color_pair(1))

        for idx, (desc, _) in enumerate(options):
            if idx == current_option:
                stdscr.addstr(idx + 1, 0, f"--> [{idx + 1}] {desc}", curses.color_pair(2))
            else:
                stdscr.addstr(idx + 1, 0, f"[{idx + 1}] {desc}", curses.color_pair(1))

        stdscr.addstr(len(options) + 1, 0, "Use arrow keys to move, Enter to select and to exit press the q button.", curses.color_pair(1))
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif key == curses.KEY_DOWN and current_option < len(options) - 1:
            current_option += 1
        elif key == ord('\n'):
            options[current_option][1](stdscr)
        elif key == ord('q'):
            break

def main(stdscr):
    """تابع اصلی"""
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    setting_command(stdscr)

def setting_body():
    """اجرای تنظیمات PyDOS"""
    curses.wrapper(main)

if __name__ == "__main__":
    setting_body()