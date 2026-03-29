import os
import shutil
import tkinter as tk
from tkinter import messagebox
import subprocess

def get_adb_path():
    # Check if adb is in the same folder
    if os.path.exists("adb.exe"):
        return "adb.exe"
    # Check if adb is natively installed and in PATH
    elif shutil.which("adb"):
        return "adb"
    else:
        return None

def run_adb_command(cmd_args):
    adb_path = get_adb_path()
    if not adb_path:
        return -1, "", "ADB not found! Please install Android Platform Tools or place adb.exe in this folder."
        
    try:
        # Prevent terminal window from flashing on Windows
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        result = subprocess.run([adb_path] + cmd_args, capture_output=True, text=True, startupinfo=startupinfo, timeout=10)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def check_status():
    status_label.config(text="Checking...", fg="black")
    root.update()
    
    code, out, err = run_adb_command(['devices'])
    if 'device' not in out or 'unauthorized' in out.lower():
        status_label.config(text="❌ No device connected or unauthorized!", fg="red", font=("Helvetica", 10, "bold"))
        return
        
    code, out, err = run_adb_command(['shell', 'pidof', 'shizuku_server'])
    
    if out.strip().isdigit():
        msg = f"✅ Shizuku is RUNNING (PID: {out.strip()})"
        msg += "\n\n⚠️ Realme/Oppo users: Turn ON\n'Disable permission monitoring'\nin Developer Options to fix the red warning!"
        status_label.config(text=msg, fg="green", font=("Helvetica", 10, "bold"))
    else:
        status_label.config(text="❌ Shizuku is NOT running.", fg="red", font=("Helvetica", 10, "bold"))

def start_shizuku():
    status_label.config(text="Starting Shizuku...", fg="black")
    root.update()
    
    code, out, err = run_adb_command(['shell', 'sh', '/storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh'])
    
    # Check if the output suggests success
    if "shizuku_starter exit with 0" in out or "info: starting server" in out:
        check_status()
    else:
        # Try checking status anyway
        root.after(1000, check_status)

# Create the main window
root = tk.Tk()
root.title("Shizuku ADB Tool")
root.geometry("400x320")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

title = tk.Label(root, text="Shizuku Connection Tool", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
title.pack(pady=20)

status_label = tk.Label(root, text="Click 'Check Status' to begin", font=("Helvetica", 11), wraplength=350, bg="#f0f0f0", height=5)
status_label.pack(pady=10)

btn_check = tk.Button(root, text="Check Status", command=check_status, width=25, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"), relief=tk.FLAT)
btn_check.pack(pady=5)

btn_start = tk.Button(root, text="Start / Restart Shizuku", command=start_shizuku, width=25, height=2, bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"), relief=tk.FLAT)
btn_start.pack(pady=5)

# Run the app
root.mainloop()
