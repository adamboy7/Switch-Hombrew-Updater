# Main application file
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv
import os
from actions.clear_downloads import clear_downloads_action
from actions.add_repository import add_repository_action
from actions.add_github_token import add_github_token_action
from actions.process_downloads import process_downloads_action
from actions.download import start_download
from actions.config import load_config

class App(tk.Tk):
    def __init__(self, files_to_download, github_token=None):
        super().__init__()

        self.files_to_download = files_to_download
        self.github_token = github_token

        self.title("GitHub Release Downloader")
        self.geometry("600x400")

        self.check_vars = {}
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        label = ttk.Label(frame, text="Select files to download:")
        label.pack(anchor=tk.W, pady=5)

        self.check_vars = {}
        for file in self.files_to_download:
            var = tk.BooleanVar(value=True)
            self.check_vars[file["repo"]] = var

            pattern_text = f" ({file['pattern']})" if file.get("pattern") else " (Download All)"
            check = ttk.Checkbutton(
                frame,
                text=f"{file['repo']}{pattern_text}",
                variable=var
            )
            check.pack(anchor=tk.W, pady=2)

        download_button = ttk.Button(
            frame, text="Download Selected", command=self.download_selected
        )
        download_button.pack(pady=10)

    def create_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Clear Downloads", command=clear_downloads_action)
        file_menu.add_command(label="Process Downloads", command=process_downloads_action)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        configure_menu = tk.Menu(menu_bar, tearoff=0)
        configure_menu.add_command(label="Add a Repository", command=add_repository_action)
        configure_menu.add_command(label="Add a GitHub Token", command=add_github_token_action)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Configure", menu=configure_menu)

        self.config(menu=menu_bar)

    def download_selected(self):
        selected_files = [
            file for file in self.files_to_download if self.check_vars.get(file["repo"]) and self.check_vars[file["repo"]].get()
        ]
        if not selected_files:
            messagebox.showwarning("No Selection", "No files selected for download.")
            return

        start_download(selected_files, self.github_token)
        messagebox.showinfo("Download Complete", "Selected files have been downloaded.")

def main():
    # Load repositories and patterns from config file
    config_file = "config.txt"
    files_to_download = load_config(config_file)

    if not files_to_download:
        print("No valid entries found in config file. Exiting.")
        exit(1)

    # Load the GitHub token from the environment (Loaded when we ran load_config)
    github_token = os.getenv("GITHUB_TOKEN")
    github_token = None if github_token == "None" else github_token

    global app
    app = App(files_to_download, github_token)
    app.mainloop()

if __name__ == "__main__":
    # Ensure .env file exists
    if not os.path.exists(".env"):
        with open(".env", "w") as env_file:
            env_file.write("GITHUB_TOKEN=None\n")

    load_dotenv()
    main()
