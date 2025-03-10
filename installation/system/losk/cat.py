import os
import sys
from rich.console import Console
import argparse

console = Console()

def cat_command(args):
    if len(args) == 0:
        console.print("[bold red]Usage:[/bold red] cat <file_name> [-s] or [-c <file_to_append>]")
        return

    # استفاده از argparse برای پردازش سوئیچ‌ها
    parser = argparse.ArgumentParser(description="Display or concatenate files.")
    parser.add_argument("file_name", help="The file to display or concatenate.")
    parser.add_argument("-s", "--show", action="store_true", help="Show the content of the file")
    parser.add_argument("-c", "--concat", metavar="file_to_append", help="Concatenate the content of another file")
    
    # پردازش آرگومان‌ها
    args = parser.parse_args(args)

    if not os.path.exists(args.file_name) or not os.path.isfile(args.file_name):
        console.print(f"[bold red]Error:[/bold red] '{args.file_name}' is not a valid file.")
        return

    if args.show:  # سوئیچ -s برای نمایش محتوا
        try:
            with open(args.file_name, 'r') as file:
                console.print(file.read())
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    if args.concat:  # سوئیچ -c برای وصل کردن محتوا
        if not os.path.exists(args.concat) or not os.path.isfile(args.concat):
            console.print(f"[bold red]Error:[/bold red] '{args.concat}' is not a valid file to append.")
            return
        try:
            with open(args.file_name, 'a') as file:
                with open(args.concat, 'r') as file_to_append:
                    file.write(file_to_append.read())
            console.print(f"[bold green]Successfully appended content from '{args.concat}' to '{args.file_name}'[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    cat_command(sys.argv[1:])