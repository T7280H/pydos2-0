import curses
from rich.console import Console
from rich.table import Table

commands = {
    "backup": "Backup all files",
    "bashrc": "Bash Converter",
    "bomb": "Run SMS bomber (pybomb.py in apps folder)",
    "bootinf": "Show boot version",
    "calc": "Calculator Usage: [-t] Text UI [-u] Graphical UI curses",
    "cd": "Change directory",
    "cls": "Clear the screen",
    "date": "Show date",
    "defpath": "Show current directory path",
    "dir": "List directories",
    "echo": "Print a message",
    "edit": "Text editor",
    "exit": "Exit PyDOS",
    "help": "Display command help",
    "ifconfig": "Show IP address",
    "ipfinder": "Find IP information",
    "mkdir": "Create directory",
    "ping": "Ping test",
    "pyrun": "Run Python applications",
    "rd": "Remove file or directory",
    "reminder": "Set a reminder",
    "restore": "Restore all files",
    "setting": "Config settings",
    "time": "Show time",
    "tracker": "IP Tracker",
    "unzip": "Unzip a file",
    "wenda": "Run Wenda Converter", 
    "dash": "Dashborad", 
    "xcopy": "Copy files",
    "zip": "ZIP a file", 
    "rename": "Rename a File", 
    "partest": "Check the All Folder and Files", "touch": "Create a Empty File", 
    "mv": "Move the File in Folder", 
    "cat": "[-s] Show the file [-c] Connect the file", 
    "reset": "Restart the Pydos"
}

def help_command(stdscr):
    curses.curs_set(0)  # Hide cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    h, w = stdscr.getmaxyx()
    console = Console(record=True, width=w-4)

    table = Table(title="PyDOS Commands", show_header=True, header_style="bold cyan")
    table.add_column("Command", style="bold yellow", justify="left")
    table.add_column("Description", style="bold white", justify="left")

    for command, description in sorted(commands.items()):
        table.add_row(command, description)

    console.print(table)
    result = console.export_text()

    lines = result.split('\n')
    max_lines = h - 4
    start_line = 0
    search_query = ""

    while True:
        stdscr.clear()
        stdscr.border(0)
        stdscr.addstr(0, 2, " PyDOS Commands ", curses.color_pair(1) | curses.A_BOLD)
        for i, line in enumerate(lines[start_line:start_line+max_lines], start=1):
            if i == 1:  # Header line
                stdscr.addstr(i, 2, line[:w-4], curses.color_pair(1) | curses.A_BOLD)
            elif i % 2 == 0:
                stdscr.addstr(i, 2, line[:w-4], curses.color_pair(2))
            else:
                stdscr.addstr(i, 2, line[:w-4], curses.color_pair(3))
        
        stdscr.addstr(h-2, 2, "Search: ", curses.color_pair(1))
        stdscr.addstr(h-2, 10, " " * (w-12))
        stdscr.addstr(h-2, 10, search_query, curses.color_pair(3))
        stdscr.addstr(h-1, 2, "Press Ctrl+X to exit. Use arrow keys to navigate.", curses.color_pair(1))
        
        stdscr.refresh()
        key = stdscr.getch()

        if key in [curses.KEY_DOWN, ord('j')]:
            if start_line + max_lines < len(lines):
                start_line += 1
        elif key in [curses.KEY_UP, ord('k')]:
            if start_line > 0:
                start_line -= 1
        elif key == 24:  # Ctrl+X
            break
        elif key == curses.KEY_BACKSPACE or key == 127:
            search_query = search_query[:-1]
        elif key == 10:  # Enter
            filtered_commands = {k: v for k, v in commands.items() if search_query.lower() in k.lower()}
            lines = [f"{k} : {v}" for k, v in sorted(filtered_commands.items())]
            start_line = 0
        elif 32 <= key <= 126:  # Printable characters
            search_query += chr(key)
            filtered_commands = {k: v for k, v in commands.items() if search_query.lower() in k.lower()}
            lines = [f"{k} : {v}" for k, v in sorted(filtered_commands.items())]
            start_line = 0
            
         
def help_body():
    curses.wrapper(help_command)

if __name__ == "__main__":
    help_body()