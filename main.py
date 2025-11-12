import sqlite3
import webbrowser
from urllib.parse import quote_plus
from tkinter import *
from tkinter import ttk
import ttkbootstrap as tk

DB_PATH = "presidents.db"

def fetch_presidents(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name, years, vp FROM presidents ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [(name, str(years), vp) for (name, years, vp) in rows]

def wikileaks_search_url(name: str) -> str:
    # Use a general search constrained to wikileaks.org for reliability
    # e.g. https://duckduckgo.com/?q=site%3Awikileaks.org+Barack+Obama
    return f"https://duckduckgo.com/?q=site%3Awikileaks.org+{quote_plus(name)}"

# --- Load data from DB ---
presidents = fetch_presidents()
if not presidents:
    raise RuntimeError("No rows found in 'presidents' table. Run the insert script first.")

# --- Setup window ---
root = tk.Window(themename="superhero")
root.title("Presidents")
root.geometry("800x600")

# --- Headings ---
mainLabel = tk.Label(root, text="Presidents", font=("Arial", 22))
mainLabel.pack(pady=20)

displayLabel = tk.Label(root, text="Select your President", font=("Arial", 18))
displayLabel.pack(pady=10)

# Build display strings + lookup
formatted_presidents = [f"{name} ({years}) — VP: {vp}" for name, years, vp in presidents]
lookup = {f"{name} ({years}) — VP: {vp}": (name, years, vp) for name, years, vp in presidents}

# Combobox
presCombo = tk.Combobox(
    root,
    bootstyle="success",
    values=formatted_presidents,
    font=("Arial", 14),
    width=60,
    state="readonly"
)
presCombo.pack(pady=20)

# ---- Radio buttons to choose what to show ----
choice_var = tk.StringVar(value="Name")

radio_frame = tk.Frame(root)
radio_frame.pack(pady=10)

rb_name = tk.Radiobutton(
    radio_frame, text="Name", value="Name", variable=choice_var,
    bootstyle="success-round-toggle"
)
rb_years = tk.Radiobutton(
    radio_frame, text="Years", value="Years", variable=choice_var,
    bootstyle="info-round-toggle"
)
rb_vp = tk.Radiobutton(
    radio_frame, text="VP", value="VP", variable=choice_var,
    bootstyle="warning-round-toggle"
)
for rb in (rb_name, rb_years, rb_vp):
    rb.pack(side=LEFT, padx=8)

# ---- URL text box + open button ----
url_var = tk.StringVar(value="")  # will hold the generated link

url_label = tk.Label(root, text="WikiLeaks search link:", font=("Arial", 12))
url_label.pack(pady=(20, 5))

url_entry = tk.Entry(root, textvariable=url_var, width=80, font=("Arial", 11))
url_entry.pack(pady=(0, 8))

def open_url():
    url = url_var.get().strip()
    if url:
        webbrowser.open(url)

open_btn = tk.Button(root, text="Open WikiLeaks Search", bootstyle="secondary", command=open_url)
open_btn.pack(pady=4)

# --- Event handling ---
def update_display(*_):
    sel = presCombo.get()
    if sel in lookup:
        name, years, vp = lookup[sel]
        mode = choice_var.get()
        if mode == "Name":
            displayLabel.config(text=f"Name: {name}")
        elif mode == "Years":
            displayLabel.config(text=f"Years in office: {years}")
        elif mode == "VP":
            displayLabel.config(text=f"Vice President: {vp}")

        # Update the WikiLeaks search link for this president
        url_var.set(wikileaks_search_url(name))
    else:
        displayLabel.config(text="Select your President")
        url_var.set("")

def on_select(event):
    update_display()

presCombo.bind("<<ComboboxSelected>>", on_select)
choice_var.trace_add("write", update_display)

# Optional: preselect first item and show it
presCombo.current(0)
update_display()

# --- Run the app ---
root.mainloop()
