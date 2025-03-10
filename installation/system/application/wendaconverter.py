import os
import re
import sys
import time
import ast
from rich.console import Console
from rich.progress import Progress

console = Console()

# ------------------------------------------------------------------
# AST-based Converter
# ------------------------------------------------------------------
class PythonToTargetConverter(ast.NodeVisitor):
    def __init__(self, target_lang: str):
        self.target_lang = target_lang
        self.result = ""
        self.indent_level = 0

    def indent(self) -> str:
        return "    " * self.indent_level

    def visit_Module(self, node: ast.Module):
        # در زبان‌هایی مانند Java و C# لازم است توابع را داخل یک کلاس قرار دهیم؛
        # اما در این نمونه، توابع به صورت مستقل تبدیل می‌شوند.
        for stmt in node.body:
            self.visit(stmt)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        func_name = node.name
        # پردازش پارامترها: فرض بر این است که تمام پارامترها از نوع int هستند (به جز در Ruby)
        params = []
        for arg in node.args.args:
            if self.target_lang == "Ruby":
                params.append(arg.arg)
            else:
                params.append("int " + arg.arg)
        param_str = ", ".join(params)

        if self.target_lang == "Ruby":
            header = f"def {func_name}({param_str})"
        elif self.target_lang in ["C", "C++"]:
            header = f"int {func_name}({param_str}) " + "{"
        elif self.target_lang in ["Java", "C#"]:
            header = f"public static int {func_name}({param_str}) " + "{"
        else:
            header = f"def {func_name}({param_str}):"

        self.result += self.indent() + header + "\n"
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        if self.target_lang == "Ruby":
            self.result += self.indent() + "end\n\n"
        elif self.target_lang in ["C", "C++", "Java", "C#"]:
            self.result += self.indent() + "}\n\n"
        else:
            self.result += "\n"

    def visit_Return(self, node: ast.Return):
        ret_val = self.visit(node.value) if node.value is not None else ""
        if self.target_lang in ["C", "C++", "Java", "C#"]:
            line = self.indent() + f"return {ret_val};\n"
        else:
            line = self.indent() + f"return {ret_val}\n"
        self.result += line

    def visit_Expr(self, node: ast.Expr):
        expr_str = self.visit(node.value)
        if self.target_lang in ["C", "C++", "Java", "C#"]:
            expr_str += ";"
        self.result += self.indent() + expr_str + "\n"

    def visit_Call(self, node: ast.Call):
        # پردازش توابع: به ویژه تابع print به صورت ویژه تبدیل می‌شود.
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            args_str = ", ".join([self.visit(arg) for arg in node.args])
            if self.target_lang == "Ruby":
                return f"puts {args_str}"
            elif self.target_lang in ["C", "C++"]:
                return f"printf({args_str})"
            elif self.target_lang in ["Java"]:
                return f"System.out.println({args_str})"
            elif self.target_lang == "C#":
                return f"Console.WriteLine({args_str})"
            else:
                return f"print({args_str})"
        else:
            func_name = self.visit(node.func)
            args_str = ", ".join([self.visit(arg) for arg in node.args])
            return f"{func_name}({args_str})"

    def visit_Name(self, node: ast.Name):
        return node.id

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, str):
            return f"\"{node.value}\""
        return str(node.value)

    def visit_Assign(self, node: ast.Assign):
        targets = ", ".join([self.visit(t) for t in node.targets])
        value = self.visit(node.value)
        if self.target_lang in ["C", "C++", "Java", "C#"]:
            line = self.indent() + f"int {targets} = {value};\n"
        else:
            line = self.indent() + f"{targets} = {value}\n"
        self.result += line

    def visit_BinOp(self, node: ast.BinOp):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return f"({left} {op} {right})"

    def visit_Add(self, node: ast.Add):
        return "+"

    def visit_Sub(self, node: ast.Sub):
        return "-"

    def visit_Mult(self, node: ast.Mult):
        return "*"

    def visit_Div(self, node: ast.Div):
        return "/"

    def visit_Mod(self, node: ast.Mod):
        return "%"

    def visit_If(self, node: ast.If):
        test = self.visit(node.test)
        if self.target_lang == "Ruby":
            line = self.indent() + f"if {test}\n"
        elif self.target_lang in ["C", "C++", "Java", "C#"]:
            line = self.indent() + f"if ({test}) " + "{\n"
        else:
            line = self.indent() + f"if {test}:\n"
        self.result += line
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1

        if node.orelse:
            if self.target_lang == "Ruby":
                self.result += self.indent() + "else\n"
            elif self.target_lang in ["C", "C++", "Java", "C#"]:
                self.result += self.indent() + "} else {\n"
            else:
                self.result += self.indent() + "else:\n"
            self.indent_level += 1
            for stmt in node.orelse:
                self.visit(stmt)
            self.indent_level -= 1

        if self.target_lang == "Ruby":
            self.result += self.indent() + "end\n"
        elif self.target_lang in ["C", "C++", "Java", "C#"]:
            self.result += self.indent() + "}\n"

    def visit_Compare(self, node: ast.Compare):
        left = self.visit(node.left)
        if node.ops and node.comparators:
            op = self.visit(node.ops[0])
            right = self.visit(node.comparators[0])
            return f"{left} {op} {right}"
        return left

    def visit_Eq(self, node: ast.Eq):
        return "=="

    def visit_NotEq(self, node: ast.NotEq):
        return "!="

    def visit_Lt(self, node: ast.Lt):
        return "<"

    def visit_LtE(self, node: ast.LtE):
        return "<="

    def visit_Gt(self, node: ast.Gt):
        return ">"

    def visit_GtE(self, node: ast.GtE):
        return ">="

    def visit_For(self, node: ast.For):
        # پشتیبانی از حلقه for به صورت: for var in range(start, stop, step)
        if (isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and
                node.iter.func.id == "range"):
            args = node.iter.args
            if len(args) == 1:
                start = "0"
                stop = self.visit(args[0])
                step = "1"
            elif len(args) == 2:
                start = self.visit(args[0])
                stop = self.visit(args[1])
                step = "1"
            elif len(args) == 3:
                start = self.visit(args[0])
                stop = self.visit(args[1])
                step = self.visit(args[2])
            else:
                start = "0"
                stop = "0"
                step = "1"
            var = self.visit(node.target)
            if self.target_lang == "Ruby":
                self.result += self.indent() + f"{var} = {start}\n"
                self.result += self.indent() + f"while {var} < {stop}\n"
            elif self.target_lang in ["C", "C++", "Java", "C#"]:
                self.result += self.indent() + f"for (int {var} = {start}; {var} < {stop}; {var} += {step}) " + "{\n"
            else:
                self.result += self.indent() + f"for {var} in range({start}, {stop}, {step}):\n"
            self.indent_level += 1
            for stmt in node.body:
                self.visit(stmt)
            self.indent_level -= 1
            if self.target_lang == "Ruby":
                self.result += self.indent() + "end\n"
            elif self.target_lang in ["C", "C++", "Java", "C#"]:
                self.result += self.indent() + "}\n"
        else:
            self.result += self.indent() + "// Unsupported for loop\n"

    def visit_While(self, node: ast.While):
        test = self.visit(node.test)
        if self.target_lang == "Ruby":
            self.result += self.indent() + f"while {test}\n"
        elif self.target_lang in ["C", "C++", "Java", "C#"]:
            self.result += self.indent() + f"while ({test}) " + "{\n"
        else:
            self.result += self.indent() + f"while {test}:\n"
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        if self.target_lang == "Ruby":
            self.result += self.indent() + "end\n"
        elif self.target_lang in ["C", "C++", "Java", "C#"]:
            self.result += self.indent() + "}\n"

    def generic_visit(self, node):
        # برای نودهایی که پیاده‌سازی نشده‌اند، از پیش‌فرض استفاده می‌کنیم.
        if isinstance(node, ast.expr):
            return ""
        return super().generic_visit(node)


def convert_ast_to_target(py_code: str, target_lang: str) -> str:
    """
    تبدیل کد پایتون به کد زبان مقصد با استفاده از AST.
    """
    try:
        tree = ast.parse(py_code)
    except Exception as e:
        return f"Error parsing Python code: {e}"
    converter = PythonToTargetConverter(target_lang)
    converter.visit(tree)
    return converter.result

# ------------------------------------------------------------------
# نمایش بنر، عنوان و منو
# ------------------------------------------------------------------
def display_banner() -> None:
    banner = r"""
                       ##%%#                                             ######                         
                        ########                                     *########                          
                         *#######***                              ************                          
                          ***************                     ***************                           
                          ++++*++++++++++++++             =++++++++++++++++++                           
                           +++++++++++++++++=---------------==++++++++++++++                            
                            ================================================                            
                            ==============---===============---============                             
                             ------===================================-----                             
                              ----+++++++++++++++++++++++++++++++++++++---                              
                              ::-++++++*@@***#@%*++++++++%@@%%@@@#++++++-:                              
                               :=****%@@*@@@@@%@@@*****@@@=@@@@#%@@%****+                               
                               +****%@@%%@@@@@@=@@@#**@@@#@@@@@@#@@@%****=                              
                               *****@@@*@@@@@@@#@@@%*#@@@=@@@@@@%@@@@*##*+                              
                               +#####@@@#@@@@@@=@@@###@@@@%@@@@@+@@@%####++                             
                          ##**++*##*#%@@@*@@@@-@@@#####@@@@*@@@+@@@#####*++***#*                        
                             ++++#%%+=#%%@@@@@@%%%%%%%%%%%@@@@@@%%%#-*%#=++**                           
                                 =*%%%%=:=#%%%%%%%%%%%%%%%%%%%%#=:*%%%*-                                
                                +==-%@%%%%#-#%*=---====-::-=*+=%@%=---===                               
                              +++==---#@@@@@@@@#+=++**+==*%@@%+#*::---===+++                            
                                        @@@@@@@@@@@@@@@@@@@@@%==-                                       
                                             **@@@@@@@@@@@*=                                            
                                              ::::::::::::::                                            
                                              --------------                                            
                                             ---------------                                            
                                             ----------------                                           
                                             ::---===========                                           
                                            ::-==============                                           
                                            ::-=+===+++++++++                                           
                                            :::--=++=++++++++                                           
                                           +++++++++++++++++++                                          
                                           +******************                                          
                                           *******************                                          
                                           *******************                                          
    """
    console.print(banner)

def display_title() -> None:
    title = "WENDA ADVANCED CONVERTER | PYDOS APPS"
    for char in title:
        console.print(f"[blue bold]{char}[/blue bold]", end="")
        sys.stdout.flush()
        time.sleep(0.05)
    console.print("\n")

def loading_animation(total: int = 100, advance: int = 20, delay: float = 0.5) -> None:
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing...", total=total)
        while not progress.finished:
            progress.update(task, advance=advance)
            time.sleep(delay)

def animated_menu() -> None:
    separator = "-" * 50
    console.print(separator)
    console.print("[bold cyan]Select a target language for conversion:[/bold cyan]")
    menu_items = [
        ("[green][1] C Converter[/green]", 0.1),
        ("[green][2] C++ Converter[/green]", 0.1),
        ("[green][3] C# Converter[/green]", 0.1),
        ("[green][4] Java Converter[/green]", 0.1),
        ("[green][5] Ruby Converter[/green]", 0.1),
        ("[red][6] Exit[/red]", 0.1)
    ]
    for item, delay in menu_items:
        console.print(item)
        time.sleep(delay)
    console.print(separator)

def get_paths() -> tuple[str | None, str | None]:
    file_path = input("Enter the path of the Python file: ").strip()
    if not os.path.exists(file_path):
        console.print("[red]File not found![/red]")
        return None, None
    output_path = input("Enter the destination path to save the converted file: ").strip()
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return file_path, output_path

# ------------------------------------------------------------------
# تابع اصلی برنامه
def main() -> None:
    lang_map = {"1": "C", "2": "C++", "3": "C#", "4": "Java", "5": "Ruby"}
    while True:
        animated_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "6":
            console.print("[red]Exiting...[/red]")
            time.sleep(2)
            os.system('clear')
            break
        if choice not in lang_map:
            console.print("[red]Invalid choice! Please try again.[/red]")
            continue

        target_lang = lang_map[choice]
        file_path, output_path = get_paths()
        if not file_path or not output_path:
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                py_code = f.read()
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            continue

        console.print("[yellow]Converting...[/yellow]")
        converted_code = convert_ast_to_target(py_code, target_lang)

        ext = {"C": "c", "C++": "cpp", "C#": "cs", "Java": "java", "Ruby": "rb"}
        output_file = os.path.join(output_path, f"converted.{ext[target_lang]}")
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(converted_code)
        except Exception as e:
            console.print(f"[red]Error writing file: {e}[/red]")
            continue

        console.print(f"[green]Conversion completed! File saved at: {output_file}[/green]")
        loading_animation()

if __name__ == "__main__":
    display_banner()
    display_title()
    main()