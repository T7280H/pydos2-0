import os

def rename_command(args):
    if len(args) != 2:
        print("Usage: rename <old_name> <new_name>")
        return

    old_name, new_name = args

    # بررسی وجود فایل قدیمی
    if not os.path.exists(old_name):
        print(f"Error: '{old_name}' does not exist.")
        return

    # بررسی اینکه فایل جدید از قبل وجود نداشته باشد
    if os.path.exists(new_name):
        print(f"Error: A file or directory named '{new_name}' already exists.")
        return

    try:
        # تبدیل مسیرها به مسیر مطلق
        old_name = os.path.abspath(old_name)
        new_name = os.path.abspath(new_name)

        os.rename(old_name, new_name)
        print(f"Renamed '{old_name}' to '{new_name}' successfully.")
    except PermissionError:
        print("Error: Permission denied. Try running as administrator.")
    except FileNotFoundError:
        print(f"Error: '{old_name}' not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    old_name = input("Enter old file name: ").strip()
    new_name = input("Enter new file name: ").strip()
    rename_command([old_name, new_name])