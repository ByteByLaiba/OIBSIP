import tkinter as tk
from tkinter import messagebox
import secrets
import string
import math

# ---------------- COLORS ---------------- #
JUNGLE_TEAL = "#6B9080"
MUTED_TEAL = "#A4C3B2"
FROZEN_WATER = "#CCE3DE"
AZURE_MIST = "#EAF4F4"
MINT_CREAM = "#F6FFF8"

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/"

# ---------------- LOGIC ---------------- #

def calculate_entropy(password):
    pool_size = 0

    if any(c.islower() for c in password):
        pool_size += 26
    if any(c.isupper() for c in password):
        pool_size += 26
    if any(c.isdigit() for c in password):
        pool_size += 10
    if any(c in SYMBOLS for c in password):
        pool_size += len(SYMBOLS)

    if pool_size == 0:
        return 0

    return round(len(password) * math.log2(pool_size), 1)


def strength_from_entropy(entropy):
    if entropy < 40:
        return "Weak", "#C62828"
    elif entropy < 60:
        return "Moderate", "#EF6C00"
    elif entropy < 80:
        return "Strong", "#2E7D32"
    else:
        return "Excellent", JUNGLE_TEAL


def generate_password():
    try:
        length = int(length_entry.get())
        if length < 8 or length > 32:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be between 8 and 32."
            )
            return
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number for password length."
        )
        return

    character_sets = []

    if letters_var.get():
        character_sets.append(string.ascii_letters)
    if digits_var.get():
        character_sets.append(string.digits)
    if symbols_var.get():
        character_sets.append(SYMBOLS)

    if not character_sets:
        messagebox.showerror(
            "Selection Required",
            "Please select at least one character type."
        )
        return

    all_characters = "".join(character_sets)
    password = "".join(secrets.choice(all_characters) for _ in range(length))

    password_var.set(password)

    entropy = calculate_entropy(password)
    label, color = strength_from_entropy(entropy)
    strength_label.config(
        text=f"Strength: {label} ({entropy} bits)",
        fg=color
    )


def copy_password():
    if password_var.get():
        root.clipboard_clear()
        root.clipboard_append(password_var.get())
        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard successfully."
        )

# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Secure Password Studio")
root.geometry("520x560")
root.configure(bg=AZURE_MIST)
root.resizable(False, False)

# Title
tk.Label(
    root,
    text="Secure Password Studio",
    font=("Segoe UI", 20, "bold"),
    bg=AZURE_MIST,
    fg=JUNGLE_TEAL
).pack(pady=20)

# Main Card
card = tk.Frame(root, bg=MINT_CREAM)
card.pack(padx=30, pady=10, fill="both")

# Password Length
tk.Label(
    card,
    text="Password Length (8–32 characters)",
    font=("Segoe UI", 11, "bold"),
    bg=MINT_CREAM,
    fg="black"
).pack(pady=(15, 5))

length_entry = tk.Entry(
    card,
    width=12,
    font=("Segoe UI", 11),
    justify="center"
)
length_entry.insert(0, "")
length_entry.pack(pady=(0, 10))

# Options
letters_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    card,
    text="Include Letters (A–Z, a–z)",
    variable=letters_var,
    bg=MINT_CREAM,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=25)

tk.Checkbutton(
    card,
    text="Include Numbers (0–9)",
    variable=digits_var,
    bg=MINT_CREAM,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=25)

tk.Checkbutton(
    card,
    text="Include Symbols (!@#$%^&*)",
    variable=symbols_var,
    bg=MINT_CREAM,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=25)

# Generate Button
tk.Button(
    root,
    text="Generate Secure Password",
    bg=JUNGLE_TEAL,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    cursor="hand2",
    command=generate_password
).pack(pady=25)

# Result
password_var = tk.StringVar()
tk.Entry(
    root,
    textvariable=password_var,
    font=("Consolas", 13),
    justify="center",
    width=38
).pack(pady=6)

# Strength
strength_label = tk.Label(
    root,
    text="Strength:",
    font=("Segoe UI", 11, "bold"),
    bg=AZURE_MIST,
    fg=JUNGLE_TEAL
)
strength_label.pack(pady=6)

# Copy Button
tk.Button(
    root,
    text="Copy Password",
    bg=MUTED_TEAL,
    fg="black",
    font=("Segoe UI", 10),
    cursor="hand2",
    command=copy_password
).pack(pady=12)

root.mainloop()
