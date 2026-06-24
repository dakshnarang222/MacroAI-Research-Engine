import pandas as pd
import numpy as np
import os
import glob
import warnings
from datetime import datetime

# --- SILENCE WARNINGS ---
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "../data/raw")
FEATURES_DIR = os.path.join(BASE_DIR, "../data/features")
SCAN_OUTPUT = os.path.join(BASE_DIR, "../data/market_scan.csv")
MACRO_OUTPUT = os.path.join(BASE_DIR, "../data/features_macro.csv")

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def load_csv_safely(filepath):
    try:
        # Load without index first to inspect columns
        df = pd.read_csv(filepath)
        df.columns = [c.lower().strip() for c in df.columns]
        
        date_col = None
        for col in df.columns:
            if 'date' in col or 'time' in col:
                date_col = col
                break
        
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
            df.set_index(date_col, inplace=True)
            df.sort_index(inplace=True)
        else:
            return None # No date column found
        
        # Check if empty
        if df.empty: return None

        # Normalize Close Column
        if 'close' in df.columns:
            return df[['close']]
        elif 'adj close' in df.columns:
            return df[['adj close']].rename(columns={'adj close': 'close'})
        elif 'value' in df.columns:
            return df[['value']].rename(columns={'value': 'close'})
            
        return None
    except Exception:
        return None

def process_macro():
    print("   [1/2] Processing Macro Data...")
    
    macro_map = {
        "liquidity": "Liquidity_FedAssets",
        "yield_10y": "Yield_10Y",
        "yield_3m": "Yield_3M",
        "inflation": "Inflation_CPI",
        "credit_stress": "Yield_Corporate_BBB"
    }
    
    dfs = []
    # Search Macro folder specifically
    macro_path = os.path.join(RAW_DIR, "Macro")
    
    if not os.path.exists(macro_path):
        print(f"   ❌ Macro folder not found at {macro_path}")
        return

    for friendly_name, file_key in macro_map.items():
        found = False
        # Manual walk for macro files
        for file in os.listdir(macro_path):
            if file_key in file and file.endswith(".csv"):
                filepath = os.path.join(macro_path, file)
                df = load_csv_safely(filepath)
                if df is not None:
                    df.columns = [friendly_name]
                    dfs.append(df)
                    found = True
                    break # Take first match
        
        if not found:
            pass

    if not dfs:
        print("   ❌ No Macro Data processed.")
        return

    master = pd.concat(dfs, axis=1).sort_index().ffill().dropna()
    
    if 'inflation' in master.columns:
        master['inflation_rate'] = master['inflation'].pct_change(252) * 100
        master['real_rate'] = master['yield_10y'] - master['inflation_rate']
    
    if 'yield_10y' in master.columns and 'yield_3m' in master.columns:
        master['yield_curve'] = master['yield_10y'] - master['yield_3m']

    if 'liquidity' in master.columns:
        master['liquidity_trend'] = master['liquidity'].pct_change(20)

    master.to_csv(MACRO_OUTPUT)
    print(f"     ✅ Macro Features Saved: {MACRO_OUTPUT}")

def process_universe():
    print(f"   [2/2] Scanning Institutional Universe...")
    print(f"        Searching in: {RAW_DIR}")
    
    os.makedirs(FEATURES_DIR, exist_ok=True)
    scan_results = []
    
    # --- ROBUST FILE FINDER (os.walk) ---
    asset_files = []
    for root, dirs, files in os.walk(RAW_DIR):
        if os.path.basename(root) == "Macro": 
            continue 
        
        for file in files:
            if file.endswith(".csv") and not file.startswith("."):
                asset_files.append(os.path.join(root, file))

    if not asset_files:
        print("   ❌ No asset files found via os.walk().")
        return

    print(f"     Found {len(asset_files)} asset files.")
    
    count = 0
    errors = 0
    
    for filepath in asset_files:
        try:
            df = load_csv_safely(filepath)
            
            # DEBUG: Print why skipping
            if df is None: 
                # errors += 1
                # print(f"Skipping {os.path.basename(filepath)} (Load Failed or Empty)")
                continue
            
            if len(df) < 20: 
                # print(f"Skipping {os.path.basename(filepath)} (Too short: {len(df)} rows)")
                continue
            
            # Extract Meta Info
            folder_name = os.path.basename(os.path.dirname(filepath))
            filename = os.path.basename(filepath)
            
            # Extract Ticker: Market_AAPL_2025... -> AAPL
            parts = filename.split('_')
            if len(parts) >= 3:
                ticker = parts[1]
            else:
                ticker = filename.replace('.csv', '')

            # --- FEATURES ---
            sma50 = df['close'].rolling(50).mean()
            sma200 = df['close'].rolling(200).mean()
            
            df['feat_dist_sma50'] = (df['close'] / sma50) - 1
            df['feat_dist_sma200'] = (df['close'] / sma200) - 1
            df['feat_volatility'] = df['close'].pct_change().rolling(20).std() * np.sqrt(252)
            df['feat_rsi'] = calculate_rsi(df['close'])
            df['feat_mom_1m'] = df['close'].pct_change(20)
            
            # Save Features
            rel_path = os.path.relpath(filepath, RAW_DIR)
            save_path = os.path.join(FEATURES_DIR, rel_path)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df.dropna().to_csv(save_path)

            # Report Snapshot
            latest = df.iloc[-1]
            dist_200 = latest.get('feat_dist_sma200', 0)
            if pd.isna(dist_200): dist_200 = 0
            trend_state = "BULL" if dist_200 > 0 else "BEAR"
            
            scan_results.append({
                "Ticker": ticker,
                "Category": folder_name,
                "Price": round(latest['close'], 2),
                "Trend": trend_state,
                "RSI": round(latest['feat_rsi'], 2),
                "Volatility": round(latest['feat_volatility'] * 100, 2),
                "Momentum_1M": round(latest['feat_mom_1m'] * 100, 2)
            })
            count += 1
            
        except Exception as e:
            errors += 1
            print(f"   ❌ Error processing {os.path.basename(filepath)}: {e}")
            continue

    if scan_results:
        scan_df = pd.DataFrame(scan_results)
        scan_df.to_csv(SCAN_OUTPUT, index=False)
        print(f"     ✅ Market Scan Saved: {SCAN_OUTPUT}")
        print(f"     📊 Assets Processed: {count}/{len(asset_files)}")
        
        bulls = len(scan_df[scan_df['Trend']=='BULL'])
        bears = len(scan_df[scan_df['Trend']=='BEAR'])
        print(f"     🔥 Breadth: {bulls} Bulls vs {bears} Bears")
    else:
        print(f"   ⚠️  No scan results generated. (Processed: {count}, Errors: {errors})")

if __name__ == "__main__":
    print(f"🚀 AGENT: Feature Engineer [Robust Mode] - {datetime.now()}")
    process_macro()
    process_universe()