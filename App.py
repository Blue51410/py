import os
import subprocess
import sys
import threading
import time
import platform
import re

required_packages = [
    "disnake",
    "psutil",
    "customtkinter",
    "GPUtil"
]

def install_missing_packages():
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"🔵 Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_missing_packages()

import psutil
import customtkinter as ctk
try:
    import GPUtil
    gpu_available = True
except ImportError:
    gpu_available = False

MAX_BOTS = 6
bots = {}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("PyBot Manager")
app.geometry("750x600")
app.configure(bg="black")

frame_bots = ctk.CTkFrame(app, fg_color="black")
frame_bots.pack(pady=10, padx=10, fill="both", expand=True)

frame_stats = ctk.CTkFrame(app, fg_color="black")
frame_stats.pack(pady=10, padx=10, fill="x")

label_cpu = ctk.CTkLabel(frame_stats, text="CPU Usage: ", text_color="#00FF00")
label_cpu.pack(pady=5)

label_cpu_temp = ctk.CTkLabel(frame_stats, text="CPU Temp: ", text_color="#00FF00")
label_cpu_temp.pack(pady=5)

label_gpu = ctk.CTkLabel(frame_stats, text="GPU Usage: N/A", text_color="#00FF00")
label_gpu.pack(pady=5)

label_gpu_temp = ctk.CTkLabel(frame_stats, text="GPU Temp: N/A", text_color="#00FF00")
label_gpu_temp.pack(pady=5)

def add_bot():
    if len(bots) >= MAX_BOTS:
        ctk.CTkMessagebox(title="Error", message="Maximum bots reached!", icon="warning")
        return
    script_path = ctk.filedialog.askopenfilename(title="Select Bot Script", filetypes=[("Python Files", "*.py")])
    if not script_path:
        return
    folder_path = os.path.dirname(script_path)
    bot_name = os.path.basename(script_path)
    bot_number = len(bots) + 1
    bots[bot_number] = {"name": bot_name, "path": folder_path, "script": os.path.basename(script_path), "process": None}
    refresh_bots()

def get_python_command():
    if platform.system() == "Windows":
        return "python"
    else:
        return "python3"

def extract_imports(script_path):
    packages = set()
    pattern_import = re.compile(r'^\s*(import|from)\s+([a-zA-Z0-9_\.]+)')
    with open(script_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern_import.match(line)
            if match:
                pkg = match.group(2).split('.')[0]  # Only base package
                if pkg not in ('sys', 'os', 'time', 'threading', 'subprocess', 'platform', 're', 'ctk', 'customtkinter', 'psutil', 'GPUtil'):  # Ignore built-ins + ones we already manage
                    packages.add(pkg)
    return packages

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", package])
    except Exception as e:
        print(f"⚠️ Failed to install {package}: {e}")

def start_bot(num):
    bot = bots.get(num)
    if bot and not bot["process"]:
        try:
            full_path = os.path.join(bot["path"], bot["script"])
            required = extract_imports(full_path)
            for pkg in required:
                try:
                    __import__(pkg)
                except ImportError:
                    print(f"🟡 Installing missing package for bot: {pkg}")
                    install_package(pkg)

            python_cmd = get_python_command()
            bot["process"] = subprocess.Popen([python_cmd, full_path])
            refresh_bots()
        except Exception as e:
            ctk.CTkMessagebox(title="Error", message=f"Failed to start bot: {e}", icon="cancel")

def stop_bot(num):
    bot = bots.get(num)
    if bot and bot["process"]:
        try:
            bot["process"].terminate()
            bot["process"].wait(timeout=5)
        except subprocess.TimeoutExpired:
            bot["process"].kill()
        bot["process"] = None
        refresh_bots()

def restart_bot(num):
    stop_bot(num)
    time.sleep(1)
    start_bot(num)

def refresh_bots():
    for widget in frame_bots.winfo_children():
        widget.destroy()
    for num, bot in bots.items():
        status = "🟢 Running" if bot["process"] else "🔴 Stopped"
        bot_frame = ctk.CTkFrame(frame_bots, fg_color="black")
        bot_frame.pack(fill="x", pady=5, padx=5)

        label = ctk.CTkLabel(bot_frame, text=f"#{num} {bot['name']} [{status}]", text_color="#00FF00")
        label.pack(side="left", padx=10)

        btn_start = ctk.CTkButton(bot_frame, text="Start", command=lambda n=num: start_bot(n), fg_color="#00FF00", hover_color="#00AA00", text_color="black")
        btn_start.pack(side="left", padx=5)

        btn_stop = ctk.CTkButton(bot_frame, text="Stop", command=lambda n=num: stop_bot(n), fg_color="#00FF00", hover_color="#00AA00", text_color="black")
        btn_stop.pack(side="left", padx=5)

        btn_restart = ctk.CTkButton(bot_frame, text="Restart", command=lambda n=num: restart_bot(n), fg_color="#00FF00", hover_color="#00AA00", text_color="black")
        btn_restart.pack(side="left", padx=5)

def update_stats():
    while True:
        try:
            cpu_usage = psutil.cpu_percent()
            label_cpu.configure(text=f"CPU Usage: {cpu_usage}%")

            temps = psutil.sensors_temperatures()
            cpu_temp = None
            for name, entries in temps.items():
                for entry in entries:
                    if entry.current:
                        cpu_temp = entry.current
                        break
                if cpu_temp:
                    break
            label_cpu_temp.configure(text=f"CPU Temp: {cpu_temp}°C" if cpu_temp else "CPU Temp: N/A")
        except Exception:
            label_cpu_temp.configure(text="CPU Temp: N/A")

        if gpu_available:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_usage = gpus[0].load * 100
                    gpu_temp = gpus[0].temperature
                    label_gpu.configure(text=f"GPU Usage: {gpu_usage:.1f}%")
                    label_gpu_temp.configure(text=f"GPU Temp: {gpu_temp}°C")
                else:
                    label_gpu.configure(text="GPU Usage: N/A")
                    label_gpu_temp.configure(text="GPU Temp: N/A")
            except Exception:
                label_gpu.configure(text="GPU Usage: N/A")
                label_gpu_temp.configure(text="GPU Temp: N/A")
        else:
            label_gpu.configure(text="GPU Usage: N/A (No GPU)")
            label_gpu_temp.configure(text="GPU Temp: N/A")
        time.sleep(1)

btn_add = ctk.CTkButton(app, text="Add Bot", command=add_bot, fg_color="#00FF00", hover_color="#00AA00", text_color="black")
btn_add.pack(pady=10)

btn_exit = ctk.CTkButton(app, text="Exit", command=lambda: app.destroy(), fg_color="#00FF00", hover_color="#00AA00", text_color="black")
btn_exit.pack(pady=5)

threading.Thread(target=update_stats, daemon=True).start()

app.mainloop()
