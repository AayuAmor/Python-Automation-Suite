"""
Batch File Renamer with Undo Support
"""
import os
import json
from datetime import datetime

# Global variable to store rename history
rename_history = []

def save_rename_history():
    """Save rename history to a JSON file"""
    try:
        with open('rename_history.json', 'w') as f:
            json.dump(rename_history, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save rename history: {e}")

def load_rename_history():
    """Load rename history from JSON file"""
    global rename_history
    try:
        if os.path.exists('rename_history.json'):
            with open('rename_history.json', 'r') as f:
                rename_history = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load rename history: {e}")
        rename_history = []

def batch_rename(directory, prefix):
    try:
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist.")
            return False
        
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            print(f"No files found in directory '{directory}'.")
            return False
        
        # Create a rename session
        session = {
            'timestamp': datetime.now().isoformat(),
            'directory': directory,
            'prefix': prefix,
            'operations': []
        }
        
        success_count = 0
        for idx, filename in enumerate(files, 1):
            try:
                ext = os.path.splitext(filename)[1]
                new_name = f"{prefix}_{idx:03d}{ext}"
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                
                # Skip if target file already exists
                if os.path.exists(new_path) and old_path != new_path:
                    print(f"Skipped: {filename} -> {new_name} (target exists)")
                    continue
                
                os.rename(old_path, new_path)
                
                # Record the operation for undo
                session['operations'].append({
                    'old_name': filename,
                    'new_name': new_name,
                    'old_path': old_path,
                    'new_path': new_path
                })
                
                success_count += 1
                print(f"Renamed: {filename} -> {new_name}")
                
            except Exception as e:
                print(f"Error renaming {filename}: {e}")
        
        if success_count > 0:
            # Add session to history and save
            rename_history.append(session)
            save_rename_history()
            print(f"\n✅ Successfully renamed {success_count} files in {directory} with prefix '{prefix}'.")
            print(f"📝 Rename session saved. Use undo_last_rename() or undo_rename_session() to revert.")
        else:
            print("❌ No files were renamed.")
            
        return success_count > 0
        
    except Exception as e:
        print(f"Error renaming files: {e}")
        return False
