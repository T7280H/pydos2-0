import curses
import os

help = {
    "^X": "Exit",
    "^O": "Write Out",
    "^G": "Get Help",
    "^B": "Search",
    "^Space": "Save File"
}

# ثابت‌ها برای کدهای کلید
ENTER_KEY = 10
BACKSPACE_KEY = 127
ESC_KEY = 27
CTRL_X_KEY = 24
CTRL_O_KEY = 15
CTRL_G_KEY = 7
CTRL_B_KEY = 2
CTRL_SPACE_KEY = 0
UP_KEY = curses.KEY_UP
DOWN_KEY = curses.KEY_DOWN
LEFT_KEY = curses.KEY_LEFT
RIGHT_KEY = curses.KEY_RIGHT

def display_help(stdscr, height):
    """نمایش راهنمای کلیدها در پایین صفحه"""
    stdscr.addstr(height - 2, 2, "^X Exit  ^O Write Out  ^G Get Help  ^B Search  ^Space Save File", curses.color_pair(1))
    stdscr.clrtoeol()

def display_status(stdscr, message, height):
    """نمایش وضعیت در پایین صفحه"""
    stdscr.addstr(height - 1, 2, message[:curses.COLS - 4], curses.color_pair(2))
    stdscr.clrtoeol()

def load_file(file_name):
    """بارگذاری محتوای فایل"""
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            return file.readlines()
    return []

def save_file(file_name, text):
    """ذخیره محتوای فایل"""
    with open(file_name, 'w') as file:
        file.writelines(text)

def search_text(stdscr, text):
    """جستجوی کلمه در متن"""
    curses.echo()
    stdscr.addstr(curses.LINES - 1, 2, "Search: ")
    query = stdscr.getstr().decode('utf-8')
    curses.noecho()
    matches = []
    for i, line in enumerate(text):
        idx = line.find(query)
        if idx != -1:
            matches.append((i, idx, len(query)))
    return matches

def highlight_matches(stdscr, matches, offset_y, editor_height):
    """هایلایت کردن نتایج جستجو"""
    for y, x, length in matches:
        if offset_y <= y < offset_y + editor_height:
            stdscr.chgat(y - offset_y + 1, x + 7, length, curses.color_pair(3))

def show_help_screen(stdscr):
    """نمایش صفحه کمک"""
    stdscr.clear()
    stdscr.addstr(0, 0, "Help", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Key Bindings:")
    for i, (key, desc) in enumerate(help.items()):
        stdscr.addstr(4 + i, 2, f"{key}: {desc}", curses.color_pair(1))
    stdscr.addstr(curses.LINES - 1, 0, "Press any key to return", curses.color_pair(2))
    stdscr.refresh()
    stdscr.getch()

def main(stdscr, file_name):
    """تابع اصلی برای ویرایش متن"""
    curses.curs_set(1)  # نمایش مکان‌نما

    # تنظیم رنگ‌ها
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    # بارگذاری فایل
    text = load_file(file_name)
    if not text:
        text.append("")

    height, width = stdscr.getmaxyx()
    editor_height = height - 5
    editor_width = width - 4

    cursor_x = 0
    cursor_y = 0
    offset_y = 0
    matches = []

    while True:
        stdscr.clear()
        stdscr.box()
        stdscr.addstr(0, 2, " PyDOS Editor VER: 1.5.5 ", curses.color_pair(1))
        for i, line in enumerate(text[offset_y:offset_y + editor_height - 1]):
            stdscr.addstr(i + 1, 2, f"{offset_y + i + 1:4} {line[:editor_width - 6]}")
        display_help(stdscr, height)
        display_status(stdscr, f"File: {file_name} - {len(text)} lines", height)
        stdscr.move(cursor_y + 1, cursor_x + 7)
        highlight_matches(stdscr, matches, offset_y, editor_height)
        stdscr.refresh()

        key = stdscr.getch()

        if key == ENTER_KEY:
            text.insert(cursor_y + offset_y + 1, "")
            cursor_y += 1
            cursor_x = 0
        elif key == BACKSPACE_KEY:
            if cursor_x > 0:
                text[cursor_y + offset_y] = text[cursor_y + offset_y][:cursor_x - 1] + text[cursor_y + offset_y][cursor_x:]
                cursor_x -= 1
            elif cursor_y + offset_y > 0:
                cursor_x = len(text[cursor_y + offset_y - 1])
                text[cursor_y + offset_y - 1] += text.pop(cursor_y + offset_y)
                cursor_y -= 1
        elif key == CTRL_X_KEY:
            break
        elif key == CTRL_O_KEY or key == CTRL_SPACE_KEY:
            save_file(file_name, text)
            display_status(stdscr, "File saved", height)
            stdscr.getch()
        elif key == CTRL_G_KEY:
            show_help_screen(stdscr)
        elif key == CTRL_B_KEY:
            matches = search_text(stdscr, text)
            if matches:
                cursor_y, cursor_x = matches[0][0] - offset_y, matches[0][1]
            else:
                display_status(stdscr, "No matches found", height)
                stdscr.getch()
        elif key == UP_KEY:
            if cursor_y > 0:
                cursor_y -= 1
            elif offset_y > 0:
                offset_y -= 1
        elif key == DOWN_KEY:
            if cursor_y < editor_height - 1:
                cursor_y += 1
            elif offset_y + editor_height - 1 < len(text):
                offset_y += 1
        elif key == LEFT_KEY:
            if cursor_x > 0:
                cursor_x -= 1
            elif cursor_y + offset_y > 0:
                cursor_y -= 1
                cursor_x = len(text[cursor_y + offset_y])
        elif key == RIGHT_KEY:
            if cursor_x < len(text[cursor_y + offset_y]):
                cursor_x += 1
            elif cursor_y + offset_y + 1 < len(text):
                cursor_y += 1
                cursor_x = 0
        else:
            text[cursor_y + offset_y] = text[cursor_y + offset_y][:cursor_x] + chr(key) + text[cursor_y + offset_y][cursor_x:]
            cursor_x += 1

        if cursor_x >= editor_width - 6:
            cursor_x = 0
            cursor_y += 1

        if cursor_y >= editor_height:
            cursor_y = editor_height - 1
            offset_y += 1

def edit_command(file_name):
    """اجرای ویرایشگر"""
    curses.wrapper(main, file_name)

if __name__ == "__main__":
    file_name = input("Enter the file name to edit: ")
    edit_command(file_name)
