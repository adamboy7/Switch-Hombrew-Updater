import os
import shutil
import tkinter.messagebox as messagebox

from actions.config import DOWNLOADS_DIR_NAME


def clear_downloads_contents(show_message=True):
    """Clear all files and folders in the Downloads directory."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    downloads_dir = os.path.join(base_dir, DOWNLOADS_DIR_NAME)
    if os.path.exists(downloads_dir):
        for entry in os.listdir(downloads_dir):
            entry_path = os.path.join(downloads_dir, entry)
            if os.path.isfile(entry_path):
                os.remove(entry_path)
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
        if show_message:
            messagebox.showinfo("Clear Downloads", "All contents in Downloads have been fully cleared.")
        return True

    if show_message:
        messagebox.showinfo("Clear Downloads", "No downloads to clear.")
    return False

def clear_downloads_action():
    clear_downloads_contents(show_message=True)
