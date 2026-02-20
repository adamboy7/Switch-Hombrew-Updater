import requests
import os
import fnmatch
import tkinter as tk
from tkinter import ttk, messagebox
from tqdm import tqdm

def download_github_release(repo, pattern, output_dir="downloads", token=None):
    """
    Downloads all release assets matching a pattern from a GitHub repository.

    :param repo: GitHub repository in the format "owner/repo".
    :param pattern: Wildcard pattern to match the desired files, or None to download all files.
    :param output_dir: Directory to save the downloaded files.
    :param token: GitHub Personal Access Token (optional for higher rate limits).
    """
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Authorization": f"token {token}"} if token else {}

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch releases for {repo}: {response.status_code} {response.text}")
        return

    release_data = response.json()
    assets = release_data.get("assets", [])

    if not assets:
        print(f"No assets found for {repo}.")
        return

    os.makedirs(output_dir, exist_ok=True)

    downloaded_any = False
    for asset in tqdm(assets, desc=f"Downloading assets from {repo}"):
        asset_name = asset["name"]
        if not pattern or fnmatch.fnmatch(asset_name, pattern):
            download_url = asset["browser_download_url"]
            print(f"Downloading {asset_name} from {repo}...")

            file_path = os.path.join(output_dir, asset_name)

            # Download the file
            with requests.get(download_url, stream=True) as file_response:
                total_size = int(file_response.headers.get("content-length", 0))
                with open(file_path, "wb") as file:
                    with tqdm(total=total_size, unit="B", unit_scale=True, desc=asset_name) as pbar:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            file.write(chunk)
                            pbar.update(len(chunk))
            print(f"Downloaded: {file_path}")
            downloaded_any = True

    if not downloaded_any:
        print(f"No files found matching pattern: {pattern} for {repo}.")

def start_download(selected_files, github_token=None):
    for file in selected_files:
        repo = file["repo"]
        pattern = file.get("pattern", None)
        download_github_release(repo, pattern, token=github_token)

def load_config(config_file="config.txt"):
    """
    Load repositories and patterns from a configuration file.

    :param config_file: Path to the configuration file.
    :return: List of repositories and patterns.
    """
    files_to_download = []
    if not os.path.exists(config_file):
        print(f"Config file '{config_file}' not found. Exiting.")
        return files_to_download

    with open(config_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split(":", 1)
            repo = parts[0].strip()
            pattern = parts[1].strip() if len(parts) > 1 else None
            files_to_download.append({"repo": repo, "pattern": pattern})

    return files_to_download

class App(tk.Tk):
    def __init__(self, files_to_download, github_token=None):
        super().__init__()

        self.files_to_download = files_to_download
        self.github_token = github_token

        self.title("GitHub Release Downloader")
        self.geometry("600x400")

        self.check_vars = {}
        self.create_widgets()

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

    def download_selected(self):
        selected_files = [
            file for file in self.files_to_download if self.check_vars[file["repo"]].get()
        ]
        if not selected_files:
            messagebox.showwarning("No Selection", "No files selected for download.")
            return

        start_download(selected_files, self.github_token)
        messagebox.showinfo("Download Complete", "Selected files have been downloaded.")

if __name__ == "__main__":
    # Load repositories and patterns from config file
    config_file = "config.txt"
    files_to_download = load_config(config_file)

    if not files_to_download:
        print("No valid entries found in config file. Exiting.")
        exit(1)

    # Optional: Add your GitHub Personal Access Token here
    github_token = None

    app = App(files_to_download, github_token)
    app.mainloop()
