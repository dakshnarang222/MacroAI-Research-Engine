import os
import shutil
import time

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

# Source: The folder you want to empty (raw 2)
SOURCE_DIR = os.path.join(DATA_DIR, "raw 2")
# Destination: The main folder (raw)
DEST_DIR = os.path.join(DATA_DIR, "raw")

def get_file_timestamp(filepath):
    """Returns the last modification time of a file."""
    return os.path.getmtime(filepath)

def merge_folders():
    print(f"--- STARTING SMART MERGE ---")
    print(f"Source:      {SOURCE_DIR}")
    print(f"Destination: {DEST_DIR}")
    
    if not os.path.exists(SOURCE_DIR):
        print("❌ Source folder 'raw 2' does not exist. Nothing to do.")
        return

    files_moved = 0
    files_skipped = 0
    files_overwritten = 0

    # Walk through Source (raw 2)
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file == ".DS_Store": continue # Skip Mac system files
            
            source_path = os.path.join(root, file)
            
            # Determine relative path (e.g., "Crypto/BTCUSD_latest.csv")
            rel_path = os.path.relpath(source_path, SOURCE_DIR)
            dest_path = os.path.join(DEST_DIR, rel_path)
            
            # Ensure destination folder exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # CHECK FOR CONFLICT
            if os.path.exists(dest_path):
                src_time = get_file_timestamp(source_path)
                dest_time = get_file_timestamp(dest_path)
                
                # Compare Logic: Only overwrite if Source is NEWER
                if src_time > dest_time:
                    try:
                        shutil.move(source_path, dest_path)
                        print(f"⚠️  Overwrote OLDER file in destination: {rel_path}")
                        files_overwritten += 1
                    except Exception as e:
                        print(f"❌ Error overwriting {rel_path}: {e}")
                else:
                    # Destination is newer or same age, keep destination
                    # Optional: Delete the source file since we already have a copy
                    try:
                        os.remove(source_path)
                        files_skipped += 1
                    except Exception as e:
                        print(f"❌ Error removing skipped file {rel_path}: {e}")
            else:
                # No conflict, just move it
                try:
                    shutil.move(source_path, dest_path)
                    files_moved += 1
                except Exception as e:
                    print(f"❌ Error moving {rel_path}: {e}")

    # CLEANUP: Remove empty folders in Source
    for root, dirs, files in os.walk(SOURCE_DIR, topdown=False):
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except OSError:
                pass # Directory not empty
    
    # Try to remove the root 'raw 2' if empty
    try:
        os.rmdir(SOURCE_DIR)
        print("\n✅ 'raw 2' folder was empty and has been removed.")
    except OSError:
        print("\n⚠️  'raw 2' could not be fully removed (files might remain). Check manually.")

    print("\n--- MERGE COMPLETE ---")
    print(f"Files Moved (New):        {files_moved}")
    print(f"Files Overwritten (Updated): {files_overwritten}")
    print(f"Files Skipped (Duplicate/Old): {files_skipped}")

if __name__ == "__main__":
    merge_folders()