import os
import time
import sys
import pyfiglet
import curses
from curses import textpad
from rich.console import Console
from rich.progress import Progress, BarColumn, SpinnerColumn

console = Console()

# پاک کردن صفحه
console.clear()

# لیست فایل‌ها و فولدرهای حیاتی
critical_files = ["shell/pydos.py"]
critical_folders = ["losk", "shell", "application"]

missing_files = []
missing_folders = []

# بررسی فایل‌ها و فولدرها
console.print("[bold cyan]CHECKING SYSTEM FILES...[/bold cyan]")

with console.status("[bold yellow]Checking files and folders...[/bold yellow]"):
    for item in critical_files + critical_folders:
        path = os.path.join(os.getcwd(), item)
        
        if item in critical_files and not os.path.exists(path):
            missing_files.append(item)
        
        elif item in critical_folders and (not os.path.isdir(path) or not os.listdir(path)):
            missing_folders.append(item)

    time.sleep(0.8)  # شبیه‌سازی پردازش سریع‌تر

# نمایش نتیجه بررسی
if missing_files or missing_folders:
    console.print("\n[bold red]Error! Missing files or folders:[/bold red]")
    if missing_files:
        console.print(f"[red]Missing files:[/red] {', '.join(missing_files)}")
    if missing_folders:
        console.print(f"[red]Missing or empty folders:[/red] {', '.join(missing_folders)}")
        for folder in missing_folders:
            os.makedirs(folder, exist_ok=True)  # فولدرهای گمشده را ایجاد می‌کند
            console.print(f"[bold green]✔ Created missing folder:[/bold green] {folder}")

    console.print("[bold yellow]Boot aborted! Please restore the missing files.[/bold yellow]")
    sys.exit(1)

console.print("\n[green]✔ All files and folders OK![/green]")

# نمایش بنر
banner = pyfiglet.figlet_format("XC-GRUB", font="slant")
console.print(f"[bold magenta]{banner}[/bold magenta]")

# نمایش لودینگ زیبا
console.print("\n[bold yellow]Loading the Bootloader...[/bold yellow]\n")

with Progress(SpinnerColumn(), BarColumn(), console=console) as progress:
    task = progress.add_task("", total=100)
    for _ in range(100):
        time.sleep(0.015)  # لودینگ سریع‌تر
        progress.update(task, advance=1)

# گزینه‌های منو
menu_items = ["PYDOS 2.0 FINAL", "SHUTDOWN"]

def menu(stdscr):
    curses.curs_set(0)  # مخفی کردن مکان‌نما
    curses.start_color()
    
    # تعریف رنگ‌ها
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # پس‌زمینه‌ی خاکستری (شبیه‌سازی با سفید و مشکی)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)   # انتخاب‌های منو با پس‌زمینه‌ی آبی
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)    # رنگ قرمز برای پیام‌های خطا

    selected_index = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # تنظیم پس‌زمینه‌ی کل صفحه به رنگ خاکستری
        stdscr.bkgd(' ', curses.color_pair(1))

        box = [[3, 3], [h-6, w-3]]
        textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
        
        title = "XC-GRUB BOOTLOADER"
        stdscr.addstr(1, w//2 - len(title)//2, title, curses.A_BOLD | curses.color_pair(1))

        # اضافه کردن فلش متحرک برای گزینه‌ها
        for i, item in enumerate(menu_items):
            x = w//2 - len(f"[{i+1}] {item}")//2
            y = h//2 - len(menu_items)//2 + i
            if i == selected_index:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, f"-->[{i+1}] {item} ", curses.A_BOLD)  # فلش اضافه شده
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(y, x, f"[{i+1}] {item}")

        # توضیح پایین منو
        desc = "Use arrow keys to navigate, Enter to select."
        stdscr.addstr(h-4, w//2 - len(desc)//2, desc, curses.A_BOLD | curses.color_pair(1))

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(menu_items) - 1:
            selected_index += 1
        elif key == 10:  # Enter key
            return selected_index

# اجرای منو
choice = curses.wrapper(menu)

# اجرای گزینه انتخاب‌شده
console.clear()
if choice == 0:
    console.print("\n[bold cyan]Booting PYDOS 2.0 FINAL...[/bold cyan]")
    time.sleep(2)
    os.system("python shell/pydos.py") 
elif choice == 1:
    console.print("\n[bold red]Shutting down...[/bold red]")
    time.sleep(2)
    sys.exit(0)