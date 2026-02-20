import os
import shutil
import tkinter.messagebox as messagebox

from actions.config import DOWNLOADS_DIR_NAME

def clear_downloads_action():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    output_dir = os.path.join(base_dir, DOWNLOADS_DIR_NAME)
    if os.path.exists(output_dir):
        for entry in os.listdir(output_dir):
            entry_path = os.path.join(output_dir, entry)
            if os.path.isfile(entry_path):
                os.remove(entry_path)
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
        messagebox.showinfo("Clear Downloads", "All contents in Downloads have been fully cleared.")
    else:
        messagebox.showinfo("Clear Downloads", "No downloads to clear.")
