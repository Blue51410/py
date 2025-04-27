from gui import setup_gui
from bot_control import setup_bot_controls
from system_stats import start_stats_updater
from installer import install_missing_packages

install_missing_packages()

app, frame_bots, frame_stats, label_cpu, label_cpu_temp, label_gpu, label_gpu_temp = setup_gui()

setup_bot_controls(app, frame_bots)
start_stats_updater(label_cpu, label_cpu_temp, label_gpu, label_gpu_temp)

app.mainloop()
