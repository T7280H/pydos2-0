import os
import re
import sys
import time
import pyfiglet
from colorama import Fore, Style, init
from rich.console import Console
from rich.progress import track
from rich.panel import Panel

# Initialize colorama for automatic reset of colors
init(autoreset=True)
console = Console()

def animated_text(text, color=Fore.YELLOW, delay=0.05):
    """Print text with animation effect."""
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_separator():
    """Print a stylish separator line."""
    console.print("[cyan]" + "=" * 50 + "[/cyan]")

def convert_assignment(line):
    """Convert Bash variable assignment to Python assignment."""
    match = re.match(r'^(\w+)=(".*?"|\'.*?\'|.+)$', line)
    if match:
        var, value = match.groups()
        value = value.strip()
        if value.startswith(('"', "'")) and value.endswith(('"', "'")):
            unquoted = value[1:-1]
        else:
            unquoted = value
        if re.match(r'^\d+(\.\d+)?$', unquoted):
            return f"{var} = {unquoted}"
        else:
            return f'{var} = "{unquoted}"'
    return line

def convert_if_statement(line):
    """Convert Bash if statement to Python if statement."""
    line = re.sub(r'\s*(.*)\s*==\s*(.*)\s*', r'\1 == \2', line)
    line = line.replace("-eq", "==").replace("-ne", "!=").replace("-lt", "<").replace("-le", "<=").replace("-gt", ">").replace("-ge", ">=")
    line = line.replace("if ", "if ").replace("elif ", "elif ").replace("else", "else:")
    return line

def convert_for_loop(line):
    """Convert Bash for loop to Python for loop."""
    match = re.match(r'for\s+(\w+)\s+in\s+(.*);', line)
    if match:
        var, iterable = match.groups()
        iterable = iterable.replace("$(seq ", "range(").replace(")", ")")
        return f"for {var} in {iterable}:"
    return line

def convert_while_loop(line):
    """Convert Bash while loop to Python while loop."""
    line = re.sub(r'while\s+\s*(.*)\s*', r'while \1:', line)
    return line

def convert_echo(line):
    """Convert Bash echo statement to Python print statement."""
    match = re.match(r'echo\s+(.*)', line)
    if match:
        return f'print({match.group(1)})'
    return line

def convert_cd(line):
    """Convert Bash cd command to Python os.chdir statement."""
    match = re.match(r'cd\s+(.*)', line)
    if match:
        return f'os.chdir({match.group(1)})'
    return line

def convert_exit(line):
    """Convert Bash exit command to Python sys.exit statement."""
    match = re.match(r'exit\s*(.*)', line)
    if match:
        return f'sys.exit({match.group(1)})'
    return line

def convert_read(line):
    """Convert Bash read command to Python input statement."""
    match = re.match(r'read\s+(.*)', line)
    if match:
        return f'{match.group(1)} = input()'
    return line

def convert_figlet_to_pyfiglet(line):
    """Convert Bash figlet/toilet command to pyfiglet equivalent."""
    match = re.match(r'(figlet|toilet)\s+(.+)', line)
    if match:
        text = match.group(2).strip('"').strip("'")  # Remove surrounding quotes if present
        return f'print(pyfiglet.figlet_format("{text}"))'
    return line

def process_line(line):
    """Apply conversion functions to a given line."""
    line = line.strip()
    if not line or line.startswith("#"):
        return line
    line = convert_figlet_to_pyfiglet(line)
    if "=" in line:
        return convert_assignment(line)
    if line.startswith("if ") or line.startswith("elif ") or line.startswith("else"):
        return convert_if_statement(line)
    if line.startswith("for "):
        return convert_for_loop(line)
    if line.startswith("while "):
        return convert_while_loop(line)
    if line.startswith("echo "):
        return convert_echo(line)
    if line.startswith("cd "):
        return convert_cd(line)
    if line.startswith("exit"):
        return convert_exit(line)
    if line.startswith("read "):
        return convert_read(line)
    return line

def convert_bash_to_python(bash_code):
    """Convert the entire Bash code into Python code."""
    lines = bash_code.splitlines()
    python_lines = ['import sys', 'import os', 'import re', 'import time', 'import pyfiglet']
    indent_level = 0

    for raw_line in track(lines, description="Processing..."):
        stripped_line = raw_line.strip()
        if stripped_line in ["fi", "done", "}"]:
            indent_level = max(indent_level - 1, 0)
            continue
        converted_line = process_line(raw_line)
        if not converted_line.strip():
            continue
        python_lines.append("    " * indent_level + converted_line)
        if converted_line.rstrip().endswith(":"):
            indent_level += 1

    return "\n".join(python_lines)

def main():
    console.clear()
    ascii_banner = pyfiglet.figlet_format("Bash Converter")
    console.print(Panel(ascii_banner, style="cyan", expand=False))
    animated_text("BASH CONVERTER VERSION 1.5 | PYDOS APPS\n", Fore.MAGENTA)

    while True:
        print_separator()
        console.print("[bold green]1- Bash Converter[/bold green]")
        console.print("[bold red]2- Exit[/bold red]")
        print_separator()
        choice = input(Fore.CYAN + "Select an option: " + Style.RESET_ALL).strip()

        if choice == "1":
            print_separator()
            file_path = input(Fore.YELLOW + "Enter Bash file path (file.sh): " + Style.RESET_ALL).strip()
            print_separator()

            if not os.path.exists(file_path):
                console.print("[bold red]File not found![/bold red]")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    bash_code = file.read()
            except Exception as e:
                console.print(f"[bold red]Error reading file: {e}[/bold red]")
                continue

            console.print("[bold cyan]Processing file...[/bold cyan]")
            print_separator()
            python_code = convert_bash_to_python(bash_code)

            output_file = "file.py"
            try:
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(python_code)
                console.print(f"\n[bold green]Converted code saved in {output_file}.[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error writing output file: {e}[/bold red]")

        elif choice == "2":
            print_separator()
            animated_text("Exiting...", Fore.RED)
            print_separator()
            time.sleep(2)
            os.system('clear')
            break
        else:
            console.print("[bold red]Invalid option! Please try again.[/bold red]")

if __name__ == "__main__":
    main()