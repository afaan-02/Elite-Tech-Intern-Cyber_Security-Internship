import os
import json
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

HASH_FILE = 'advanced_hashes.json'
LOG_FILE = 'integrity_log.txt'

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def get_all_files(path):
    all_files = []
    for root, _, files in os.walk(path):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def log_change(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()} - {message}\n")

def update_table():
    tree.delete(*tree.get_children())
    for file in monitored_files:
        tree.insert("", tk.END, values=(file, "❓ Unknown"))

def add_file_or_folder():
    path = filedialog.askopenfilename(title="Select File") or filedialog.askdirectory(title="Select Folder")
    if path and path not in monitored_files:
        monitored_files.append(path)
        update_table()

def check_integrity():
    stored_hashes = load_hashes()
    new_hashes = {}
    result_map = {}

    for item in monitored_files:
        files = [item]
        if os.path.isdir(item):
            files = get_all_files(item)

        for file_path in files:
            current_hash = calculate_hash(file_path)
            if current_hash:
                new_hashes[file_path] = current_hash
                if file_path in stored_hashes:
                    if current_hash != stored_hashes[file_path]:
                        result_map[file_path] = "⚠ Changed"
                        log_change(f"[CHANGED] {file_path}")
                    else:
                        result_map[file_path] = "✔ OK"
                else:
                    result_map[file_path] = "🆕 New"
                    log_change(f"[NEW] {file_path}")
            else:
                result_map[file_path] = "❌ Missing or unreadable"
                log_change(f"[MISSING] {file_path}")

    save_hashes(new_hashes)
    display_results(result_map)

def display_results(results):
    tree.delete(*tree.get_children())
    for file, status in results.items():
        tree.insert("", tk.END, values=(file, status))
    messagebox.showinfo("Integrity Check", "Integrity check complete. See table for results.")

# ---------------- GUI SETUP ------------------

app = tk.Tk()
app.title("🔐 Advanced File Integrity Checker")
app.geometry("800x500")

style = ttk.Style(app)
style.theme_use("clam")  # light theme (or "alt", "default", "vista")

monitored_files = []

tk.Label(app, text="Monitored Files & Folders", font=("Helvetica", 14)).pack(pady=10)

columns = ("File / Folder", "Status")
tree = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=350 if col == "File / Folder" else 100)
tree.pack(fill="both", expand=True, padx=20)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="➕ Add File/Folder", command=add_file_or_folder, width=18).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="🛡 Check Integrity", command=check_integrity, width=18).grid(row=0, column=1, padx=10)

# Optional: open log button
def open_log():
    if os.path.exists(LOG_FILE):
        os.system(f'notepad "{LOG_FILE}"' if os.name == 'nt' else f'xdg-open "{LOG_FILE}"')

tk.Button(btn_frame, text="📄 View Log", command=open_log, width=18).grid(row=0, column=2, padx=10)

app.mainloop()
