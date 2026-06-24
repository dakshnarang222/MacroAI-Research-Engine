import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score
import joblib
import os
from datetime import datetime
import glob

# --- CONFIGURATION (PATH FIX) ---
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_CLEAN = os.path.join(PROJECT_ROOT, "data", "cleaned")
DATA_RAW = os.path.join(PROJECT_ROOT, "data", "raw")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)

# TARGET CONFIGURATION
TARGET_ASSETS = {
    "SPY": "Indices_Major/SPY_latest.csv",       
    "BTC": "Crypto_Top100/BTCUSD_latest.csv"     
}
PREDICTION_HORIZON = 5 # Predict 5 days into the future

def load_data(asset_subpath):
    """Loads Asset data and merges with Macro features"""
    
    # 1. Load Macro Features
    macro_path = os.path.join(DATA_CLEAN, "features_macro.csv")
    if not os.path.exists(macro_path):
        print("❌ Macro features missing. Run Agent #2 first.")
        return None
    macro_df = pd.read_csv(macro_path, index_col=0, parse_dates=True)
    
    # 2. Load Asset Price
    asset_path = os.path.join(DATA_RAW, asset_subpath)
    
    # Fallback Search
    if not os.path.exists(asset_path):
        print(f"⚠️ Path not found: {asset_subpath}. Searching...")
        filename = os.path.basename(asset_subpath)
        found_files = glob.glob(os.path.join(DATA_RAW, "**", filename), recursive=True)
        if found_files:
            asset_path = found_files[0]
            print(f"   Found at: {asset_path}")
        else:
            print(f"❌ Asset file definitely missing: {filename}")
            return None
        
    price_df = pd.read_csv(asset_path)
    price_df.columns = [c.lower() for c in price_df.columns]
    
    # Fix Date
    date_col = 'date' if 'date' in price_df.columns else price_df.columns[0]
    price_df[date_col] = pd.to_datetime(price_df[date_col])
    price_df.set_index(date_col, inplace=True)
    
    # Find Close Price
    target_col = 'close' if 'close' in price_df.columns else 'adj close'
    if target_col not in price_df.columns: 
        if 'value' in price_df.columns: target_col = 'value'
        else: return None
        
    price_df = price_df[[target_col]].rename(columns={target_col: 'price'})
    
    # 3. Merge
    df = price_df.join(macro_df, how='inner').sort_index()
    return df

def create_features(df):
    """Creates ML-ready features"""
    data = df.copy()
    
    # Returns
    data['ret_1d'] = data['price'].pct_change()
    data['ret_5d'] = data['price'].pct_change(5)
    data['vol_20d'] = data['ret_1d'].rolling(20).std()
    
    # Macro Lags
    cols_to_lag = ['real_rate', 'liquidity_trend', 'inflation_rate', 'vix']
    for col in cols_to_lag:
        if col in data.columns:
            data[f'{col}_lag1'] = data[col].shift(1)
            data[f'{col}_lag5'] = data[col].shift(5)
            
    # Technical Lags
    data['price_lag1'] = data['price'].shift(1)
    
    # TARGET
    future_return = data['price'].shift(-PREDICTION_HORIZON) / data['price'] - 1
    data['target'] = (future_return > 0).astype(int)
    
    data = data.dropna()
    return data

def train_model(ticker, subpath):
    print(f"\nTraining AI Model for {ticker}...")
    
    raw_df = load_data(subpath)
    if raw_df is None: return
    
    df = create_features(raw_df)
    
    # Features (X) and Target (y)
    drop_cols = ['price', 'target']
    features = [c for c in df.columns if c not in drop_cols]
    
    X = df[features]
    y = df['target']
    
    # Train/Test Split
    split_point = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_point], X.iloc[split_point:]
    y_train, y_test = y.iloc[:split_point], y.iloc[split_point:]
    
    # Train XGBoost
    model = xgb.XGBClassifier(
        n_estimators=100, learning_rate=0.05, max_depth=4,
        objective='binary:logistic', random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, zero_division=0)
    
    print(f"   ✔ Model Trained.")
    print(f"   Accuracy: {acc:.2%}")
    print(f"   Precision: {prec:.2%}")
    
    # Save Model
    model_path = os.path.join(MODELS_DIR, f"xgb_{ticker}.pkl")
    joblib.dump(model, model_path)
    
    # Predict Future
    last_row = X.iloc[[-1]] 
    future_prob = model.predict_proba(last_row)[0][1]
    direction = "BULLISH" if future_prob > 0.5 else "BEARISH"
    
    print(f"   5-Day Forecast: {direction} ({future_prob:.1%} Probability)")
    
    return {
        "Asset": ticker,
        "Forecast": direction,
        "Probability": f"{future_prob:.1%}",
        "Accuracy": f"{acc:.1%}"
    }

if __name__ == "__main__":
    print(f"AGENT: Model Trainer Initiated [{datetime.now().strftime('%Y%m%d')}]")
    results = []
    for ticker, path in TARGET_ASSETS.items():
        res = train_model(ticker, path)
        if res: results.append(res)
        
    if results:
        pred_df = pd.DataFrame(results)
        save_path = os.path.join(OUTPUT_DIR, "ai_predictions.csv")
        pred_df.to_csv(save_path, index=False)
        print(f"\n✔ AI Predictions Saved: {save_path}")