import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCAN_FILE = os.path.join(BASE_DIR, "../data/market_scan.csv")
MACRO_FILE = os.path.join(BASE_DIR, "../data/features_macro.csv")

def load_data():
    if not os.path.exists(SCAN_FILE) or not os.path.exists(MACRO_FILE):
        print("Error: Input files missing. Run 'agent_feature_engineer.py' first.")
        return None, None
    try:
        scan = pd.read_csv(SCAN_FILE)
        macro = pd.read_csv(MACRO_FILE, index_col=0)
        return scan, macro
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def analyze_macro_regime(macro):
    """Determines the Macro Economic Regime."""
    if macro.empty: return "NEUTRAL", "NEUTRAL", "NEUTRAL"

    latest = macro.iloc[-1]
    
    # 1. Liquidity (Fed Balance Sheet 1-Month Trend)
    liq = latest.get('liquidity_trend', 0)
    liq_trend = "EXPANDING" if liq > 0 else "CONTRACTING"
    
    # 2. Real Rates (10Y Yield - Inflation)
    real_r = latest.get('real_rate', 0)
    rate_regime = "RESTRICTIVE" if real_r > 1.0 else "ACCOMMODATIVE"
    
    # 3. Yield Curve (10Y - 3M Spread)
    curve_val = latest.get('yield_curve', 0)
    curve = "INVERTED (Recession Risk)" if curve_val < 0 else "NORMAL (Growth)"
    
    return liq_trend, rate_regime, curve

def print_table(df, title):
    """Helper to print a clean ASCII table."""
    print(f"\n{title}")
    print("-" * 65)
    print(f"{'TICKER':<10} {'SECTOR':<25} {'PRICE':<10} {'1M CHG':<10} {'RSI':<5}")
    print("-" * 65)
    
    if df.empty:
        print("No assets met criteria.")
        return

    for _, row in df.iterrows():
        # Clean up sector name (remove 'Sector_' prefix for cleaner look)
        sector = str(row['Category']).replace('Sector_', '').replace('Com_', '')[:24]
        price = f"${row['Price']:.2f}"
        mom = f"{row['Momentum_1M']:.1f}%"
        rsi = f"{row['RSI']:.0f}"
        
        print(f"{row['Ticker']:<10} {sector:<25} {price:<10} {mom:<10} {rsi:<5}")
    print("-" * 65)

def generate_signals(scan, liq_trend, rate_regime):
    """
    Generates the Executive Summary.
    """
    # Header
    print("\n" + "="*65)
    print(f"MACRO QUANTITATIVE REPORT | {datetime.now().strftime('%Y-%m-%d')}")
    print("="*65)
    
    # 1. Macro Snapshot
    print(f"MACRO ENVIRONMENT:")
    print(f"Liquidity:   {liq_trend}")
    print(f"Real Rates:  {rate_regime}")
    print(f"Yield Curve: {rate_regime}")
    print("-" * 65)
    
    # 2. Strategy Logic
    strategy_name = "NEUTRAL / WAIT"
    rationale = "Signals are mixed. Verify trends before execution."
    target_sectors = []

    if liq_trend == "EXPANDING" and rate_regime == "ACCOMMODATIVE":
        strategy_name = "RISK-ON (Growth)"
        rationale = "Liquidity expansion supports high-beta assets."
        target_sectors = ["Tech", "Crypto", "Discretionary"]
        
        candidates = scan[
            (scan['Category'].str.contains('Tech|Crypto|Discret', case=False, na=False)) & 
            (scan['RSI'] < 70) & 
            (scan['Trend'] == 'BULL')
        ].sort_values('Momentum_1M', ascending=False).head(5)

    elif rate_regime == "RESTRICTIVE" or liq_trend == "CONTRACTING":
        strategy_name = "DEFENSIVE (Inflation/Value)"
        rationale = "Tightening financial conditions favor hard assets."
        target_sectors = ["Energy", "Metals", "Agriculture", "Utilities"]
        
        candidates = scan[
            (scan['Category'].str.contains('Energy|Metals|Agri|Util', case=False, na=False)) & 
            (scan['Trend'] == 'BULL')
        ].sort_values('Momentum_1M', ascending=False).head(5)
    
    else:
        candidates = pd.DataFrame() # Empty if neutral

    print(f"STRATEGY:    {strategy_name}")
    print(f"RATIONALE:   {rationale}")
    
    # 3. Top Picks Table
    if not candidates.empty:
        print_table(candidates, f"TOP PICKS ({', '.join(target_sectors)})")

    # 4. Momentum Breakouts (Independent of Macro)
    breakouts = scan[
        (scan['Momentum_1M'] > 15) &  # Strong move
        (scan['RSI'] < 80)            # Not fully exhausted
    ].sort_values('Momentum_1M', ascending=False).head(5)
    
    print_table(breakouts, "MOMENTUM BREAKOUTS (High Relative Strength)")
    print("\n")

if __name__ == "__main__":
    scan_df, macro_df = load_data()
    if scan_df is not None and macro_df is not None:
        liq, rate, curve = analyze_macro_regime(macro_df)
        generate_signals(scan_df, liq, rate)