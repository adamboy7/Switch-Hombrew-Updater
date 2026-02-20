import os
import tkinter.messagebox as messagebox

def clear_downloads_action():
    output_dir = "Downloads"
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        messagebox.showinfo("Clear Downloads", "All downloads have been cleared.")
    else:
        messagebox.showinfo("Clear Downloads", "No downloads to clear.")
