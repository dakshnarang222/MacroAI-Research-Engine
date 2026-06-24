import pandas as pd
import os

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UNIVERSE_CSV = os.path.join(BASE_DIR, "../data/universe.csv")

def sanitize_csv():
    print(f"🧼 Scrubbing {UNIVERSE_CSV}...")
    
    if not os.path.exists(UNIVERSE_CSV):
        print("❌ Universe file not found.")
        return

    df = pd.read_csv(UNIVERSE_CSV)
    original_count = len(df)
    
    # 1. REMOVE BAD SUFFIXES
    # Filter out rows where Ticker contains garbage
    bad_patterns = ["_PRICE", "_LATEST", "USD-USD", "HELOC"]
    
    df_clean = df.copy()
    for pattern in bad_patterns:
        df_clean = df_clean[~df_clean['Ticker'].str.contains(pattern, na=False)]
        
    # 2. REMOVE DUPLICATES
    df_clean = df_clean.drop_duplicates(subset=['Ticker'])
    
    removed_count = original_count - len(df_clean)
    
    # Save back
    df_clean.to_csv(UNIVERSE_CSV, index=False)
    
    print(f"✅ Scrub Complete.")
    print(f"   Removed {removed_count} bad rows.")
    print(f"   New Total: {len(df_clean)}")

if __name__ == "__main__":
    sanitize_csv()