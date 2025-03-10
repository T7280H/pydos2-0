import curses
import sys

def calculator_gui(stdscr):
    curses.curs_set(0)  # مخفی کردن نشانگر
    stdscr.clear()
    curses.start_color()

    # تعریف رنگ‌ها
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_GREEN)   # اعداد
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)    # عملگرها
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_GREEN)    # دکمه C (متن قرمز)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)  # دکمه =
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)  # دکمه انتخاب‌شده (پس‌زمینه سفید)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)   # کادر نمایش عبارت

    options = ["7", "8", "9", "/", 
               "4", "5", "6", "*", 
               "1", "2", "3", "-", 
               "0", "C", "=", "+"]

    rows, cols = 4, 4
    selected = 0
    expression = ""

    button_width = 7   # عرض دکمه
    button_height = 3  # ارتفاع دکمه
    padding = 2        # فاصله بین دکمه‌ها
    expr_width = 30    # عرض کادر نمایش اعداد

    while True:
        stdscr.clear()

        # دریافت اندازه صفحه‌نمایش
        height, width = stdscr.getmaxyx()

        # محاسبه مکان شروع برای نمایش وسط صفحه
        calc_width = cols * (button_width + padding)
        calc_height = rows * (button_height + padding) + 4  # 4 خط برای نمایش محاسبات

        start_x = (width - calc_width) // 2
        start_y = (height - calc_height) // 2

        # محاسبه مکان شروع کادر نمایش اعداد
        expr_x = start_x + (calc_width - expr_width) // 2
        expr_y = start_y - 3  # کمی بالاتر از دکمه‌ها

        # رسم کادر برای نمایش اعداد
        stdscr.attron(curses.color_pair(6))  # فعال کردن رنگ کادر
        stdscr.addstr(expr_y, expr_x, "+" + "-" * (expr_width - 2) + "+")
        stdscr.addstr(expr_y + 1, expr_x, "|" + " " * (expr_width - 2) + "|")
        stdscr.addstr(expr_y + 2, expr_x, "+" + "-" * (expr_width - 2) + "+")
        stdscr.attroff(curses.color_pair(6))  # غیرفعال کردن رنگ کادر

        # نمایش عبارت داخل کادر
        stdscr.addstr(expr_y + 1, expr_x + 2, expression[:expr_width - 4], curses.A_BOLD)

        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                x = start_x + j * (button_width + padding)
                y = start_y + i * (button_height + padding)

                # تعیین رنگ مناسب برای دکمه‌ها (پس‌زمینه سبز)
                if options[index].isdigit():
                    color = curses.color_pair(1)  # آبی روی سبز
                elif options[index] in ["+", "-", "*", "/"]:
                    color = curses.color_pair(2)  # قرمز روی سبز
                elif options[index] == "C":
                    color = curses.color_pair(3)  # قرمز روی سبز
                elif options[index] == "=":
                    color = curses.color_pair(4)  # مشکی روی سبز
                else:
                    color = curses.A_NORMAL

                # اگر دکمه انتخاب شده است، پس‌زمینه سفید شود
                if index == selected:
                    if options[index] == "C":
                        color = curses.color_pair(3) | curses.A_BOLD  # متن قرمز روی سبز
                    else:
                        color = curses.color_pair(5)  # مشکی روی سفید

                # نمایش دکمه‌ها در مرکز صفحه
                stdscr.addstr(y, x, " " * button_width, color)
                stdscr.addstr(y + 1, x, f"  {options[index]}  ", color)
                stdscr.addstr(y + 2, x, " " * button_width, color)

        # دریافت ورودی کلید از کاربر
        key = stdscr.getch()

        # اگر کاربر دکمه ESC را فشار دهد، از حالت گرافیکی خارج می‌شود
        if key == 27:  # 27 کد کلید ESC است
            break

        if key == curses.KEY_RIGHT and (selected % cols) < (cols - 1):
            selected += 1
        elif key == curses.KEY_LEFT and (selected % cols) > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected + cols < len(options):
            selected += cols
        elif key == curses.KEY_UP and selected - cols >= 0:
            selected -= cols
        elif key == 10:  # Enter
            choice = options[selected]
            if choice == "=":
                try:
                    expression = str(eval(expression))
                except:
                    expression = "Error"
            elif choice == "C":
                expression = ""
            else:
                expression += choice

        stdscr.refresh()

def calc_command():
    if len(sys.argv) < 3:
        print("Usage: calc -t <expression> or calc -u start")
        return
    
    if sys.argv[1] == "-t":
        expression = sys.argv[2]
        try:
            result = eval(expression)
            print(f"Result: {result}")
        except:
            print("Invalid expression")
    elif sys.argv[1] == "-u" and sys.argv[2] == "start":
        print("Running graphical interface with curses...")
        curses.wrapper(calculator_gui)
    else:
        print("Invalid argument")

if __name__ == "__main__":
    calc_command()