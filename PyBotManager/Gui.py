import customtkinter as ctk

def setup_gui():
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

    return app, frame_bots, frame_stats, label_cpu, label_cpu_temp, label_gpu, label_gpu_temp
