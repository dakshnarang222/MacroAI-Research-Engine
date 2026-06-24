import pandas as pd
import matplotlib.pyplot as plt
import os

# Reuse logic from your signal engine
from signal_engine import load_and_prep_data

def plot_history():
    print("...Generating Historical Test Chart...")
    
    # Load all the data
    df = load_and_prep_data()
    
    # Setup the Plot (3 Rows)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    plt.subplots_adjust(hspace=0.3)
    
    # --- CHART 1: REAL RATES (The Driver) ---
    # Formula: 10Y Yield - Inflation
    real_rates = df['yield_10y'] - df['inflation_rate']
    
    # Plot the line
    ax1.plot(df.index, real_rates, color='blue', linewidth=2, label='Real Rates (Yield - CPI)')
    
    # Color the background (Red = Restrictive, Green = Stimulative)
    ax1.axhline(0, color='black', linewidth=1)
    ax1.fill_between(df.index, real_rates, 0, where=(real_rates < 0), color='green', alpha=0.1, label='Stimulative (Neg Rates)')
    ax1.fill_between(df.index, real_rates, 0, where=(real_rates > 1.5), color='red', alpha=0.1, label='Restrictive (>1.5%)')
    
    ax1.set_title("1. Real Rates (Cost of Money)", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Percent (%)")
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # --- CHART 2: LIQUIDITY (The Fuel) ---
    # 4-Week Change in Fed Assets
    liq_change = df['liquidity'].diff(4)
    
    # Bar chart for liquidity changes
    colors = ['green' if x > 0 else 'red' for x in liq_change]
    ax2.bar(df.index, liq_change, color=colors, width=5)
    
    ax2.set_title("2. Fed Liquidity Momentum (4-Week Change)", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Millions (USD)")
    ax2.grid(True, alpha=0.3)

    # --- CHART 3: YIELD CURVE (The Alarm) ---
    # 10Y - 3M Spread
    ax3.plot(df.index, df['spread'], color='black', linewidth=1.5)
    
    # Fill Red when Inverted
    ax3.fill_between(df.index, df['spread'], 0, where=(df['spread'] < 0), color='red', alpha=0.3, label='RECESSION SIGNAL (Inverted)')
    ax3.axhline(0, color='red', linestyle='--')
    
    ax3.set_title("3. Yield Curve (Recession Signal)", fontsize=12, fontweight='bold')
    ax3.set_ylabel("Spread (%)")
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)

    print("✅ Chart Generated. Check your screen.")
    plt.show()

if __name__ == "__main__":
    plot_history()