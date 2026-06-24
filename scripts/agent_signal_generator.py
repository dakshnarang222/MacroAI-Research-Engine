import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- CONFIGURATION (PATH FIX) ---
import os
# Get absolute path of THIS script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up to Project Root
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Define absolute paths
CLEAN_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
TODAY_STR = datetime.now().strftime("%Y%m%d")

def generate_signals():
    print(f"🚀 AGENT: Signal Generator Tier 2 Initiated [{TODAY_STR}]...")
    
    # 1. LOAD FEATURES
    feature_path = os.path.join(CLEAN_DIR, "features_master.csv")
    if not os.path.exists(feature_path):
        print("❌ Features missing. Run Agent #2 first.")
        return

    df = pd.read_csv(feature_path, index_col=0, parse_dates=True)
    latest = df.iloc[-1]
    
    print(f"   Analyzing Data from: {latest.name}")
    
    signals = []

    # ==========================================
    # 2. LOGIC ENGINE (Dalio + Simons Hybrid)
    # ==========================================

    # --- A. MACRO REGIME (The Climate) ---
    # Rule: If Yield Curve Inverted AND Credit Spreads Rising = RECESSION DANGER
    recession_risk = False
    if latest['yield_curve_inverted'] == 1 and latest['credit_spread'] > latest['credit_stress_trend']:
        recession_risk = True
        macro_comment = "RECESSION WATCH: Inverted Curve + Rising Credit Stress."
    elif latest['liquidity_change_4w'] < 0:
        macro_comment = "HEADWIND: Fed draining liquidity (-)."
    else:
        macro_comment = "SUPPORTIVE: Liquidity expanding or neutral."

    # --- B. RISK APPETITE (The Mood) ---
    # Rule: Are investors chasing Tech (Risk On) or hiding in Utilities (Risk Off)?
    if latest['risk_ratio'] > latest['risk_ratio_trend']:
        risk_mode = "RISK ON"
    else:
        risk_mode = "RISK OFF"

    # ==========================================
    # 3. ASSET CONVICTION (The Specifics)
    # ==========================================
    
    # --- S&P 500 (SPY) ---
    # Logic: Buy if Risk On AND no Recession Risk
    spy_score = 0
    if risk_mode == "RISK ON": spy_score += 1
    if not recession_risk: spy_score += 1
    if latest['real_rate'] < 1.0: spy_score += 1 # Low rates help stocks
    
    if spy_score >= 2: spy_signal = "BUY"
    elif spy_score == 1: spy_signal = "NEUTRAL"
    else: spy_signal = "SELL"
    
    signals.append({
        "Asset": "S&P 500",
        "Price": latest['price_spy'],
        "Signal": spy_signal,
        "Conviction": f"{spy_score}/3",
        "Driver": f"Mode: {risk_mode}. {macro_comment}"
    })

    # --- BITCOIN (BTC) ---
    # Logic: Pure Liquidity Proxy. Needs Risk On + Expanding Liquidity.
    btc_score = 0
    if risk_mode == "RISK ON": btc_score += 1
    if latest['liquidity_change_4w'] > 0: btc_score += 2 # Highly sensitive to liquidity
    
    if btc_score >= 2: btc_signal = "BUY"
    elif btc_score == 1: btc_signal = "NEUTRAL"
    else: btc_signal = "SELL"
    
    signals.append({
        "Asset": "Bitcoin",
        "Price": latest['price_btc'],
        "Signal": btc_signal,
        "Conviction": f"{btc_score}/3",
        "Driver": f"Sensitive to Liquidity ({latest['liquidity_change_4w']:,.0f}M). Trend: {risk_mode}"
    })

    # --- GOLD (GC) ---
    # Logic: Hedge. Buy if Real Rates are falling or Recession Risk is high.
    gold_score = 0
    if recession_risk: gold_score += 2
    if latest['real_rate'] < 0.5: gold_score += 1
    
    if gold_score >= 2: gold_signal = "BUY"
    elif gold_score == 1: gold_signal = "NEUTRAL"
    else: gold_signal = "SELL"

    signals.append({
        "Asset": "Gold",
        "Price": latest['price_gold'],
        "Signal": gold_signal,
        "Conviction": f"{gold_score}/3",
        "Driver": f"Real Rates: {latest['real_rate']:.2f}%. Safe Haven demand: {'High' if recession_risk else 'Low'}."
    })

    # ==========================================
    # 4. SAVE OUTPUTS
    # ==========================================
    final_df = pd.DataFrame(signals)
    
    # Save dated version (History)
    save_path = os.path.join(OUTPUT_DIR, f"signals_{TODAY_STR}.csv")
    final_df.to_csv(save_path, index=False)
    
    # Save latest version (For Report Agent)
    latest_path = os.path.join(OUTPUT_DIR, "signals_latest.csv")
    final_df.to_csv(latest_path, index=False)
    
    print("\n📊 TIER 2 TRADE SHEET:")
    print(final_df.to_string(index=False))
    print(f"\n✅ Signals Saved: {save_path}")

if __name__ == "__main__":
    generate_signals()