import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
CRYPTO_TICKER = "BTC-USD"   # The Asset in question
TECH_TICKER = "QQQ"         # Proxy for Risk/Growth
GOLD_TICKER = "GLD"         # Proxy for Safety/Inflation
DOLLAR_TICKER = "DX-Y.NYB"  # Proxy for Liquidity Stress

def fetch_data(ticker, period="1y"):
    """Fetches historical closing data."""
    try:
        df = yf.download(ticker, period=period, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df['Close']
    except Exception as e:
        print(f"[ERROR] Could not fetch {ticker}: {e}")
        return pd.Series()

print(f"--- ANALYZING {CRYPTO_TICKER} CORRELATIONS ---")

# 1. Get Data
btc = fetch_data(CRYPTO_TICKER)
tech = fetch_data(TECH_TICKER)
gold = fetch_data(GOLD_TICKER)
dxy = fetch_data(DOLLAR_TICKER)

# 2. Align Data
df = pd.concat([btc, tech, gold, dxy], axis=1).dropna()
df.columns = ['BTC', 'Tech', 'Gold', 'Dollar']

# 3. Calculate Rolling Correlations (60-Day Window)
# +1.0 = Moving perfectly together
# -1.0 = Moving perfectly opposite
corr_tech = df['BTC'].rolling(60).corr(df['Tech'])
corr_gold = df['BTC'].rolling(60).corr(df['Gold'])
corr_dxy = df['BTC'].rolling(60).corr(df['Dollar'])

# --- VISUALIZATION DASHBOARD ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the lines
ax.plot(corr_tech.index, corr_tech, label='Correlation to TECH (Risk-On)', color='cyan', linewidth=2)
ax.plot(corr_gold.index, corr_gold, label='Correlation to GOLD (Inflation Hedge)', color='gold', linewidth=2)
ax.plot(corr_dxy.index, corr_dxy, label='Correlation to DOLLAR (Liquidity)', color='red', linestyle='--', alpha=0.7)

# Add a "Zero Line" (No Correlation)
ax.axhline(0, color='white', linestyle=':', alpha=0.5)

ax.set_title(f"WHO IS BITCOIN FOLLOWING? (60-Day Correlation)", fontsize=14, fontweight='bold')
ax.set_ylabel("Correlation Coefficient (-1 to +1)")
ax.legend(loc='lower left')
ax.grid(True, alpha=0.2)

# Interpret Current State on Chart
current_tech_corr = corr_tech.iloc[-1]
current_gold_corr = corr_gold.iloc[-1]

if current_tech_corr > 0.5:
    status = "IDENTITY: TECH STOCK (High Risk Beta)"
elif current_gold_corr > 0.5:
    status = "IDENTITY: DIGITAL GOLD (Safe Haven)"
else:
    status = "IDENTITY: DECOUPLED (Idiosyncratic Move)"

ax.text(df.index[0], 0.8, status, color='white', fontsize=12, fontweight='bold', bbox=dict(facecolor='black', alpha=0.5))

plt.tight_layout()
plt.show()

# --- TEXT REPORT ---
print("\n--- CRYPTO CORRELATION REPORT ---")
print(f"Current Correlation to TECH: {current_tech_corr:.2f}")
print(f"Current Correlation to GOLD: {current_gold_corr:.2f}")

if current_tech_corr > current_gold_corr and current_tech_corr > 0.5:
    print("[RESULT] Bitcoin is trading like a TECH STOCK.")
    print(">>> Strategy: Trade it with Nasdaq logic. If Tech dumps, BTC dumps.")
elif current_gold_corr > current_tech_corr and current_gold_corr > 0.5:
    print("[RESULT] Bitcoin is trading like DIGITAL GOLD.")
    print(">>> Strategy: It is acting as a hedge against the Dollar/Inflation.")
elif current_tech_corr < 0.2 and current_gold_corr < 0.2:
    print("[RESULT] Bitcoin is DECOUPLED.")
    print(">>> Strategy: It is moving on its own news/flows. Ignore the stock market.")
else:
    print("[RESULT] Mixed Signals. No clear narrative driver.")