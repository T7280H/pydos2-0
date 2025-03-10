import subprocess
import os
import sys

def bomb_command():
    # مسیر فایل Pybomb در فولدر apps
    pybomb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'application', 'pybomber.py'))
    
    if os.path.exists(pybomb_path):
        try:
            # اجرای فایل Pybomb
            subprocess.run(['python3', pybomb_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing Pybomb: {e}")
            sys.exit(1)
    else:
        print(f"File not found: {pybomb_path}")
        sys.exit(1)

if __name__ == "__main__":
    bomb_command()