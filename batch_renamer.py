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

def undo_last_rename():
    """Undo the most recent rename operation"""
    global rename_history
    
    if not rename_history:
        print("❌ No rename operations to undo.")
        return False
    
    session = rename_history[-1]
    return undo_rename_session(len(rename_history) - 1)

def undo_rename_session(session_index):
    """Undo a specific rename session by index"""
    global rename_history
    
    if session_index < 0 or session_index >= len(rename_history):
        print(f"❌ Invalid session index: {session_index}")
        return False
    
    session = rename_history[session_index]
    directory = session['directory']
    
    if not os.path.exists(directory):
        print(f"❌ Directory no longer exists: {directory}")
        return False
    
    print(f"🔄 Undoing rename session from {session['timestamp']}")
    print(f"📁 Directory: {directory}")
    print(f"🏷️ Prefix: {session['prefix']}")
    
    success_count = 0
    failed_operations = []
    
    # Reverse the operations (undo in reverse order)
    for operation in reversed(session['operations']):
        try:
            old_name = operation['old_name']
            new_name = operation['new_name']
            # Current path (what the file is named now)
            current_path = os.path.join(directory, new_name)
            # Target path (what we want to rename it back to)
            target_path = os.path.join(directory, old_name)
            
            if not os.path.exists(current_path):
                print(f"⚠️ File not found: {new_name} (may have been moved or deleted)")
                failed_operations.append(operation)
                continue
            
            if os.path.exists(target_path) and current_path != target_path:
                print(f"⚠️ Cannot restore {new_name} -> {old_name} (target exists)")
                failed_operations.append(operation)
                continue
            
            os.rename(current_path, target_path)
            print(f"✅ Restored: {new_name} -> {old_name}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error restoring {operation['new_name']}: {e}")
            failed_operations.append(operation)
    
    if success_count > 0:
        # Remove the session from history if all operations were successful
        if not failed_operations:
            rename_history.pop(session_index)
            save_rename_history()
            print(f"\n✅ Successfully undid {success_count} rename operations.")
            print("📝 Session removed from history.")
        else:
            print(f"\n⚠️ Partially undid {success_count} operations. {len(failed_operations)} operations failed.")
    else:
        print("❌ No operations could be undone.")
    
    return success_count > 0
