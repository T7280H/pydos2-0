import socket
import platform
import psutil
import curses

def gather_system_info():
    """جمع‌آوری اطلاعات سیستم"""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = platform.system() + " " + platform.release()
    cpu_info = platform.processor() or "Unknown"
    ram_info = f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 1)} GB"
    cpu_usage = f"{psutil.cpu_percent()}%"
    ram_usage = f"{psutil.virtual_memory().percent}%"

    return (
        f"Hostname: {hostname}\n"
        f"IP Address: {ip_address}\n"
        f"OS: {os_info}\n"
        f"Processor: {cpu_info}\n"
        f"RAM: {ram_info} ({ram_usage} used)\n"
        f"CPU Usage: {cpu_usage}"
    )

def display_system_info(stdscr, system_info):
    """نمایش اطلاعات سیستم"""
    h, w = stdscr.getmaxyx()  # دریافت ارتفاع و عرض پنجره

    stdscr.clear()
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(1, 2, "System Information")
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(2, 2, system_info)
    stdscr.attroff(curses.color_pair(3))
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(h - 2, 2, "Press Ctrl+X to exit.")
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()

def dash_command(stdscr):
    """تابع اصلی برای نمایش داشبورد"""
    curses.curs_set(0)  # پنهان کردن نشانگر
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    try:
        # جمع‌آوری اطلاعات سیستم
        system_info = gather_system_info()

        # نمایش اطلاعات سیستم
        display_system_info(stdscr, system_info)

        stdscr.getch()  # منتظر فشار کلید

    except Exception as e:
        h, _ = stdscr.getmaxyx()  # دریافت ارتفاع پنجره
        stdscr.addstr(h - 2, 2, f"Error: {e}", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()  # منتظر فشار کلید

def dashboard_command():
    """اجرای داشبورد"""
    curses.wrapper(dash_command)

if __name__ == "__main__":
    dashboard_command()