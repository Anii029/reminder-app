import customtkinter as ctk
from plyer import notification
from datetime import datetime
import json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

import os

FILE = os.path.join(os.path.dirname(__file__), "reminders.json")

# Load data
try:
    with open(FILE, "r") as f:
        reminders = json.load(f)
except:
    reminders = []

# Save
def save_data():
    with open(FILE, "w") as f:
        json.dump(reminders, f, indent=4)

# Add reminder
def add_reminder():
    t = time_entry.get()
    msg = msg_entry.get()

    if t and msg:
        reminders.append({"time": t, "msg": msg, "done": False})
        listbox.insert("end", f"{t} - {msg}")
        save_data()

    time_entry.delete(0, "end")
    msg_entry.delete(0, "end")

# Delete reminder
def delete_reminder():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        listbox.delete(index)
        reminders.pop(index)
        save_data()

# Load list
def load_list():
    for r in reminders:
        listbox.insert("end", f"{r['time']} - {r['msg']}")

# Notification loop
def check_reminders():
    now = datetime.now().strftime("%H:%M")

    for r in reminders:
        if now >= r["time"] and not r["done"]:
            notification.notify(
                title="Reminder",
                message=r["msg"],
                timeout=5
            )
            r["done"] = True
            save_data()

    app.after(30000, check_reminders)

# App window
app = ctk.CTk()
app.title("Reminder App")
app.geometry("420x500")

# Title
title = ctk.CTkLabel(app, text="Reminder App", font=("Arial", 22, "bold"))
title.pack(pady=10)

# Inputs
time_entry = ctk.CTkEntry(app, placeholder_text="Time (HH:MM)")
time_entry.pack(pady=5)

msg_entry = ctk.CTkEntry(app, placeholder_text="Message")
msg_entry.pack(pady=5)

# Buttons
ctk.CTkButton(app, text="Add Reminder", command=add_reminder).pack(pady=5)
ctk.CTkButton(app, text="Delete Selected", command=delete_reminder).pack(pady=5)

# Listbox
import tkinter as tk
listbox = tk.Listbox(app, bg="#2b2b2b", fg="white")
listbox.pack(fill="both", expand=True, padx=10, pady=10)

# Load + start
load_list()
check_reminders()

app.mainloop()