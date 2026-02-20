import os
import shutil
import zipfile
import py7zr

def prompt_user_overwrite(dest_path):
    # Placeholder for the user prompt function to overwrite files
    # Returns True to overwrite, False otherwise
    print(f"File {dest_path} already exists. Prompting user for overwrite.")
    # Replace with actual user prompt logic
    return True  # Default behavior for this example

def move_or_merge(src, dest):
    """Move or merge a directory/file, asking for overwrite only on file conflicts."""
    if os.path.isdir(src):
        if not os.path.exists(dest):
            shutil.move(src, dest)
            print(f"Moved directory: {src} to {dest}")
        else:
            for item in os.listdir(src):
                src_item = os.path.join(src, item)
                dest_item = os.path.join(dest, item)
                move_or_merge(src_item, dest_item)
            os.rmdir(src)
    elif os.path.isfile(src):
        if os.path.exists(dest):
            if prompt_user_overwrite(dest):
                os.remove(dest)
                shutil.move(src, dest)
                print(f"Overwritten file: {dest}")
            else:
                print(f"Skipped file: {dest}")
        else:
            shutil.move(src, dest)
            print(f"Moved file: {src} to {dest}")

def copy_or_merge(src, dest):
    """Copy or merge a directory/file, asking for overwrite only on file conflicts."""
    if os.path.isdir(src):
        if not os.path.exists(dest):
            shutil.copytree(src, dest, dirs_exist_ok=True)
            print(f"Copied directory: {src} to {dest}")
        else:
            for item in os.listdir(src):
                src_item = os.path.join(src, item)
                dest_item = os.path.join(dest, item)
                copy_or_merge(src_item, dest_item)
    elif os.path.isfile(src):
        if os.path.exists(dest):
            if prompt_user_overwrite(dest):
                shutil.copy2(src, dest)
                print(f"Overwritten file: {dest}")
            else:
                print(f"Skipped file: {dest}")
        else:
            shutil.copy2(src, dest)
            print(f"Copied file: {src} to {dest}")

def process_downloads_action():
    # Set directories
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    downloads_dir = os.path.join(base_dir, "Downloads")
    output_dir = os.path.join(base_dir, "Output")
    processing_dir = os.path.join(base_dir, "Processing")

    # Specific folder names to look for
    target_folders = {"atmosphere", "switch", "bootloader"}

    # Ensure necessary directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(processing_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "switch"), exist_ok=True)

    # Step 1: Move .NRO files to Output/switch
    for item in os.listdir(downloads_dir):
        item_path = os.path.join(downloads_dir, item)
        if item.lower().endswith(".nro"):
            switch_dir = os.path.join(output_dir, "switch")
            os.makedirs(switch_dir, exist_ok=True)
            shutil.move(item_path, os.path.join(switch_dir, item))
            print(f"Moved .NRO file: {item} to Output/switch")

    # Step 1.5: Move .OVL files to Output/switch/.overlays
    for item in os.listdir(downloads_dir):
        item_path = os.path.join(downloads_dir, item)
        if item.lower().endswith(".ovl"):
            overlays_dir = os.path.join(output_dir, "switch", ".overlays")
            os.makedirs(overlays_dir, exist_ok=True)
            shutil.move(item_path, os.path.join(overlays_dir, item))
            print(f"Moved .OVL file: {item} to Output/switch/.overlays")

    # Step 2: Extract valid archive files into Processing
    for item in os.listdir(downloads_dir):
        item_path = os.path.join(downloads_dir, item)
        extract_dir = os.path.join(processing_dir, os.path.splitext(item)[0])
        try:
            if item.lower().endswith(".zip"):
                with zipfile.ZipFile(item_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                os.remove(item_path)
                print(f"Extracted and removed .zip file: {item}")
            elif item.lower().endswith(".7z"):
                with py7zr.SevenZipFile(item_path, mode='r') as seven_zip:
                    seven_zip.extractall(extract_dir)
                os.remove(item_path)
                print(f"Extracted and removed .7z file: {item}")
        except Exception as e:
            print(f"Failed to extract {item}: {e}")

    # Step 3: Crawl Processing for target folders and move entire directory contents to Output
    for foldername in os.listdir(processing_dir):
        folder_path = os.path.join(processing_dir, foldername)
        if os.path.isdir(folder_path):
            has_target = False
            for root, dirs, files in os.walk(folder_path):
                for dir_name in dirs:
                    if dir_name in target_folders:
                        target_path = os.path.join(root, dir_name)
                        dest_path = os.path.join(output_dir, dir_name)
                        os.makedirs(dest_path, exist_ok=True)
                        for item in os.listdir(target_path):
                            move_or_merge(os.path.join(target_path, item), os.path.join(dest_path, item))
                        has_target = True
            if has_target:
                for item in os.listdir(folder_path):
                    move_or_merge(os.path.join(folder_path, item), os.path.join(output_dir, item))

    # Step 4: Remove empty folders from Processing
    def remove_empty_folders(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for d in dirs:
                dir_path = os.path.join(root, d)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"Removed empty folder: {dir_path}")

    remove_empty_folders(processing_dir)

    # Step 5: Handle remaining unprocessed folders in Processing
    for foldername in os.listdir(processing_dir):
        folder_path = os.path.join(processing_dir, foldername)
        if os.path.isdir(folder_path):
            switch_dir = os.path.join(output_dir, "switch")
            os.makedirs(switch_dir, exist_ok=True)
            print(f"Unprocessed folder {foldername} found, assuming switch homebrew app")
            shutil.move(folder_path, os.path.join(switch_dir, foldername))

    # Step 6: Copy contents of Persistent folder to Output
    persistent_dir = os.path.join(base_dir, "Persistent")
    if os.path.exists(persistent_dir):
        for item in os.listdir(persistent_dir):
            src_path = os.path.join(persistent_dir, item)
            dest_path = os.path.join(output_dir, item)
            copy_or_merge(src_path, dest_path)
    print("Persistent folder contents have been copied to Output.")
    
    # Check if Processing folder is empty and delete it if so
    if not os.listdir(processing_dir):  # Check if folder is empty
        os.rmdir(processing_dir)  # Remove empty folder
        print("Processing folder was empty and has been deleted.")
    else:
        print("Processing folder is not empty, so it was not deleted.")


    print("Processing complete.")
