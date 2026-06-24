import os
import glob

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "../data/raw")

def cleanup_legacy_filenames():
    print(f"🧹 STARTING FILENAME CLEANUP in {RAW_DIR}...")
    
    deleted_count = 0
    
    # Walk through all folders
    for root, dirs, files in os.walk(RAW_DIR):
        for file in files:
            # Target files with the "Wrong Naming Convention"
            if "_LATEST" in file or "_PRICE" in file:
                filepath = os.path.join(root, file)
                
                try:
                    os.remove(filepath)
                    print(f"   🗑 Deleted Legacy File: {file}")
                    deleted_count += 1
                except Exception as e:
                    print(f"   ❌ Error deleting {file}: {e}")

    print("\n" + "="*30)
    print(f"CLEANUP COMPLETE")
    print(f"Deleted {deleted_count} improperly named files.")
    print("="*30)

if __name__ == "__main__":
    cleanup_legacy_filenames()