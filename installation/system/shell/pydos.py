import sys
import os
import time
import colorama
from colorama import Fore, Style, Back
from cmd import Cmd
from rich.progress import Progress
from rich.console import Console
import readline
import subprocess
import json
import getpass

# Add the path to the dev folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import commands from the dev folder
from losk.exit import exit_command
from losk.dir import dir_command
from losk.ping import ping_command
from losk.calc import calc_command
from losk.date import date_command
from losk.edit import edit_command
from losk.find import find_command
from losk.help import help_body
from losk.mkdir import mkdir_command
from losk.rd import rd_command
from losk.time import time_command
from losk.ver import ver_command
from losk.backup import backup_command
from losk.restore import restore_command
from losk.reminder import reminder_command
from losk.cIP import cIP_command
from losk.ifconfig import ifconfig_command
from losk.appmgr import appmgr_command
from losk.bomb import bomb_command
from losk.pyrun import pyrun_command
from losk.cls import cls_command
from losk.echo import echo_command
from losk.bootinf import bootinf_command
from losk.defpath import defpath_command
from losk.cd import cd_command
from losk.dash import dashboard_command
from losk.xcopy import xcopy_command
from losk.zip import zip_command
from losk.unzip import unzip_command
from losk.setting import setting_body
from losk.wenda import wenda_command
from losk.bashrc import bashrc_command
from losk.ipfinder import ipfinder_command
from losk.tracker import tracker_command
from losk.rename import rename_command
from losk.partest import partest_command
from losk.touch import touch_command
from losk.mv import mv_command
from losk.cat import cat_command

console = Console()

def load_banner():
    """Load and execute the load_banner function from the specified banner file."""
    try:
        # مسیر پوشه‌ی بنر و فایل‌های مربوطه
        banner_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'banner'))
        current_banner_path = os.path.join(banner_dir, 'current_banner.txt')

        # خواندن نام فایل بنر از current_banner.txt
        with open(current_banner_path, 'r') as f:
            banner_file = f.read().strip()
        banner_path = os.path.join(banner_dir, banner_file)

        # خواندن محتوای فایل پایتونی و اجرای آن
        with open(banner_path, 'r') as f:
            banner_code = f.read()

        # ایجاد یک دیکشنری برای محیط امن اجرا
        exec_globals = {}
        exec(banner_code, exec_globals)

        # اجرای تابع load_banner اگر در فایل وجود داشته باشد
        if 'load_banner' in exec_globals and callable(exec_globals['load_banner']):
            exec_globals['load_banner']()
        else:
            console.print("[bold red]Error:[/bold red] No valid load_banner function found in the file.")

    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] Banner file not found.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] An error occurred while loading the banner: {e}")

def check_account(login, password):
    """Verify the login credentials by checking the account information from account.json."""
    account_file = os.path.join('Config', 'account.json')  # مسیر فایل account.json در فولدر Config
    
    if not os.path.exists(account_file):
        console.print("[bold yellow]Warning: account.json file not found![/bold yellow]")
        # از کاربر بخواهید که ادامه دهد یا تلاش کند
        choice = input("Do you want to continue without login? (y/n): ").strip().lower()
        if choice == 'n':
            console.print("[bold red]Exiting program...[/bold red]")
            time.sleep(2)
            sys.exit(0)  # در صورت عدم تمایل به ادامه، برنامه خاتمه می‌یابد
        else:
            console.print("[bold green]Continuing without login.[/bold green]")
            time.sleep(2)
            colorama.init()
            PyDOSCmd().cmdloop()
            colorama.deinit()  # برای اینکه اجازه دهد ادامه دهد

    with open(account_file, 'r') as file:
        account_data = json.load(file)
    
    # بررسی نام کاربری و رمز عبور با تبدیل به حروف کوچک و حذف فاصله‌های اضافی
    if account_data["login"].strip().lower() == login.strip().lower() and account_data["password"].strip() == password.strip():
        return True
    return False

def login():
    """Prompt user for login credentials and verify."""
    console.print("[bold yellow]----PYDOS LOGIN----[/bold yellow]")
    login = input("Login: ")
    password = getpass.getpass("Password: ")
    
    if check_account(login, password):
        console.print(f"[bold yellow]Login Successful!, WELCOME {login}[/bold yellow]")
        time.sleep(2)
    
    else:
        console.print("[bold red]**ERR**: LOGIN FAILED[/bold red]")
        time.sleep(2)
        sys.exit(0)

class PyDOSCmd(Cmd):
    prompt = Back.BLUE + Fore.WHITE + f'PyDOS\\{os.path.basename(os.getcwd())}> ' + Style.RESET_ALL
    intro = Fore.GREEN + 'PyDOS 2.0 FINAL | PYTHON CMD PROJECT' + Style.RESET_ALL
    gulie = Fore.BLUE + 'TO SEE COMMAND TYPE (help)' + Style.RESET_ALL

    def preloop(self):
        load_banner()

    def do_exit(self, line):
        """Exit the PyDOS application."""
        exit_command()
        return True

    def do_dir(self, line):
        """List directory contents."""
        try:
            dir_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_ping(self, line):
        """Ping a specified address."""
        try:
            with Progress() as progress:
                task = progress.add_task("[cyan]Pinging...", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    ping_command(line)
                    break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_calc(self, line):
        """Calc Command"""
        try:
            args = line.split()
            if len(args) < 2:
                raise ValueError("Usage: calc -t <expression> or calc -u start")
                
            sys.argv = ["calc"] + args
            calc_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_date(self, line):
        """Display the current date."""
        try:
            date_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_edit(self, line):
        """Edit a file."""
        try:
            edit_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_find(self, line):
        """Find a file or directory."""
        try:
            find_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_help(self, line):
        """Display help information."""
        try:
            help_body()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_mkdir(self, line):
        """Create a new directory."""
        try:
            mkdir_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_rd(self, arg):
        """Remove a file or directory."""
        if not arg:
            console.print("[bold red]Error:[/bold red] Please specify a file or directory to remove.")
        else:
            try:
                rd_command(arg)
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

    def do_time(self, line):
        """Display the current time."""
        try:
            time_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_ver(self, line):
        """Display version information."""
        try:
            ver_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_restore(self, line):
        """Restore from a backup."""
        args = line.split()
        if len(args) < 1:
            console.print("[bold red]Error:[/bold red] No restore path provided.")
        else:
            restore_path = args[0]
            try:
                restore_command(restore_path)
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

    def do_reminder(self, line):
        """Set a reminder with a message and delay."""
        args = line.split()
        if len(args) < 2:
            console.print("[bold red]Error:[/bold red] Please provide both a message and a delay.")
        else:
            message = args[0]
            try:
                delay = int(args[1])
                reminder_command(message, delay)
            except ValueError:
                console.print("[bold red]Error:[/bold red] Delay must be an integer.")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

    def do_cIP(self, line):
        """Change IP address."""
        try:
            cIP_command(line)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_ifconfig(self, line):
        """Display network configuration."""
        try:
            ifconfig_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_appmgr(self, line):
        """Manage applications."""
        args = line.split()
        if len(args) < 2:
            console.print("[bold red]Error:[/bold red] Please provide both the application name and the action.")
        else:
            try:
                appmgr_command(args[0], args[1])
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

    def do_bomb(self, line):
        """Trigger a bomb command (use with caution)."""
        try:
            bomb_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_pyrun(self, line):
        """Run a Python script."""
        try:
            pyrun_command(line)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_cls(self, line):
        """Clear the screen."""
        try:
            cls_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_echo(self, line):
        """Echo a message."""
        try:
            echo_command(line)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_bootinf(self, line):
        """Display boot information."""
        try:
            bootinf_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_cd(self, line):
        """Change directory."""
        try:
            os.chdir(line)
            self.prompt = Back.RED + Fore.BLACK + f'PyDOS\\{os.path.basename(os.getcwd())}> ' + Style.RESET_ALL
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_defpath(self, line):
        """Set default path."""
        try:
            defpath_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_dash(self, line):
        """Display dashboard."""
        try:
            dashboard_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_backup(self, line):
        """Backup files."""
        args = line.split()
        if len(args) < 2:
            console.print("[bold red]Error:[/bold red] Please provide both source and destination.")
        else:
            try:
                backup_command(args[0], args[1])
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

    def do_xcopy(self, line):
        """Copy files."""
        args = line.split()
        if len(args) < 2:
            console.print("[bold red]Error:[/bold red] Please provide both source and destination.")
        else:
            try:
                xcopy_command(args[0], args[1])
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

    def do_setting(self, line):
        """Display settings."""
        try:
            setting_body()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_zip(self, line):
        """Zip files."""
        args = line.split()
        if len(args) < 2:
            console.print("[bold red]Error:[/bold red] You need to provide both source and destination.")
            return

        source = args[0]
        destination = args[1]

        try:
            zip_command(source, destination)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_unzip(self, line):
        """Unzip files."""
        args = line.split()
        if len(args) < 2:
            console.print("[bold red]Error:[/bold red] You need to provide both source and destination.")
            return

        source = args[0]
        destination = args[1]

        try:
            unzip_command(source, destination)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_wenda(self, line):
        """Run Wenda command."""
        try:
            subprocess.run(['clear'])
            wenda_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_bashrc(self, line):
        """Run Bashrc command."""
        try:
            subprocess.run(['clear'])
            bashrc_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_ipfinder(self, line):
        """Run IP Finder command."""
        try:
            subprocess.run(['clear'])
            ipfinder_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_tracker(self, line):
        """Run Tracker command."""
        try:
            subprocess.run(['clear'])
            tracker_command()
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_rename(self, line):
        """Rename a file or directory."""
        try:
            args = line.split()  # Convert input to list
            rename_command(args)  # Send to rename function
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    def do_partest(self, line):
        '''Checking the Folder'''
        try:
            args = line.split()
            partest_command(args)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            
    def do_touch(self, line):
        try:
            args = line.split()
            touch_command(args)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            
    def do_mv(self, line):
        try:
            args = line.split()
            mv_command(args)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            
    def do_cat(self, line):
        try:
            args = line.split()
            cat_command(args)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            
    def do_reset(self, line):
        try:
            console.print("[bold yellow]Restarting Pydos Without Login....")
            time.sleep(2)
            colorama.init()
            PyDOSCmd().cmdloop()
            colorama.deinit()
        except Exception as e:
            console.print("[bold red]**KERNEL PANIC**: RESET COMMAND DAMAGED.")
            time.sleep(1)
            console.print(f"log: {e}")

    def complete(self, text, state):
        """Auto-complete commands."""
        commands = [command[3:] for command in dir(self.__class__) if command.startswith('do_')]
        matches = [command for command in commands if command.startswith(text)]
        try:
            return matches[state]
        except IndexError:
            return None

    def default(self, line):
        """Handle unknown commands."""
        console.print(f"[bold red]Error:[/bold red] Unknown command: {line}")

if __name__ == '__main__':
    colorama.init()
    login()
    PyDOSCmd().cmdloop()
    colorama.deinit()
