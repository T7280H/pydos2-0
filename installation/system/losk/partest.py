import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def partest_command(args):
    if len(args) != 1:
        console.print("Usage: partest <directory>")
        return

    directory = args[0]

    if not os.path.isdir(directory):
        console.print(f"Error: '{directory}' is not a valid directory.")
        return

    def check_directory(directory, depth=0):
        indent = "  " * depth
        console.print(f"\nChecking The Folder: {directory}...\n")
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                status = "[CHECKED]"
                status_color = "green"
                file_status = Text(f"{indent}{item} {status}")
                panel = Panel(file_status, expand=False)
                console.print(panel)
                check_directory(item_path, depth + 1)
            elif os.path.isfile(item_path):
                _, file_extension = os.path.splitext(item)
                if file_extension:
                    status = f"[EXT: {file_extension}]"
                    status_color = "blue"
                else:
                    status = "[ERROR]"
                    status_color = "red"
                file_status = Text(f"{indent}{item} {status}")
                panel = Panel(file_status, expand=False)
                console.print(panel)
            else:
                status = "[UNKNOWN]"
                status_color = "yellow"
                file_status = Text(f"{indent}{item} {status}")
                panel = Panel(file_status, expand=False)
                console.print(panel)

    try:
        check_directory(directory)
    except PermissionError:
        console.print("Error: Permission denied. Try running as administrator.")
    except FileNotFoundError:
        console.print(f"Error: '{directory}' not found.")
    except Exception as e:
        console.print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        partest_command(sys.argv[1:])
    else:
        console.print("Usage: partest <directory>")