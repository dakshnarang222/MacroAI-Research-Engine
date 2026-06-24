import pandas as pd
import os

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UNIVERSE_FILE = os.path.join(BASE_DIR, "../data/universe.csv")

def audit_universe():
    print(f"📊 STARTING UNIVERSE AUDIT...")
    
    if not os.path.exists(UNIVERSE_FILE):
        print("❌ Universe file not found. Run 'utils_universe_generator.py' first.")
        return

    # Load the Map
    df = pd.read_csv(UNIVERSE_FILE)
    
    # 1. TOTAL COUNT
    total_rows = len(df)
    unique_tickers = df['Ticker'].nunique()
    
    print(f"\n--- HIGH LEVEL SUMMARY ---")
    print(f"   Total Entries:   {total_rows}")
    print(f"   Unique Assets:   {unique_tickers}")
    
    if total_rows != unique_tickers:
        print(f"   ⚠️  DUPLICATES FOUND: {total_rows - unique_tickers}")
    else:
        print(f"   ✅ No Duplicates detected.")

    # 2. DUPLICATE CHECK
    # Check if the same ticker appears in multiple categories
    if total_rows != unique_tickers:
        print(f"\n--- DUPLICATE DETAIL ---")
        duplicates = df[df.duplicated('Ticker', keep=False)].sort_values('Ticker')
        print(duplicates)

    # 3. CATEGORY BREAKDOWN
    print(f"\n--- CATEGORY BREAKDOWN ---")
    breakdown = df['Category'].value_counts()
    print(breakdown)
    
    print(f"\n" + "="*30)
    print(f"   REAL TRACKING COUNT: {unique_tickers}")
    print(f"="*30)

if __name__ == "__main__":
    audit_universe()