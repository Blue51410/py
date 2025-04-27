
📜 INSTALL INSTRUCTIONS (for PyBot Manager GUI Version)
📥 1. Requirements
You need to install:

disnake
psutil
customtkinter
matplotlib

They are required for the bot management, stats tracking, and graphs.

🖥️ WINDOWS INSTALL
Open Command Prompt or Windows Terminal and run:

bash
pip install disnake psutil customtkinter matplotlib
If pip doesn't work, try:

bash
python -m pip install disnake psutil customtkinter matplotlib
✅ After installing, run the app:

bash
python yourfilename.py
🖥️ LINUX INSTALL (Ubuntu, Debian, etc.)
First update your package manager:

bash
sudo apt update
sudo apt install python3-pip python3-tk -y
Then install Python packages:

bash
pip3 install disnake psutil customtkinter matplotlib
✅ After installing, run the app:

bash
python3 yourfilename.py
📋 Quick Troubleshooting

Problem	Solution
pip not found	Install pip first: sudo apt install python3-pip or on Windows install Python from python.org and check "Add to PATH"
tkinter not installed (Linux)	Install python3-tk package: sudo apt install python3-tk
Permission denied	Add --user to pip install commands: pip install --user disnake psutil customtkinter matplotlib
Python version too old	Make sure you are using Python 3.10 or higher

✨ Recommended Final Command to Paste for New Users:
Windows full install command:
bash
pip install disnake psutil customtkinter matplotlib
Linux full install command:

bash
sudo apt update && sudo apt install python3-pip python3-tk -y && pip3 install disnake psutil customtkinter matplotlib
✅ Then just run:

bash
python (or python3) yourfilename.py
