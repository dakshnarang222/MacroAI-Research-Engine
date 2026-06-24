import os
import pandas as pd
import re

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, "../data/raw")
OUTPUT_FILE = os.path.join(BASE_DIR, "../data/universe.csv")

# --- MANUAL SURGERY: FIX SPECIFIC FAILURES ---
FIX_MAP = {
    # Commodities (The source of your GC error)
    "GC": "GC=F", "GOLD": "GC=F",
    "CL": "CL=F", "CRUDE": "CL=F",
    "SI": "SI=F", "SILVER": "SI=F",
    "NG": "NG=F", "HG": "HG=F", 
    "RB": "RB=F", "HO": "HO=F", "BZ": "BZ=F",
    "LBS": "LBS=F", "ZNC": "ZNC=F", "LIT": "LIT", # LIT is an ETF
    
    # Dirty Filenames -> Clean Tickers
    "BTCUSD_PRICE": "BTC-USD",
    "ETHUSD_PRICE": "ETH-USD",
    "GC_PRICE": "GC=F",
    "CL_PRICE": "CL=F",
    
    # Crypto Corrections
    "BSCUSD-USD": "BNB-USD",
    "USDTB-USD": "USDT-USD",
    "PY-USD": "PYUSD-USD", 
    "RL-USD": "RLUSD-USD",
    
    # Indices / Forex
    "GSPC": "^GSPC", "IXIC": "^IXIC", "DJI": "^DJI", "RUT": "^RUT", 
    "VIX": "^VIX", "MXX": "^MXX", "N225": "^N225", "HSI": "^HSI", 
    "FTSE": "^FTSE", "GDAXI": "^GDAXI", "FCHI": "^FCHI", "BVSP": "^BVSP",
    "EURUSD": "EURUSD=X", "JPY": "JPY=X", "DXY": "DX-Y.NYB"
}

# --- BLACKLIST: IGNORE THESE (PERMANENTLY BROKEN) ---
BLACKLIST = [
    "FIGR_HELOC-USD", "USYC-USD", "SUSDS-USD", 
    "ASTER-USD", "CBBTC-USD", "BUIDL-USD"
]

def extract_clean_ticker(filename, category):
    """Cleans filenames and applies Asset Class rules."""
    
    # 1. Basic Clean
    name = os.path.splitext(filename)[0].upper()
    name = name.replace("MARKET_", "").replace("MACRO_", "")
    name = re.sub(r'_LATEST$', '', name)
    name = re.sub(r'_PRICE$', '', name)
    name = re.sub(r'_\d{8}$', '', name)
    
    # 2. BLACKLIST CHECK
    if name in BLACKLIST:
        return None

    # 3. COMMODITIES LOGIC 
    if category.upper().startswith("COM_"): 
        known_etfs = ["LIT", "URA", "REMX", "COPX", "PICK", "GUNR", "BDRY"]
        if len(name) <= 3 and "=" not in name:
            if name not in known_etfs:
                name = f"{name}=F"

    # 4. CRYPTO LOGIC
    if "CRYPTO" in category.upper():
        if name.endswith("USD") and "-" not in name:
            name = name[:-3] + "-USD"
        if "USD-USD" in name:
            name = name.replace("USD-USD", "-USD")

    # 5. FINAL OVERRIDE (Apply Fix Map Last - This fixes GC)
    if name in FIX_MAP:
        return FIX_MAP[name]
        
    return name

def scan_and_generate_map():
    print(f"🕵️  Deep Scanning & Repairing Tickers...")
    
    universe_list = []
    seen = set()

    for root, dirs, files in os.walk(RAW_DATA_DIR):
        category = os.path.relpath(root, RAW_DATA_DIR)
        
        if category == "." or category.startswith(".") or "Macro" in category:
            continue
            
        for file in files:
            if file.endswith(".csv") or file.endswith(".parquet"):
                if file.startswith("."): continue
                
                ticker = extract_clean_ticker(file, category)
                
                if ticker and len(ticker) < 20 and ticker not in seen:
                    universe_list.append({"Ticker": ticker, "Category": category})
                    seen.add(ticker)

    if universe_list:
        df = pd.DataFrame(universe_list)
        df = df.sort_values(by=["Category", "Ticker"])
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Universe Repaired!")
        print(f"   Saved {len(df)} unique assets.")
        
        # Verify GC Fix
        gc = df[df['Ticker'].str.contains("GC=")]
        print(f"   Check Gold: {gc['Ticker'].values if not gc.empty else 'Missing'}")
    else:
        print("⚠️ No assets found.")

if __name__ == "__main__":
    scan_and_generate_map()