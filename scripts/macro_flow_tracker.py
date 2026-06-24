import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
TICKER_A = "XLK"  # Technology ETF
TICKER_B = "XLE"  # Energy ETF
LOOKBACK_YEARS = 2

def fetch_data(ticker, period="2y"):
    """Fetches historical data and calculates 'Dollar Volume' proxy."""
    df = yf.download(ticker, period=period, progress=False)
    
    # Flatten MultiIndex columns if present (common in new yfinance versions)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # "Dollar Volume" proxy
    df['Dollar_Vol'] = df['Close'] * df['Volume']
    return df

def calculate_obv(df):
    """Calculates On-Balance Volume (OBV) without pandas_ta."""
    # If Close > Prev Close, add Volume. If < Prev Close, subtract Volume.
    direction = np.sign(df['Close'].diff())
    # Fill NaN (first row) with 0
    direction.iloc[0] = 0
    obv = (direction * df['Volume']).cumsum()
    return obv

print(f"--- FETCHING INSTITUTIONAL FLOW DATA FOR {TICKER_A} VS {TICKER_B} ---")

# 1. Get Data
tech = fetch_data(TICKER_A)
energy = fetch_data(TICKER_B)

# 2. Build the "Relative Rotation" Ratio
ratio = tech['Close'] / energy['Close']

# 3. Calculate "Money Flow" Indicators (Using Standard Pandas)
# Moving Averages
ratio_sma_50 = ratio.rolling(window=50).mean()
ratio_sma_200 = ratio.rolling(window=200).mean()

# OBV (Using our custom function)
tech['OBV'] = calculate_obv(tech)
energy['OBV'] = calculate_obv(energy)

# --- VISUALIZATION DASHBOARD ---
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# PLOT 1: The War for Capital (Relative Strength)
ax1.plot(ratio.index, ratio, label=f'{TICKER_A} / {TICKER_B} Ratio', color='white', linewidth=1.5)
ax1.plot(ratio.index, ratio_sma_50, label='50-Day Trend (Smart Money)', color='cyan', linestyle='--')
ax1.plot(ratio.index, ratio_sma_200, label='200-Day Trend (Regime)', color='orange', linestyle='--')

# Logic for "Regime" Text
current_ratio = ratio.iloc[-1]
current_ma = ratio_sma_200.iloc[-1]

# Handle cases where data might be missing or calculating
if pd.isna(current_ma):
    status = "CALCULATING..."
    color = "white"
elif current_ratio > current_ma:
    status = f"REGIME: GROWTH ({TICKER_A} Dominating)"
    color = "cyan"
else:
    status = f"REGIME: COMMODITIES ({TICKER_B} Dominating)"
    color = "orange"

ax1.set_title(f"INSTITUTIONAL ROTATION: {status}", fontsize=14, color=color, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# PLOT 2: Hidden Accumulation (OBV Momentum)
# We normalize OBV to compare them on the same chart (Percent change from start)
# We use a small epsilon to avoid division by zero if OBV starts at 0
tech_obv_norm = (tech['OBV'] - tech['OBV'].iloc[0]) 
energy_obv_norm = (energy['OBV'] - energy['OBV'].iloc[0]) 

# Re-normalize to percentage growth relative to the max volume to keep scales similar
tech_obv_norm = tech_obv_norm / tech['Volume'].max() * 100
energy_obv_norm = energy_obv_norm / energy['Volume'].max() * 100

ax2.plot(tech.index, tech_obv_norm, label=f'{TICKER_A} Vol Flow', color='cyan')
ax2.plot(energy.index, energy_obv_norm, label=f'{TICKER_B} Vol Flow', color='orange')
ax2.set_title("VOLUME FLOW MOMENTUM (Who is being accumulated?)", fontsize=12)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# --- ALERT SYSTEM ---
print("\n--- AI ANALYSIS REPORT ---")
# Check for "Crossovers" (The Signal)
try:
    if ratio.iloc[-1] > ratio_sma_50.iloc[-1] and ratio.iloc[-20] < ratio_sma_50.iloc[-20]:
        print(f"[ALERT] {TICKER_A} (Tech) has just crossed ABOVE the 50-day trend. Money is rotating IN.")
    elif ratio.iloc[-1] < ratio_sma_50.iloc[-1] and ratio.iloc[-20] > ratio_sma_50.iloc[-20]:
        print(f"[ALERT] {TICKER_A} (Tech) has crossed BELOW the 50-day trend. Money is rotating OUT to {TICKER_B}.")
    else:
        print(f"[STATUS] Trend is established. No immediate rotation detected today.")
except IndexError:
    print("[STATUS] Not enough data to generate alerts yet.")