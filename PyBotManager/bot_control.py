import os
import subprocess
import platform
import tkinter.filedialog as filedialog

bots = {}
MAX_BOTS = 6

def get_python_command():
    return "python" if platform.system() == "Windows" else "python3"

def add_bot(frame_bots):
    script_path = filedialog.askopenfilename(title="Select Bot Script", filetypes=[("Python Files", "*.py")])
    if not script_path:
        return
    folder_path = os.path.dirname(script_path)
    bot_name = os.path.basename(script_path)
    bot_number = len(bots) + 1
    bots[bot_number] = {"name": bot_name, "path": folder_path, "script": os.path.basename(script_path), "process": None}
    refresh_bots(frame_bots)

def start_bot(num):
    bot = bots.get(num)
    if bot and not bot["process"]:
        full_path = os.path.join(bot["path"], bot["script"])
        python_cmd = get_python_command()
        bot["process"] = subprocess.Popen([python_cmd, full_path])

def stop_bot(num):
    bot = bots.get(num)
    if bot and bot["process"]:
        bot["process"].terminate()
        bot["process"].wait()
        bot["process"] = None

def restart_bot(num):
    stop_bot(num)
    start_bot(num)

def refresh_bots(frame_bots):
    for widget in frame_bots.winfo_children():
        widget.destroy()

    from customtkinter import CTkButton, CTkLabel

    for num, bot in bots.items():
        status = "🟢 Running" if bot["process"] else "🔴 Stopped"
        label = CTkLabel(frame_bots, text=f"#{num} {bot['name']} [{status}]", text_color="#00FF00")
        label.pack(pady=2)

        CTkButton(frame_bots, text="Start", command=lambda n=num: start_bot(n), fg_color="#00FF00", hover_color="#00AA00", text_color="black").pack(pady=2)
        CTkButton(frame_bots, text="Stop", command=lambda n=num: stop_bot(n), fg_color="#00FF00", hover_color="#00AA00", text_color="black").pack(pady=2)
        CTkButton(frame_bots, text="Restart", command=lambda n=num: restart_bot(n), fg_color="#00FF00", hover_color="#00AA00", text_color="black").pack(pady=2)

def setup_bot_controls(app, frame_bots):
    from customtkinter import CTkButton
    CTkButton(app, text="Add Bot", command=lambda: add_bot(frame_bots), fg_color="#00FF00", hover_color="#00AA00", text_color="black").pack(pady=10)
    CTkButton(app, text="Exit", command=lambda: app.destroy(), fg_color="#00FF00", hover_color="#00AA00", text_color="black").pack(pady=5)
