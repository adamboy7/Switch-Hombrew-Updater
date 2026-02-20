import os
import tkinter.messagebox as messagebox

from actions.config import DOWNLOADS_DIR_NAME

def clear_downloads_action():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    output_dir = os.path.join(base_dir, DOWNLOADS_DIR_NAME)
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        messagebox.showinfo("Clear Downloads", "All downloads have been cleared.")
    else:
        messagebox.showinfo("Clear Downloads", "No downloads to clear.")
