import os
import pandas as pd

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "../data/raw")

def strict_purge():
    print(f"🔥 STARTING STRICT PRICE CHECK & TRIM on {RAW_DIR}...")
    
    deleted_count = 0
    trimmed_count = 0
    kept_count = 0
    
    for root, dirs, files in os.walk(RAW_DIR):
        for file in files:
            if not file.endswith(".csv"): continue
                
            filepath = os.path.join(root, file)
            
            try:
                # 1. Load CSV
                df = pd.read_csv(filepath)
                # Standardize column names (lowercase, strip spaces)
                df.columns = [c.lower().strip() for c in df.columns]
                
                # 2. Find Price Column
                price_col = None
                for col in ['close', 'adj close', 'value']:
                    if col in df.columns:
                        price_col = col
                        break
                
                # 3. ANALYZE DATA QUALITY
                # We extract ONLY the rows where price is NOT empty
                if price_col:
                    valid_rows = df.dropna(subset=[price_col])
                else:
                    valid_rows = pd.DataFrame() # No price col = invalid
                
                # 4. DECISION LOGIC
                if valid_rows.empty:
                    # Case A: File is completely dead (All NaNs)
                    print(f"   🗑 Deleting Ghost File (No Prices): {file}")
                    os.remove(filepath)
                    deleted_count += 1
                elif len(valid_rows) < 10:
                    # Case B: File has barely any data (<10 rows)
                    print(f"   🗑 Deleting Tiny File (<10 rows): {file}")
                    os.remove(filepath)
                    deleted_count += 1
                else:
                    # Case C: File has data!
                    # Check if we need to trim the "Black Space" (NaNs at start)
                    if len(valid_rows) < len(df):
                        # Overwrite the file with ONLY the valid rows
                        # This removes the 2000-2010 empty rows from Bitcoin files
                        valid_rows.to_csv(filepath, index=False)
                        trimmed_count += 1
                        # print(f"   ✂️ Trimmed empty rows: {file}")
                    
                    kept_count += 1
                        
            except Exception as e:
                print(f"   ❌ Corrupt File: {file} ({e})")
                os.remove(filepath)
                deleted_count += 1

    print("\n" + "="*30)
    print("STRICT PURGE & TRIM RESULTS")
    print("="*30)
    print(f"🗑  TRASHED: {deleted_count} (Ghosts/Empty)")
    print(f"✂️  TRIMMED: {trimmed_count} (Fixed Sparse Starts)")
    print(f"✅ VALID:   {kept_count} (Ready for AI)")
    print("="*30)

if __name__ == "__main__":
    strict_purge()