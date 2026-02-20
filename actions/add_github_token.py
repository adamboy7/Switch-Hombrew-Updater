import tkinter as tk
import tkinter.messagebox as messagebox
from dotenv import set_key

from actions.config import get_env_path

def add_github_token_action():
    token_window = tk.Toplevel()
    token_window.title("Add GitHub Token")
    token_window.columnconfigure(1, weight=1)

    tk.Label(token_window, text="GitHub Token:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    token_entry = tk.Entry(token_window)
    token_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def save_token():
        token = token_entry.get().strip()
        token = token if token else "None"
        set_key(get_env_path(), "GITHUB_TOKEN", token)
        messagebox.showinfo("GitHub Token", "GitHub token updated successfully.")
        token_window.destroy()

    tk.Button(token_window, text="Save", command=save_token).grid(row=1, column=0, columnspan=2, pady=10)
