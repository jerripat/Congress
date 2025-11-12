from ctypes import c_double
from tkinter import *
from tkinter import ttk
import ttkbootstrap as tk
from Presidents import list_of_us_presidents  # list of tuples: (name, years, vp)

# --- Setup window ---
root = tk.Window(themename="superhero")
root.title("Presidents")
root.geometry("800x600")

# --- Widgets ---
mainLabel = tk.Label(root, text="Presidents", font=("Arial", 22))
mainLabel.pack(pady=20)

displayLabel = tk.Label(root, text="Select your President", font=("Arial", 18))
displayLabel.pack(pady=10)

# Prepare ComboBox data (pretty strings) + lookup map back to tuples
formatted_presidents = [f"{name} ({years}) — VP: {vp}" for name, years, vp in list_of_us_presidents]
lookup = {f"{name} ({years}) — VP: {vp}": (name, years, vp) for name, years, vp in list_of_us_presidents}

# Create ComboBox
presCombo = tk.Combobox(
    root,
    bootstyle="success",
    values=formatted_presidents,
    font=("Arial", 14),
    width=60,
)
presCombo.pack(pady=20)

# ---- Radio buttons to choose what to show ----
choice_var = tk.StringVar(value="Name")  # default selection

radio_frame = tk.Frame(root)
radio_frame.pack(pady=10)

# Round toggle style + color (e.g., success)
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
    else:
        displayLabel.config(text="Select your President")

def on_select(event):
    update_display()

# Update on both combobox change and radio change
presCombo.bind("<<ComboboxSelected>>", on_select)
choice_var.trace_add("write", update_display)

# --- Run the app ---
root.mainloop()
