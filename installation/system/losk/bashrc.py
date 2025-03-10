import subprocess
import os
import sys

def bashrc_command():
    # مسیر فایل BASH CONVERTER
    bashrc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'application', 'bashconverter.py'))
    
    if os.path.exists(bashrc_path):
        try:
            # اجرای فایل BASH CONVERTER
            subprocess.run(['python3', bashrc_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing Bash Converter: {e}")
            sys.exit(1)
    else:
        print(f"File not found: {bashrc_path}")
        sys.exit(1)

if __name__ == "__main__":
    bashrc_command()