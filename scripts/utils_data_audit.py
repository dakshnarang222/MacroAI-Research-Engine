import os
import pandas as pd
from collections import defaultdict

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

FOLDER_A = os.path.join(DATA_DIR, "raw")
FOLDER_B = os.path.join(DATA_DIR, "raw 2")

def get_file_inventory(root_folder):
    inventory = {} # Key: Filename, Value: Full Path
    count = 0
    if not os.path.exists(root_folder):
        return {}, 0
        
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".csv") or file.endswith(".parquet"):
                # We use the filename as the unique key
                inventory[file] = os.path.join(root, file)
                count += 1
    return inventory, count

def audit_folders():
    print(f"--- Auditing Data Folders ---")
    print(f"   A: {FOLDER_A}")
    print(f"   B: {FOLDER_B}")
    
    inv_a, count_a = get_file_inventory(FOLDER_A)
    inv_b, count_b = get_file_inventory(FOLDER_B)
    
    print(f"\nSTATUS REPORT:")
    print(f"   Folder 'raw':   {count_a} files")
    print(f"   Folder 'raw 2': {count_b} files")
    print(f"   ---------------------------")
    print(f"   Total Assets:   {count_a + count_b}")

    # Check for Conflicts
    conflicts = []
    for filename in inv_b:
        if filename in inv_a:
            conflicts.append(filename)
            
    if len(conflicts) > 0:
        print(f"\n⚠️  WARNING: {len(conflicts)} DUPLICATE FILES FOUND!")
        print("   If you merge these, one will overwrite the other.")
        print("   Examples of conflicts:")
        for f in conflicts[:5]:
            print(f"   - {f}")
        print("\n   Run 'python scripts/utils_merge_folders.py' to resolve intelligently.")
    else:
        print("\n✅ SAFE TO MERGE")
        print("   There are NO duplicate filenames.")
        print("   Action: You can safely drag all folders from 'raw 2' into 'raw'.")

if __name__ == "__main__":
    audit_folders()