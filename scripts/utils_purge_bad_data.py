import os
import pandas as pd

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "../data/raw")

def purge_bad_data():
    print(f"🔥 STARTING DATA PURGE on {RAW_DIR}...")
    
    deleted_count = 0
    kept_count = 0
    
    # Walk through every file
    for root, dirs, files in os.walk(RAW_DIR):
        for file in files:
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)
                
                try:
                    # 1. Read the file
                    df = pd.read_csv(filepath)
                    
                    # 2. THE STRICT CHECK
                    # Must have at least 10 rows of data
                    # Must not be all NaNs
                    if len(df) < 10 or df.dropna(how='all').empty:
                        print(f"   🗑 Deleting Empty/Corrupt File: {file}")
                        os.remove(filepath)
                        deleted_count += 1
                    else:
                        kept_count += 1
                        
                except Exception as e:
                    print(f"   ❌ Error reading {file}, deleting it. ({e})")
                    os.remove(filepath)
                    deleted_count += 1

    print("\n" + "="*30)
    print("PURGE RESULTS")
    print("="*30)
    print(f"🗑  TRASHED: {deleted_count} files (Empty/Corrupt)")
    print(f"✅ KEPT:    {kept_count} files (Valid Data)")
    print("="*30)
    
    if deleted_count > 0:
        print("⚠️  You now need to regenerate your Universe Map.")

if __name__ == "__main__":
    purge_bad_data()