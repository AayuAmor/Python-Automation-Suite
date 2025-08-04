"""
Intelligent File Organizer
"""
import os
import shutil
from collections import defaultdict

def organize_files_by_extension(directory):
    try:
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist.")
            return
        
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            print(f"No files found in directory '{directory}'.")
            return
        
        ext_map = defaultdict(list)
        for f in files:
            ext = os.path.splitext(f)[1][1:] or 'no_extension'
            ext_map[ext].append(f)
        
        for ext, files in ext_map.items():
            ext_dir = os.path.join(directory, ext)
            os.makedirs(ext_dir, exist_ok=True)
            for f in files:
                shutil.move(os.path.join(directory, f), os.path.join(ext_dir, f))
        
        print(f"Organized {len(files)} files in {directory} by extension.")
    except Exception as e:
        print(f"Error organizing files: {e}")
