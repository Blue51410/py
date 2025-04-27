import os
import sys
import subprocess
import time
import threading
import psutil

# --- BOT DATA ---
bots = {}
MAX_BOTS = 15

# --- FUNCTIONS ---

def get_python_command():
    return "python" if sys.platform.startswith("win") else "python3"

def add_bot():
    if len(bots) >= MAX_BOTS:
        print("[!] Max bot limit reached (15 bots). Cannot add more.")
        return
    path = input("Enter full path to bot .py file: ").strip()
    if not os.path.isfile(path):
        print("[!] Invalid file path.")
        return
    bot_number = len(bots) + 1
    bots[bot_number] = {
        "name": os.path.basename(path),
        "path": os.path.dirname(path),
        "script": os.path.basename(path),
        "process": None
    }
    print(f"[+] Added bot #{bot_number}: {bots[bot_number]['name']}")

def start_bot():
    list_bots()
    try:
        num = int(input("Enter bot number to START: "))
        bot = bots.get(num)
        if bot and not bot["process"]:
            full_path = os.path.join(bot["path"], bot["script"])
            python_cmd = get_python_command()
            bot["process"] = subprocess.Popen([python_cmd, full_path])
            print(f"[+] Bot {bot['name']} started.")
        else:
            print("[!] Invalid bot number or already running.")
    except Exception as e:
        print(f"[!] Error: {e}")

def stop_bot():
    list_bots()
    try:
        num = int(input("Enter bot number to STOP: "))
        bot = bots.get(num)
        if bot and bot["process"]:
            bot["process"].terminate()
            bot["process"].wait(timeout=5)
            bot["process"] = None
            print(f"[+] Bot {bot['name']} stopped.")
        else:
            print("[!] Invalid bot number or already stopped.")
    except Exception as e:
        print(f"[!] Error: {e}")

def restart_bot():
    list_bots()
    try:
        num = int(input("Enter bot number to RESTART: "))
        bot = bots.get(num)
        if bot:
            if bot["process"]:
                bot["process"].terminate()
                bot["process"].wait(timeout=5)
                bot["process"] = None
            time.sleep(1)
            full_path = os.path.join(bot["path"], bot["script"])
            python_cmd = get_python_command()
            bot["process"] = subprocess.Popen([python_cmd, full_path])
            print(f"[+] Bot {bot['name']} restarted.")
        else:
            print("[!] Invalid bot number.")
    except Exception as e:
        print(f"[!] Error: {e}")

def list_bots():
    if not bots:
        print("[!] No bots loaded.")
        return
    print("\n--- Loaded Bots ---")
    for num, bot in bots.items():
        status = "🟢 Running" if bot["process"] else "🔴 Stopped"
        print(f"#{num}: {bot['name']} [{status}]")
    print("-------------------\n")

def show_system_stats():
    print("\n--- System Stats ---")
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_string = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

    print(f"CPU Usage: {cpu}%")
    print(f"RAM Usage: {ram}%")
    print(f"Disk Usage: {disk}%")
    print(f"Uptime: {uptime_string}")
    print("--------------------\n")

def main_menu():
    while True:
        print("""
====== PyBot Manager: Server Pro Edition ======

1. Add Bot
2. Start Bot
3. Stop Bot
4. Restart Bot
5. List Bots
6. Show System Stats
7. Exit
""")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            add_bot()
        elif choice == "2":
            start_bot()
        elif choice == "3":
            stop_bot()
        elif choice == "4":
            restart_bot()
        elif choice == "5":
            list_bots()
        elif choice == "6":
            show_system_stats()
        elif choice == "7":
            print("[*] Exiting...")
            for bot in bots.values():
                if bot["process"]:
                    bot["process"].terminate()
            break
        else:
            print("[!] Invalid choice.")

# --- START APP ---
if __name__ == "__main__":
    main_menu()
