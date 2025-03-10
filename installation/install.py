import os
import shutil
import subprocess
import time
import curses
import json
from rich.console import Console

# Initialize rich console for better output
console = Console()

VALID_LICENSE_CODE = "PYDOS-7180-6277-RT89"  # کد لایسنس معتبر

def print_center(stdscr, text, delay=0.01):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    x = width // 2 - len(text) // 2
    y = height // 2

    # رنگ سایه (برای نمایش متن)
    stdscr.attron(curses.color_pair(6))  # سایه روشن
    stdscr.addstr(y + 1, x + 1, text)  # سایه کمی پایین‌تر و سمت راست
    stdscr.attroff(curses.color_pair(6))

    # رنگ متن اصلی
    stdscr.attron(curses.color_pair(4))  # رنگ روشن‌تر برای متن
    for char in text:
        stdscr.addstr(y, x, char)
        stdscr.refresh()
        time.sleep(delay)
        x += 1
    time.sleep(1)
    stdscr.clear()
    stdscr.refresh()

def print_slow(stdscr, text, delay=0.01):
    height, width = stdscr.getmaxyx()
    lines = []
    for i in range(0, len(text), width - 1):
        lines.append(text[i:i + width - 1])
    for line in lines:
        stdscr.addstr(line + "\n")
        stdscr.refresh()
        time.sleep(delay)
    stdscr.refresh()

def draw_menu(stdscr, selected_row_idx, menu):
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h - 2 - len(menu) + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def create_message_box(stdscr, message, display_time=2):
    h, w = stdscr.getmaxyx()
    box_width = min(max(len(message) + 4, 50), w - 2)
    box_height = min(5, h - 2)
    box_x = w // 2 - box_width // 2
    box_y = h // 2 - box_height // 2

    # رنگ سایه (برای اطراف پنجره) بدون تغییر
    stdscr.attron(curses.color_pair(6))  # استفاده از رنگ شماره 6 برای سایه
    for i in range(box_height + 1):
        stdscr.addstr(box_y + i + 1, box_x + 2, " " * (box_width - 2))
    stdscr.attroff(curses.color_pair(6))

    # کادر پنجره (رنگ روشن‌تر برای کادر)
    stdscr.attron(curses.color_pair(5))  # استفاده از رنگ شماره 5 برای کادر پنجره
    for i in range(box_height):
        stdscr.addstr(box_y + i, box_x, " " * box_width)
    stdscr.attroff(curses.color_pair(5))

    # پس‌زمینه پنجره (رنگ روشن‌تر برای پس‌زمینه پنجره)
    stdscr.attron(curses.color_pair(4))  # استفاده از رنگ روشن برای پس‌زمینه
    for i in range(box_height):
        stdscr.addstr(box_y + i, box_x + 1, " " * (box_width - 2))
    stdscr.attroff(curses.color_pair(4))

    # نمایش پیام داخل پنجره
    message_lines = message.splitlines()
    for idx, line in enumerate(message_lines):
        if idx >= box_height - 2:
            break
        if len(line) > box_width - 4:
            line = line[:box_width - 4]
        if box_y + 1 + idx < h and box_x + 2 + len(line) < w:
            stdscr.addstr(box_y + 1 + idx, box_x + 2, line, curses.A_BOLD)

    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    time.sleep(display_time)
    stdscr.clear()

def check_files(files, base_path):
    missing_files = []
    for file in files:
        if not os.path.exists(os.path.join(base_path, file)):
            missing_files.append(file)
    return missing_files

def spin_loader(stdscr, message, duration=2):
    h, w = stdscr.getmaxyx()
    box_width = min(max(len(message) + 4, 50), w - 2)
    box_height = 5
    box_x = w // 2 - box_width // 2
    box_y = h // 2 - box_height // 2

    # رنگ سایه (برای نمایش متن و کادر)
    stdscr.attron(curses.color_pair(6))  # سایه
    for i in range(box_height + 1):
        stdscr.addstr(box_y + i + 1, box_x + 1, " " * box_width)  # سایه کادر
    stdscr.attroff(curses.color_pair(6))

    # کادر اصلی
    stdscr.attron(curses.color_pair(1))  # کادر اصلی
    for i in range(box_height):
        stdscr.addstr(box_y + i, box_x, " " * box_width)  # کادر
    stdscr.addstr(box_y + 1, box_x + 2, message)  # نمایش پیام اصلی
    stdscr.attroff(curses.color_pair(1))

    # انیمیشن چرخشی
    stdscr.refresh()
    spinner = ['|', '/', '-', '\\']
    for _ in range(duration * 10):
        for char in spinner:
            stdscr.addstr(box_y + 3, box_x + 2, char)  # نمایش چرخش
            stdscr.refresh()
            time.sleep(0.1)
    stdscr.clear()
    stdscr.refresh()

def select_install_path(stdscr):
    create_message_box(stdscr, "Please select the installation path.")
    return input_window(stdscr, "Enter the installation path (e.g., /storage/emulated/0): ")

def enter_name_and_password(stdscr):
    create_message_box(stdscr, "Please enter your name and password.")
    name = input_window(stdscr, "Enter your name: ")
    password = input_window(stdscr, "Enter your password: ")  # جمع‌آوری پسورد
    return name, password

def input_window(stdscr, prompt):
    h, w = stdscr.getmaxyx()
    input_height = 5
    input_width = min(max(len(prompt) + 4, 50), w - 2)
    input_win = curses.newwin(input_height, input_width, h // 2 - input_height // 2, w // 2 - input_width // 2)
    input_win.box()
    input_win.addstr(1, 1, prompt)
    input_win.refresh()
    curses.echo()
    user_input = input_win.getstr(1, len(prompt) + 1).decode().strip()
    curses.noecho()
    return user_input

def license_agreement(stdscr):
    license_text = """
    PyDOS License Agreement
    ------------------------
    By using this software, you agree to the following terms and conditions:
    1. You may use this software for personal and commercial purposes.
    2. Redistribution of this software is prohibited without prior written consent.
    3. The author is not responsible for any damage caused by the use of this software.
    """
    print_slow(stdscr, license_text)
    menu = ["Yes", "No"]
    current_row = 0
    while True:
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return current_row == 0

def input_license_code(stdscr):
    while True:
        license_code = input_window(stdscr, "Enter the license code: ")

        # Validate the license code
        if license_code == VALID_LICENSE_CODE:
            return license_code
        else:
            create_message_box(stdscr, "Invalid license code. Please try again.")

def save_user_info(stdscr, name, password, install_path):
    cache_dir = os.path.join(install_path, ".cache")
    os.makedirs(cache_dir, exist_ok=True)

    cache_path = os.path.join(cache_dir, "cache.txt")
    with open(cache_path, "w") as cache_file:
        cache_file.write(f"login: {name}\n")
        cache_file.write(f"password: {password}\n")
        
    create_message_box(stdscr, "INFORMATION SAVED, READY TO CONVERT.")

def convert_cache_to_json(stdscr, install_path):
    cache_path = os.path.join(install_path, ".cache", "cache.txt")
    account_path = os.path.join(install_path, "Config", "account.json")

    if os.path.exists(cache_path):
        with open(cache_path, "r") as cache_file:
            lines = cache_file.readlines()
            user_info = {}
            for line in lines:
                key, value = line.strip().split(": ")
                user_info[key] = value

        with open(account_path, "w") as account_file:
            json.dump(user_info, account_file)
        
        create_message_box(stdscr, f"User information converted and saved to {account_path}")
    else:
        create_message_box(stdscr, "cache.txt not found.")

def check_memory(stdscr):
    create_message_box(stdscr, "Checking memory...")
    spin_loader(stdscr, "Checking memory", duration=2)
    create_message_box(stdscr, "Memory check complete.")

def format_directory(stdscr, path):
    create_message_box(stdscr, f"Formatting directory: {path}")
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))
    create_message_box(stdscr, f"Directory {path} formatted successfully")

def create_directories(stdscr, destination):
    directories = ["losk", "shell", "banner", "application", "Config"]
    for directory in directories:
        os.makedirs(os.path.join(destination, directory), exist_ok=True)
    create_message_box(stdscr, "Directories created successfully")

def copy_files(stdscr, files, base_path, destination):
    create_message_box(stdscr, "Copying files...")
    for file, target_dir in files.items():
        target_path = os.path.join(destination, target_dir)
        print_slow(stdscr, "Setup is Copying Files, Please Wait...")
        create_message_box(stdscr, f"COPYING: {file.split('/')[-1]}", display_time=1)

        try:
            shutil.copy(os.path.join(base_path, file), target_path)
        except FileNotFoundError:
            create_message_box(stdscr, f"Error: {file} not found. Skipping...")
    create_message_box(stdscr, "Files copied successfully")

def copy_boot_file(stdscr, base_path, install_path):
    create_message_box(stdscr, "Copying XC-GRUB BOOTLOADER...")
    shutil.copy(os.path.join(base_path, "xcgrub.py"), install_path)
    create_message_box(stdscr, "XC-GRUP copied successfully")

def install_requirements(stdscr, base_path):
    create_message_box(stdscr, "Installing required packages...")
    try:
        subprocess.check_call(["pip", "install", "-r", os.path.join(base_path, "requirements.txt")])
        create_message_box(stdscr, "Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        create_message_box(stdscr, f"Error installing requirements: {e}")

def display_readme(stdscr, base_path):
    readme_path = os.path.join(base_path, "read", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as file:
            readme_lines = file.readlines()
        current_line = 0
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            for i, line in enumerate(readme_lines[current_line:current_line + height - 1]):
                stdscr.addstr(i, 0, line.strip())
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_DOWN and current_line < len(readme_lines) - height + 1:
                current_line += 1
            elif key == curses.KEY_UP and current_line > 0:
                current_line -= 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break
    else:
        create_message_box(stdscr, "README.md file not found in 'read' folder.")

    menu = ["Continue"]
    current_row = 0
    while True:
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                return

def setup_complete(stdscr):
    create_message_box(stdscr, "Setup is complete. PyDOS is installed, please wait...")

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)  # Set red background
    stdscr.bkgd(' ', curses.color_pair(2))
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    
    # سایه: مشکی روی پس‌زمینه فیروزه‌ای روشن
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
    current_row = 0

    base_path = "system"
    required_files = [
        "application/wendaconverter.py", "application/bashconverter.py", "application/editor.py", 
        "application/iptracker.py", "application/IPFINDER.py", "application/pybomber.py", 
        "banner/__init__.py", "banner/dragon.py", "banner/final.py", "banner/hacker.py", 
        "banner/pydosbanner.py", "losk/__init__.py", "losk/appmgr.py", "losk/backup.py", 
        "losk/bashrc.py", "losk/bomb.py", "losk/bootinf.py", "losk/calc.py", "losk/cat.py", 
        "losk/cd.py", "losk/cIP.py", "losk/cls.py", "losk/dash.py", "losk/help.py", 
        "losk/date.py", "losk/defpath.py", "losk/pyrun.py", "losk/dir.py", "losk/echo.py", "losk/edit.py", 
        "losk/exit.py", "losk/find.py", "losk/ifconfig.py", "losk/ipfinder.py", 
        "losk/mkdir.py", "losk/mv.py", "losk/partest.py", "losk/ping.py", 
        "losk/reminder.py", "losk/rename.py", "losk/restore.py", "losk/setting.py", 
        "losk/time.py", "losk/touch.py", "losk/unzip.py", "losk/zip.py", "losk/ver.py", 
        "losk/wenda.py", "losk/xcopy.py", "shell/pydos.py", "losk/rd.py", "losk/tracker.py", "xcgrub.py", "banner/arial.py", "banner/greenyellow.py", "requirements.txt"
    ]

    files = {
        "application/bashconverter.py": "application", "application/wendaconverter.py": "application", 
        "application/editor.py": "application", "application/iptracker.py": "application", 
        "application/IPFINDER.py": "application", "application/pybomber.py": "application", 
        "banner/__init__.py": "banner", "banner/dragon.py": "banner", "banner/final.py": "banner", "banner/greenyellow.py": "banner", "banner/arial.py": "banner", 
       "banner/hacker.py": "banner", "banner/pydosbanner.py": "banner", "losk/__init__.py": "losk", 
        "losk/backup.py": "losk", "losk/bashrc.py": "losk", "losk/bomb.py": "losk", 
        "losk/bootinf.py": "losk", "losk/calc.py": "losk", "losk/cat.py": "losk", 
        "losk/cd.py": "losk", "losk/cIP.py": "losk", "losk/cls.py": "losk", "losk/dash.py": "losk", 
        "losk/help.py": "losk", "losk/date.py": "losk", "losk/defpath.py": "losk", 
        "losk/dir.py": "losk", "losk/echo.py": "losk", "losk/edit.py": "losk", 
        "losk/exit.py": "losk", "losk/find.py": "losk", "losk/ifconfig.py": "losk", 
        "losk/ipfinder.py": "losk", "losk/mkdir.py": "losk", "losk/mv.py": "losk", 
        "losk/partest.py": "losk", "losk/ping.py": "losk", "losk/reminder.py": "losk", 
        "losk/rename.py": "losk", "losk/restore.py": "losk", "losk/setting.py": "losk", 
        "losk/time.py": "losk", "losk/touch.py": "losk", "losk/unzip.py": "losk", 
        "losk/zip.py": "losk", "losk/ver.py": "losk", "losk/wenda.py": "losk", 
        "losk/xcopy.py": "losk", "losk/appmgr.py": "losk", "losk/rd.py": "losk", "losk/pyrun.py": "losk", "losk/tracker.py": "losk", "shell/pydos.py": "shell"
    }

    try:
        print_center(stdscr, "SETUP IS STARTING...")
        print_slow(stdscr, "Checking required files...")
        missing_files = check_files(required_files, base_path)
        if missing_files:
            print_slow(stdscr, "Required files are missing. Setup cannot proceed.")
            print_slow(stdscr, f"Missing files: {', '.join(missing_files)}")
            return
        spin_loader(stdscr, "Checking files", duration=2)

        welcome_message = "Welcome to PyDOS!, press the Install PyDOS button.\n"
        create_message_box(stdscr, welcome_message)
        text_1 = "---Welcome to Pydos 2.0 Final Setup, This program has been updated a lot, which you can read in the Readme---"
        print_slow(stdscr, text_1)
        print_slow(stdscr, "BUILD: 2025TRMX")
        menu = ["Install PyDOS", "Exit"]
        while True:
            draw_menu(stdscr, current_row, menu)
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == 1:
                    return
                break

        print_center(stdscr, "Select Installation Path")
        install_path = select_install_path(stdscr)

        while True:
            print_center(stdscr, "Enter Name and Password")
            name, password = enter_name_and_password(stdscr)  # تغییر نام تابع
            if name and password:
                break
            menu = ["Retry", "Back"]
            current_row = 0
            print_slow(stdscr, "Information is Empty, Try Again.")
            while True:
                draw_menu(stdscr, current_row, menu)
                key = stdscr.getch()
                if key == curses.KEY_UP and current_row > 0:
                    current_row -= 1
                elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                    current_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if current_row == 1:
                        return
                    break

        if not license_agreement(stdscr):
            create_message_box(stdscr, "You must accept the license agreement to proceed.")
            return

        license_code = input_license_code(stdscr)

        print_center(stdscr, "SETUP IS CHECKING YOUR MEMORY...")
        check_memory(stdscr)

        display_readme(stdscr, base_path)

        print_center(stdscr, "SETUP IS FORMATTING INSTALLATION DIRECTORY...")
        format_directory(stdscr, install_path)
        
        print_center(stdscr, "SETUP IS SAVING YOUR ACCOUNT...")
        save_user_info(stdscr, name, password, install_path)
        
        print_center(stdscr, "SETUP IS CREATING DICTIONARIES...")
        create_directories(stdscr, install_path)

        print_center(stdscr, "SETUP IS COPYING SYSTEM FILES...")
        copy_files(stdscr, files, base_path, install_path)

        print_center(stdscr, "SETUP IS COPYING XC-GRUB...")
        print_slow(stdscr, "Setup is Copying the Bootloader...")
        copy_boot_file(stdscr, base_path, install_path)
        
        print_center(stdscr, "SETUP IS CONVERTING CACHE.TXT TO ACCOUNT.JSON...")
        convert_cache_to_json(stdscr, install_path)
        print_center(stdscr, "SETUP IS INSTALLING REQUIREMENTS...")
        install_requirements(stdscr, base_path)

        print_center(stdscr, "Setup Complete")
        setup_complete(stdscr)
        menu = ["Exit"]
        current_row = 0
        while True:
            print_slow(stdscr, "Setup is complete, I hope you enjoy this program. To run the program, please enter the folder and run XC-GRUB.")
            draw_menu(stdscr, current_row, menu)
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == 0:
                    return

    except Exception as e:
        create_message_box(stdscr, f"An error occurred: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main)