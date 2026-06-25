# MacroAI Research Engine 

An automated, Python-based system designed to ingest macroeconomic data, forecast market trends, and generate probability-driven investment signals. 

This engine focuses on tracking major global money flows and macro indicators to output sized trade ideas with strict risk controls. It runs entirely locally on macOS, prioritizing data accuracy and deterministic execution.

## Core Architecture

The system operates as a continuous, automated pipeline divided into four primary stages:

1. **Data Ingestion (Observation):** Automated collection and storage of market prices, Treasury yields, and macro series (CPI, S&P 500, DXY) into optimized Parquet files.
2. **Feature Engineering (Interpretation):** Processing raw data into quantitative variables (e.g., yield curve slopes, credit spread changes, VIX gaps).
3. **Modeling Engine (Prediction):** An ensemble approach that calculates a final "Conviction Score" (0-100%) to predict asset direction across short, medium, and long-term horizons.
4. **Action & Risk (Execution):** Generates daily PDF reports and Telegram alerts for high-conviction trades, strictly gated by a Human-in-the-Loop (HITL) execution policy.

## The Modeling Ensemble

To ensure robust forecasts and avoid relying on a single methodology, the engine combines three modeling approaches:

* **Rule-Based Logic:** Hardcoded economic principles (e.g., if the 10y-2y yield curve inverts and credit spreads widen, increase recession probability).
* **Econometrics & Statistics:** Time-series analysis (Vector Autoregression, Granger Causality) to quantify the lead-lag effects between economic variables.
* **Machine Learning:** Gradient Boosted Trees (XGBoost) trained on structured data with strict walk-forward cross-validation to prevent look-ahead bias.

## Data Sources & Accuracy

The pipeline prioritizes data accuracy and high availability, starting with foundational market data:
* **Market Prices:** S&P 500, NASDAQ, Russell, WTI Crude, Gold, Copper, BTC, ETH.
* **Fixed Income:** US Treasury yields (1m to 30y) via FRED.
* **Core Macro:** CPI, Unemployment, Retail Sales, PMI.
* **Alternative Data (Planned):** News sentiment scraping, credit spreads, and shipping indices.

## Local Execution & Automation

The system is fully automated using macOS `launchd` to schedule deterministic Python scripts daily at 6:00 AM. 

**Daily Runbook:**
1. `agent_nightly_ingest.py` - Fetches and validates new data.
2. `agent_feature_engineer.py` - Calculates new features and updates the normalized feature store.
3. `agent_signal_generator.py` - Runs the ensemble models to generate conviction scores.
4. `agent_news_scraper.py` - Updates localized sentiment scores.
5. `agent_report_generator.py` & `agent_telegram_alert.py` - Compiles the daily summary and pushes alerts if a trade hits the >75% conviction threshold.

## Risk Management

* **Position Sizing:** Dictated by Volatility Parity and a Kelly Criterion fraction to dynamically scale exposure.
* **Kill-Switch:** A single command-line script immediately halts all `launchd` jobs and system operations.
* **Validation:** Continuous performance benchmarking against a passive S&P 500 Buy-and-Hold strategy to verify true predictive edge.

## Project Roadmap

* **Phase 1 (MVP):** Build data pipeline, compute basic features (yield curve, S&P returns), and backtest 5-10 initial macro rules.
* **Phase 2:** Integrate news sentiment scraping, train basic XGBoost models, and launch Streamlit dashboard/Telegram alerts.
* **Phase 3:** Integrate Regime Detection (Hidden Markov Models) and connect to broker APIs (Alpaca/Interactive Brokers) for semi-automated execution.
