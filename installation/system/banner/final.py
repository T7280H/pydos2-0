from rich.console import Console

console = Console()

def load_banner():
    banner = """[bold red]
   __  __      _____   _  _ __   __   _  
     )/  )      /  '  | )' )  ) /  )_//  
 .--'/  /    ,-/-,,---|/  /  / /--/ /   
(__o(__/    (_/    \_/ \_/  (_/  (_/___ 
    [/bold red]"""
    console.print(banner)

if __name__ == "__main__":
    load_banner()