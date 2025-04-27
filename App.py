import os
import subprocess
import sys
import threading
import time
import platform
import psutil
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- INSTALL REQUIRED PACKAGES ---
required_packages = ["disnake", "psutil", "customtkinter", "matplotlib"]

def install_missing_packages():
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", package])

install_missing_packages()

# --- BOT DATA ---
bots = {}
MAX_BOTS = 6
logs = []
notes_content = ""

# --- SETUP GUI ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("🖥️ PyBot Manager v3.0")
app.geometry("1200x800")
app.configure(bg="black")

# --- FRAMES ---
frame_title = ctk.CTkFrame(app, fg_color="black", border_width=2, border_color="green")
frame_title.pack(pady=10, padx=10, fill="x")

frame_body = ctk.CTkFrame(app, fg_color="black", border_width=2, border_color="green")
frame_body.pack(pady=10, padx=10, fill="both", expand=True)

frame_left = ctk.CTkFrame(frame_body, fg_color="black")
frame_left.pack(side="left", fill="both", expand=True, padx=5)

frame_right = ctk.CTkFrame(frame_body, fg_color="black")
frame_right.pack(side="right", fill="both", expand=True, padx=5)

frame_stats = ctk.CTkFrame(frame_left, fg_color="black")
frame_stats.pack(pady=5)

frame_actions = ctk.CTkFrame(frame_left, fg_color="black")
frame_actions.pack(pady=5)

frame_actions_row1 = ctk.CTkFrame(frame_actions, fg_color="black")
frame_actions_row1.pack(pady=5)

frame_actions_row2 = ctk.CTkFrame(frame_actions, fg_color="black")
frame_actions_row2.pack(pady=5)

frame_dropdown = ctk.CTkFrame(frame_right, fg_color="black")
frame_dropdown.pack(pady=5)

frame_display = ctk.CTkFrame(frame_right, fg_color="black", border_width=2, border_color="green")
frame_display.pack(expand=True, fill="both", padx=10, pady=5)

# --- TITLE ---
label_title = ctk.CTkLabel(frame_title, text="🖥️ PyBot Manager - Multi View Edition", font=("Consolas", 26), text_color="lime")
label_title.pack(pady=10)

# --- SYSTEM STATS LABELS ---
label_cpu = ctk.CTkLabel(frame_stats, text="CPU Usage: ", font=("Consolas", 20), text_color="lime")
label_cpu.pack(pady=2)

label_ram = ctk.CTkLabel(frame_stats, text="RAM Usage: ", font=("Consolas", 20), text_color="lime")
label_ram.pack(pady=2)

label_disk = ctk.CTkLabel(frame_stats, text="Disk Usage: ", font=("Consolas", 20), text_color="lime")
label_disk.pack(pady=2)

label_uptime = ctk.CTkLabel(frame_stats, text="Uptime: ", font=("Consolas", 20), text_color="lime")
label_uptime.pack(pady=2)

# --- FUNCTIONS ---

def get_python_command():
    return "python" if platform.system() == "Windows" else "python3"

def add_bot():
    if len(bots) >= MAX_BOTS:
        return
    script_path = ctk.filedialog.askopenfilename(title="Select Bot Script", filetypes=[("Python Files", "*.py")])
    if not script_path:
        return
    folder_path = os.path.dirname(script_path)
    bot_name = os.path.basename(script_path)
    bot_number = len(bots) + 1
    bots[bot_number] = {"name": bot_name, "path": folder_path, "script": bot_name, "process": None}
    logs.append(f"Added bot: {bot_name}")
    refresh_bots()

def add_bots_from_folder():
    folder_path = ctk.filedialog.askdirectory(title="Select Folder Containing Bots")
    if not folder_path:
        return
    for file in os.listdir(folder_path):
        if file.endswith(".py") and len(bots) < MAX_BOTS:
            bot_number = len(bots) + 1
            bots[bot_number] = {"name": file, "path": folder_path, "script": file, "process": None}
            logs.append(f"Bulk added bot: {file}")
    refresh_bots()

def start_bot(num):
    bot = bots.get(num)
    if bot and not bot["process"]:
        try:
            full_path = os.path.join(bot["path"], bot["script"])
            python_cmd = get_python_command()
            bot["process"] = subprocess.Popen([python_cmd, full_path])
            logs.append(f"Started bot: {bot['name']}")
            refresh_bots()
        except Exception as e:
            print(f"Failed to start bot: {e}")

def stop_bot(num):
    bot = bots.get(num)
    if bot and bot["process"]:
        try:
            bot["process"].terminate()
            bot["process"].wait(timeout=5)
            logs.append(f"Stopped bot: {bot['name']}")
        except subprocess.TimeoutExpired:
            bot["process"].kill()
            logs.append(f"Force killed bot: {bot['name']}")
        bot["process"] = None
        refresh_bots()

def restart_bot(num):
    stop_bot(num)
    time.sleep(1)
    start_bot(num)

def start_all_bots():
    for num in bots.keys():
        start_bot(num)

def stop_all_bots():
    for num in bots.keys():
        stop_bot(num)

def restart_all_bots():
    for num in bots.keys():
        restart_bot(num)

def refresh_bots():
    pass  # Refreshing bots handled elsewhere now


# --- SYSTEM STATS UPDATE ---
def update_stats():
    while True:
        try:
            cpu_usage = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            label_cpu.configure(text=f"CPU Usage: {cpu_usage}%")
            label_ram.configure(text=f"RAM Usage: {ram}%")
            label_disk.configure(text=f"Disk Usage: {disk}%")

            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_string = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
            label_uptime.configure(text=f"Uptime: {uptime_string}")

        except Exception as e:
            print(f"Stats Error: {e}")

        time.sleep(1)

# --- RIGHT SIDE MENU SYSTEM ---

current_display = None

def clear_frame():
    for widget in frame_display.winfo_children():
        widget.destroy()

def show_smart_bot_manager():
    clear_frame()
    if not bots:
        label = ctk.CTkLabel(frame_display, text="No bots loaded yet.", text_color="lime", font=("Consolas", 20))
        label.pack(pady=10)
    else:
        for num, bot in bots.items():
            status = "🟢 Running" if bot["process"] else "🔴 Stopped"
            label = ctk.CTkLabel(frame_display, text=f"{bot['name']} [{status}]", font=("Consolas", 18), text_color="lime")
            label.pack(pady=5)

def show_alerts_center():
    clear_frame()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    cpu = psutil.cpu_percent()

    if ram > 80:
        alert1 = ctk.CTkLabel(frame_display, text="⚠️ RAM Usage High!", text_color="red", font=("Consolas", 20))
        alert1.pack(pady=10)
    if disk > 90:
        alert2 = ctk.CTkLabel(frame_display, text="⚠️ Disk Space Critically Low!", text_color="red", font=("Consolas", 20))
        alert2.pack(pady=10)
    if cpu > 85:
        alert3 = ctk.CTkLabel(frame_display, text="⚠️ CPU Usage High!", text_color="red", font=("Consolas", 20))
        alert3.pack(pady=10)
    if ram <= 80 and disk <= 90 and cpu <= 85:
        ok = ctk.CTkLabel(frame_display, text="✅ All systems normal.", text_color="lime", font=("Consolas", 20))
        ok.pack(pady=10)

def show_graphs():
    clear_frame()
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=frame_display)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    x_data, y_data_cpu, y_data_ram = [], [], []

    def animate(i):
        x_data.append(i)
        y_data_cpu.append(psutil.cpu_percent())
        y_data_ram.append(psutil.virtual_memory().percent)

        ax.clear()
        ax.plot(x_data[-50:], y_data_cpu[-50:], label='CPU %')
        ax.plot(x_data[-50:], y_data_ram[-50:], label='RAM %')
        ax.legend(loc='upper right')
        ax.set_ylim(0, 100)
        ax.set_ylabel("Usage (%)")
        ax.set_xlabel("Time (s)")
        fig.tight_layout()

        canvas.draw()

    def update_graph():
        counter = 0
        while True:
            animate(counter)
            counter += 1
            time.sleep(1)

    threading.Thread(target=update_graph, daemon=True).start()

def show_notes():
    clear_frame()
    textbox = ctk.CTkTextbox(frame_display, font=("Consolas", 16))
    textbox.pack(expand=True, fill="both", padx=10, pady=10)
    textbox.insert("1.0", notes_content)

    def save_notes():
        global notes_content
        notes_content = textbox.get("1.0", "end").strip()

    save_btn = ctk.CTkButton(frame_display, text="Save Notes", command=save_notes, fg_color="green", hover_color="darkgreen", text_color="black", font=("Consolas", 16))
    save_btn.pack(pady=5)

# --- MENU HANDLER ---

def menu_handler(choice):
    if choice == "Smart Bot Manager":
        show_smart_bot_manager()
    elif choice == "Alerts Center":
        show_alerts_center()
    elif choice == "Live Graphs":
        show_graphs()
    elif choice == "Notes Panel":
        show_notes()

# --- DROPDOWN MENU ---

menu_option = ctk.StringVar()
menu_dropdown = ctk.CTkOptionMenu(frame_dropdown, variable=menu_option, values=["Smart Bot Manager", "Alerts Center", "Live Graphs", "Notes Panel"], command=menu_handler)
menu_dropdown.set("Smart Bot Manager")
menu_dropdown.pack(pady=10)

# --- ACTION BUTTONS (LEFT SIDE) ---

btn_add = ctk.CTkButton(frame_actions_row1, text="Add Bot", command=add_bot, fg_color="lime", hover_color="darkgreen", text_color="black", font=("Consolas", 16), corner_radius=10)
btn_add.pack(side="left", padx=10, pady=5)

btn_bulk_add = ctk.CTkButton(frame_actions_row1, text="Add Bots From Folder", command=add_bots_from_folder, fg_color="lime", hover_color="darkgreen", text_color="black", font=("Consolas", 16), corner_radius=10)
btn_bulk_add.pack(side="left", padx=10, pady=5)

btn_start_all = ctk.CTkButton(frame_actions_row1, text="Start All", command=start_all_bots, fg_color="green", hover_color="darkgreen", text_color="black", font=("Consolas", 16), corner_radius=10)
btn_start_all.pack(side="left", padx=10, pady=5)

btn_stop_all = ctk.CTkButton(frame_actions_row2, text="Stop All", command=stop_all_bots, fg_color="red", hover_color="darkred", text_color="white", font=("Consolas", 16), corner_radius=10)
btn_stop_all.pack(side="left", padx=10, pady=5)

btn_restart_all = ctk.CTkButton(frame_actions_row2, text="Restart All", command=restart_all_bots, fg_color="orange", hover_color="darkorange", text_color="black", font=("Consolas", 16), corner_radius=10)
btn_restart_all.pack(side="left", padx=10, pady=5)

btn_exit = ctk.CTkButton(frame_actions_row2, text="Exit", command=lambda: app.destroy(), fg_color="red", hover_color="darkred", text_color="white", font=("Consolas", 16), corner_radius=10)
btn_exit.pack(side="left", padx=10, pady=5)

# --- BACKGROUND THREADS ---
threading.Thread(target=update_stats, daemon=True).start()

# --- RUN APP ---
menu_handler("Smart Bot Manager")
app.mainloop()
