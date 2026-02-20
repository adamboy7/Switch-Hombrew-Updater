import tkinter as tk
import tkinter.messagebox as messagebox

def add_repository_action():
    add_window = tk.Toplevel()
    add_window.title("Add Repository")
    add_window.columnconfigure(1, weight=1)

    tk.Label(add_window, text="Repository:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tk.Label(add_window, text="Pattern (optional):").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    repo_entry = tk.Entry(add_window)
    repo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    pattern_entry = tk.Entry(add_window)
    pattern_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def save_repository():
        repo = repo_entry.get().strip()
        pattern = pattern_entry.get().strip() or None
        if repo:
            with open("config.txt", "a") as config_file:
                config_file.write(f"{repo}:{pattern}\\n" if pattern else f"{repo}\\n")
            messagebox.showinfo("Add Repository", "Repository added successfully.")
            add_window.destroy()
        else:
            messagebox.showwarning("Add Repository", "Repository cannot be empty.")

    tk.Button(add_window, text="Add", command=save_repository).grid(row=2, column=0, columnspan=2, pady=10)
