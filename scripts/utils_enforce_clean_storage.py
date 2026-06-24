import os
import pandas as pd
import re

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "../data/raw")
UNIVERSE_CSV = os.path.join(BASE_DIR, "../data/universe.csv")

def enforce_clean_storage():
    print(f"🧹 STARTING STORAGE ENFORCEMENT...")
    
    # 1. Load the Approved List
    if not os.path.exists(UNIVERSE_CSV):
        print("❌ Universe file missing. Cannot enforce.")
        return
        
    df = pd.read_csv(UNIVERSE_CSV)
    # Create a set of valid tickers for O(1) lookup
    valid_tickers = set(df['Ticker'].unique())
    print(f"   📋 Approved Tickers: {len(valid_tickers)}")
    
    deleted_count = 0
    kept_count = 0
    
    # 2. Walk the Storage
    for root, dirs, files in os.walk(RAW_DIR):
        for file in files:
            if not file.endswith(".csv") and not file.endswith(".parquet"):
                continue
                
            filepath = os.path.join(root, file)
            
            # Extract Ticker from Filename
            # Expected Format: Market_TICKER_YYYYMMDD.csv
            # We want to grab the "TICKER" part strictly
            
            # Remove extension
            name_no_ext = os.path.splitext(file)[0]
            
            # Regex to find the Ticker part
            # It looks for "Market_" prefix and "_202..." suffix
            match = re.search(r"Market_([A-Z0-9\-\.\=\^]+)_\d{8}", name_no_ext)
            
            if match:
                file_ticker = match.group(1)
                
                # THE CHECK: Is this ticker in our Approved List?
                if file_ticker in valid_tickers:
                    kept_count += 1
                else:
                    # It looks like a valid file format, but the ticker isn't in our universe
                    # This catches 'PY-USD' because universe only has 'PYUSD-USD'
                    print(f"   🗑 Deleting Unlisted Asset: {file} (Ticker: {file_ticker})")
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                    except Exception as e:
                        print(f"      Error: {e}")
            else:
                # File doesn't match standard naming convention at all
                # e.g. "PY-USD_latest.csv" or "BadData.csv"
                # If it's a Macro file, skip (don't delete)
                if "Macro_" in file:
                    continue
                    
                print(f"   🗑 Deleting Rogue File: {file}")
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"      Error: {e}")

    print("\n" + "="*30)
    print("STORAGE ENFORCEMENT COMPLETE")
    print("="*30)
    print(f"✅ KEPT:    {kept_count} (Valid Files)")
    print(f"🗑  DELETED: {deleted_count} (Duplicates/Ghosts)")
    print("="*30)

if __name__ == "__main__":
    enforce_clean_storage()