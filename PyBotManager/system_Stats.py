import threading
import psutil
try:
    import GPUtil
    gpu_available = True
except ImportError:
    gpu_available = False
import time

def start_stats_updater(label_cpu, label_cpu_temp, label_gpu, label_gpu_temp):
    def update_stats():
        while True:
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
                except:
                    label_gpu.configure(text="GPU Usage: N/A")
                    label_gpu_temp.configure(text="GPU Temp: N/A")
            else:
                label_gpu.configure(text="GPU Usage: N/A (No GPU)")
                label_gpu_temp.configure(text="GPU Temp: N/A")

            time.sleep(1)

    threading.Thread(target=update_stats, daemon=True).start()
