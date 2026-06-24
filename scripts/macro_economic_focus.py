import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
MARKET_TICKER = "^GSPC"     # S&P 500
YIELD_TICKER = "^TNX"       # 10-Year Yield (Cost of Money)
DOLLAR_TICKER = "DX-Y.NYB"  # US Dollar (Global Currency Strength)

def fetch_data(ticker, period="2y"):
    """Fetches historical closing data."""
    try:
        df = yf.download(ticker, period=period, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df['Close']
    except Exception as e:
        print(f"[ERROR] Could not fetch {ticker}: {e}")
        return pd.Series()

print("--- ANALYZING CURRENT MARKET FOCUS ---")

# 1. Get Data
market = fetch_data(MARKET_TICKER)
yields = fetch_data(YIELD_TICKER)
dxy = fetch_data(DOLLAR_TICKER)

# 2. Align Data
df = pd.concat([market, yields, dxy], axis=1).dropna()
df.columns = ['Market', 'Yields', 'Dollar']

# 3. Calculate Trends (Simple Moving Average Check)
# True if current price is higher than 50-day average (Trending Up)
yield_rising = df['Yields'].iloc[-1] > df['Yields'].rolling(50).mean().iloc[-1]
dxy_rising = df['Dollar'].iloc[-1] > df['Dollar'].rolling(50).mean().iloc[-1]

# --- VISUALIZATION DASHBOARD ---
plt.style.use('dark_background')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# PLOT 1: The Market
ax1.plot(df.index, df['Market'], color='white')
ax1.set_title("THE MARKET (S&P 500)", fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.2)

# PLOT 2: Interest Rates (The Brake Pedal)
color_y = 'red' if yield_rising else 'lime'
ax2.plot(df.index, df['Yields'], color=color_y)
ax2.set_title("INTEREST RATES (Cost of Money)", fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.2)

# PLOT 3: The Dollar (The Wrecking Ball)
color_d = 'red' if dxy_rising else 'lime'
ax3.plot(df.index, df['Dollar'], color=color_d)
ax3.set_title("US DOLLAR STRENGTH", fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# --- THE "MARKET FOCUS" REPORT ---
print("\n--- MARKET FOCUS REPORT ---")

if yield_rising and dxy_rising:
    print("[STATUS] TIGHTENING (Rates UP + Dollar UP)")
    print(">>> FOCUS: DEFENSE & CASH")
    print(">>> Avoid: High-Risk Tech, Crypto.")
    print(">>> Look at: Short-term Treasuries, Dollar Cash.")

elif not yield_rising and not dxy_rising:
    print("[STATUS] EASING (Rates DOWN + Dollar DOWN)")
    print(">>> FOCUS: AGGRESSIVE GROWTH")
    print(">>> Buy: Tech, Crypto, Small Caps.")
    print(">>> The wind is at your back.")

elif yield_rising and not dxy_rising:
    print("[STATUS] INFLATIONARY (Rates UP + Dollar DOWN)")
    print(">>> FOCUS: COMMODITIES")
    print(">>> Buy: Oil, Gold, Metals, Energy Stocks.")
    print(">>> Money is rotating into 'Hard Assets'.")

else:
    print("[STATUS] MIXED / CHOPPY")
    print(">>> FOCUS: STOCK PICKING")
    print(">>> No clear macro wave. Stick to high-quality companies.")