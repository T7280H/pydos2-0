import shutil
import os
import sys

def backup_command(source, destination):
    try:
        if not os.path.exists(source):
            print(f"Error: The source '{source}' does not exist.")
            return

        if os.path.abspath(source) == os.path.abspath(destination):
            print("Error: Source and destination cannot be the same.")
            return

        if os.path.isfile(source):
            shutil.copy2(source, destination)
            print(f"File '{source}' backed up to '{destination}' successfully.")
        elif os.path.isdir(source):
            if os.path.exists(destination):
                destination = os.path.join(destination, os.path.basename(source))
            shutil.copytree(source, destination)
            print(f"Directory '{source}' backed up to '{destination}' successfully.")
        else:
            print(f"Error: Invalid source '{source}'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: backup <source> <destination>")
    else:
        backup_command(sys.argv[1], sys.argv[2])