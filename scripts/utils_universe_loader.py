import pandas as pd
import os

# CONFIGURATION
UNIVERSE_CSV = "../data/universe.csv"

def load_universe():
    """
    Layer 1 Utility: Loads the asset universe from CSV.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, UNIVERSE_CSV)

    if os.path.exists(csv_path):
        try:
            # Read CSV directly
            df = pd.read_csv(csv_path)
            # Standardize column names
            df.columns = [c.strip().lower() for c in df.columns]
            return df
        except Exception as e:
            print(f"Error reading universe.csv: {e}")
            return pd.DataFrame()

    print(f"CRITICAL ERROR: universe.csv not found at {csv_path}")
    return pd.DataFrame()

if __name__ == "__main__":
    df = load_universe()
    if not df.empty:
        print(f"Universe Loaded. Assets: {len(df)}")