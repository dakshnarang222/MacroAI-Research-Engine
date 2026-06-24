import pandas as pd
import yfinance as yf
from datetime import datetime
import os
import time
import sys
import shutil
import warnings

# SILENCE WARNINGS (Suppress yfinance FutureWarnings)
warnings.simplefilter(action='ignore', category=FutureWarning)

# Ensure loader exists and can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from utils_universe_loader import load_universe
except ImportError:
    print("❌ Critical Error: utils_universe_loader.py missing.")
    sys.exit(1)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_ROOT = os.path.join(BASE_DIR, "../data/raw")
CLEANED_ROOT = os.path.join(BASE_DIR, "../data/cleaned")

FED_SERIES = {
    'Liquidity_FedAssets': 'WALCL',
    'Yield_10Y': 'DGS10',
    'Yield_3M': 'DGS3MO',
    'Inflation_CPI': 'CPIAUCSL',
    'Yield_Corporate_BBB': 'BAMLC0A4CBBB'
}

def get_timestamp():
    return datetime.now().strftime('%Y%m%d')

def clear_yfinance_cache():
    """Nukes cache to prevent database locks."""
    cache_dirs = [
        os.path.join(os.path.expanduser("~"), "Library", "Caches", "py-yfinance"),
        os.path.join(os.path.expanduser("~"), ".cache", "py-yfinance")
    ]
    for d in cache_dirs:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
            except:
                pass

def get_save_paths(category, ticker, filename_base):
    safe_category = category.replace(" ", "_").replace("/", "-")
    raw_cat_path = os.path.join(RAW_ROOT, safe_category)
    clean_cat_path = os.path.join(CLEANED_ROOT, safe_category)
    
    os.makedirs(raw_cat_path, exist_ok=True)
    os.makedirs(clean_cat_path, exist_ok=True)
    
    raw_full = os.path.join(raw_cat_path, f"{filename_base}.csv")
    clean_full = os.path.join(clean_cat_path, f"{filename_base}.parquet")
    return raw_full, clean_full

def validate_and_save(df, raw_path, clean_path):
    """
    PARANOID VALIDATION: Checks specific columns for actual data.
    """
    if df is None or df.empty:
        return False
        
    # Standardize column names to lowercase for checking
    # Note: We work on a copy to not mess up the save
    check_df = df.copy()
    check_df.columns = [c.lower() for c in check_df.columns]
    
    # 1. Check for 'close' or 'adj close'
    close_col = None
    if 'close' in check_df.columns:
        close_col = 'close'
    elif 'adj close' in check_df.columns:
        close_col = 'adj close'
    elif 'value' in check_df.columns: # FRED Data
        close_col = 'value'
        
    # If no price column exists, fail
    if not close_col:
        return False
        
    # 2. Check for Non-NaN values
    valid_prices = check_df[close_col].dropna()
    if valid_prices.empty:
        return False
        
    # 3. Check for Zero values (some APIs return 0.0 for missing data)
    # We allow some 0s (e.g. oil futures went negative once), but not ALL 0s
    if (valid_prices == 0).all():
        return False

    # 4. Check Length (For MAX history, we expect > 10 rows)
    if len(valid_prices) < 10:
        return False

    # If we pass all checks, SAVE.
    df.to_csv(raw_path)
    
    try:
        # Parquet Logic
        df_clean = df.copy()
        if isinstance(df_clean.columns, pd.MultiIndex):
            df_clean.columns = ["_".join(col).strip() for col in df_clean.columns.values]
        else:
            df_clean.columns = [c.lower() for c in df_clean.columns]
        df_clean.ffill().to_parquet(clean_path)
    except Exception:
        pass 
        
    return True

def ingest_asset_universe():
    today_str = get_timestamp()
    universe = load_universe()
    
    if universe.empty:
        print("⚠️ No assets to ingest.")
        return

    ticker_cat_map = dict(zip(universe['ticker'], universe['category']))
    tickers = list(ticker_cat_map.keys())
    total_assets = len(tickers)
    
    print(f"🚀 Starting Deep Ingestion (MAX History) for {total_assets} Assets...")

    success_count = 0
    fail_count = 0
    batch_size = 20
    
    for i in range(0, total_assets, batch_size):
        batch = tickers[i:i + batch_size]
        print(f"   ...Processing batch {i} to {i+len(batch)}...")
        
        try:
            if i % 100 == 0: clear_yfinance_cache()
            
            # period="max" gets everything
            data = yf.download(
                batch, 
                period="max", 
                group_by='ticker', 
                progress=False, 
                threads=False, 
                auto_adjust=False
            )
            
            for ticker in batch:
                try:
                    df_asset = pd.DataFrame()
                    
                    if len(batch) > 1:
                        if ticker in data.columns.levels[0]:
                            df_asset = data[ticker]
                        else:
                            fail_count += 1
                            continue 
                    else:
                        df_asset = data
                    
                    category = ticker_cat_map.get(ticker, "Uncategorized")
                    filename_base = f"Market_{ticker}_{today_str}"
                    raw_path, clean_path = get_save_paths(category, ticker, filename_base)

                    if validate_and_save(df_asset, raw_path, clean_path):
                        success_count += 1
                    else:
                        # print(f"      Validation Failed for {ticker} (Empty/NaNs)")
                        fail_count += 1
                        
                except Exception:
                    fail_count += 1
            
            time.sleep(1.0) 
            
        except Exception as e:
            print(f"   ❌ Batch Error: {e}")
            fail_count += len(batch)
    
    # --- AUDIT REPORT ---
    net_valid = total_assets - fail_count
    
    print("\n" + "="*40)
    print(f"📊 INGESTION AUDIT [{datetime.now().strftime('%H:%M:%S')}]")
    print("="*40)
    print(f"   Total Requested:    {total_assets}")
    print(f"   - Failed Downloads: {fail_count}")
    print(f"   ---------------------------")
    print(f"   = NET VALID ASSETS: {net_valid}  (Yield: {(net_valid/total_assets)*100:.1f}%)")
    print("="*40 + "\n")

def ingest_macro_data():
    print("🦅 Starting Macro/Fed Ingestion (Deep History)...")
    today_str = get_timestamp()
    for name, series_id in FED_SERIES.items():
        try:
            url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
            df = pd.read_csv(url, index_col=0, parse_dates=True)
            if not df.empty:
                filename_base = f"Macro_FRED_{name}_{today_str}"
                raw_path, clean_path = get_save_paths("Macro", name, filename_base)
                df.columns = ['close']
                validate_and_save(df, raw_path, clean_path)
        except Exception as e:
            print(f"      ❌ Error: {e}")

if __name__ == "__main__":
    print(f"--- 🟢 NIGHTLY INGEST AGENT STARTED: {datetime.now()} ---")
    clear_yfinance_cache()
    ingest_macro_data()
    ingest_asset_universe()
    print(f"--- 🏁 INGESTION COMPLETE: {datetime.now()} ---")