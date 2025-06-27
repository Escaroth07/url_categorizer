import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import subprocess
import threading
import time
import sys
import os
import signal

API_URL = "http://localhost:8000/categorize"

def start_api_server(pipe_callback):
    # Start API server as subprocess, capture stdout+stderr
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    )

def stop_api_server(process):
    if os.name == 'nt':
        process.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        process.terminate()

def categorize_url():
    url = url_entry.get().strip()
    result_text.set("")
    status_label.config(text="", foreground="black")
    if not url:
        status_label.config(text="Please enter a URL.", foreground="red")
        return
    categorize_btn.config(state="disabled")
    status_label.config(text="Categorizing...", foreground="blue")
    root.update()
    try:
        resp = requests.post(API_URL, params={"url": url}, timeout=60)
        data = resp.json()
        display = (
            f"URL: {data.get('url', '')}\n"
            f"Category: {data.get('predicted_category', '').upper()}\n"
            f"Confidence: {round(float(data.get('confidence', 0)), 3)}\n"
            f"Method: {data.get('method', '').upper()}"
        )
        result_text.set(display)
        if data.get('predicted_category') in ['malware', 'adult', 'ads']:
            result_box.config(foreground="#c0392b")
        elif data.get('predicted_category') in ['social', 'news', 'shopping']:
            result_box.config(foreground="#2980b9")
        elif data.get('predicted_category') in ['unknown', 'manual_review']:
            result_box.config(foreground="gray")
        else:
            result_box.config(foreground="#27ae60")
        status_label.config(text="Done!", foreground="green")
    except Exception as e:
        result_text.set("")
        status_label.config(text=f"Error: {str(e)}", foreground="red")
    finally:
        categorize_btn.config(state="normal")

def clear_fields():
    url_entry.delete(0, tk.END)
    result_text.set("")
    status_label.config(text="", foreground="black")
    url_entry.focus()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            stop_api_server(api_process)
        except Exception:
            pass
        root.destroy()

def check_api_ready():
    # Runs in background thread, enables GUI when ready
    while True:
        try:
            requests.get("http://localhost:8000", timeout=2)
            break
        except Exception:
            time.sleep(0.5)
    # Enable categorize button and update status in main thread
    root.after(0, api_ready_ui)

def api_ready_ui():
    categorize_btn.config(state="normal")
    status_label.config(text="Ready!", foreground="green")
    log_box.insert(tk.END, "\nAPI server is ready. You can now categorize URLs.\n")
    log_box.see(tk.END)

def read_api_logs(process):
    # Continuously read stdout from the process and put it into the log window
    while True:
        line = process.stdout.readline()
        if not line:
            break
        root.after(0, lambda l=line: append_log_line(l))
    root.after(0, lambda: append_log_line("\n[API server process ended]\n"))

def append_log_line(line):
    log_box.insert(tk.END, line)
    log_box.see(tk.END)

# --- Start API server in background, with log reading thread ---
root = tk.Tk()
root.title("URL Categorizer")
root.geometry("620x440")
root.resizable(False, False)
try:
    root.iconbitmap(default='favicon.ico')
except:
    pass

style = ttk.Style(root)
if "clam" in style.theme_names():
    style.theme_use("clam")

mainframe = ttk.Frame(root, padding=25)
mainframe.pack(fill=tk.BOTH, expand=True)

header = ttk.Label(mainframe, text="🔎 URL Categorizer", font=("Segoe UI", 20, "bold"))
header.pack(pady=(0, 12))

input_frame = ttk.Frame(mainframe)
input_frame.pack(fill=tk.X, pady=(0, 8))

ttk.Label(input_frame, text="Enter URL:", font=("Segoe UI", 12)).pack(side=tk.LEFT)
url_entry = ttk.Entry(input_frame, width=50, font=("Segoe UI", 11))
url_entry.pack(side=tk.LEFT, padx=8)
url_entry.focus()

button_frame = ttk.Frame(mainframe)
button_frame.pack(fill=tk.X, pady=(0, 10))
categorize_btn = ttk.Button(button_frame, text="Categorize", command=categorize_url, state="disabled")
categorize_btn.pack(side=tk.LEFT, padx=(0, 5))
clear_btn = ttk.Button(button_frame, text="Clear", command=clear_fields)
clear_btn.pack(side=tk.LEFT)

status_label = ttk.Label(mainframe, text="Starting API server...", font=("Segoe UI", 10), foreground="blue")
status_label.pack(fill=tk.X, pady=(2, 10))

result_text = tk.StringVar()
result_box = ttk.Label(mainframe, textvariable=result_text, font=("Consolas", 13), justify=tk.LEFT, background="#f8f8f8", anchor=tk.NW, padding=15, relief="solid", width=68)
result_box.pack(fill=tk.BOTH, expand=True, pady=(2, 4))

# --- Log output window ---
ttk.Label(mainframe, text="API Server Log:", font=("Segoe UI", 10, "italic")).pack(anchor="w", pady=(4,0))
log_box = scrolledtext.ScrolledText(mainframe, height=8, font=("Consolas", 9), background="#1a1a1a", foreground="#b0ffb0", relief="groove")
log_box.pack(fill=tk.BOTH, expand=False, pady=(2,0))

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start API and logging thread
api_process = start_api_server(pipe_callback=None)
threading.Thread(target=read_api_logs, args=(api_process,), daemon=True).start()
threading.Thread(target=check_api_ready, daemon=True).start()

root.mainloop()
