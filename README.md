Macro Ai Research Engine 
AI-Powered System for Forecasting Macro Trends and Generating Investment Signals
Version: 1.1 Date: November 30, 2025 
Prepared for: Daksh Narang Prepared by: AI Assistant (ChatGPT, Gemini, and DeepSeek)

Table of Contents
	•	Executive Summary
	•	1.1. Core System Goal
	•	1.2. Top-3 Immediate Actions
	•	System Architecture and Components
	•	2.1. High-Level Architecture (Six Layers)
	•	2.2. Definitions and Simple Explanations (Glossary)
	•	Core Global Forces to Track
	•	3.1. The Five Global Forces
	•	3.2. Decomposing Forces into Measurable Signals
	•	Data and Inputs
	•	4.1. Tier 1: Must-Have Data (The Foundation)
	•	4.2. Tier 2: High-Value Data (Next-Level Edge)
	•	4.3. Tier 3: Advanced/Alternative Data (Proprietary Edge)
	•	4.4. Data Governance and Licensing
	•	Modeling Approach
	•	5.1. Paradigm 1: Theory-Derived Rule Engine
	•	5.2. Paradigm 2: Statistical Models and Econometrics
	•	5.3. Paradigm 3: Machine Learning Ensemble
	•	5.4. The Meta-Model: Bayesian Combination and Conviction Score
	•	Risk Management and Safe Practices
	•	6.1. Position Sizing and Portfolio Logic
	•	6.2. System Kill-Switches and Emergency Procedures
	•	6.3. Model Governance and Auditability
	•	Evaluation Metrics and Monitoring
	•	7.1. Predictive Metrics (Signal-Level)
	•	7.2. Portfolio Metrics (Strategy-Level)
	•	7.3. Operational Monitoring
	•	Detailed Project Roadmap (Milestones and Tasks)
	•	8.1. Week 1 — Data Pipeline and Simple Signals (MVP)
	•	8.2. Week 2 — ML, News, and Dashboard (MVP Complete)
	•	8.3. Milestone 7 to 9: Scale and Automation
	•	Future Improvements & Advanced Ideas
	•	Local Execution Plan and Runbook
	•	10.1. macOS launchd Configuration
	•	10.2. Local Execution Architecture
	•	10.3. Daily Operations Runbook

1. Executive Summary - 1.1. Core System Goal

This document outlines the blueprint for a sophisticated Macro Prediction Intelligence Engine. The goal is to build a private, automated system that continuously ingests cross-asset and alternative data, translates major global forces (money flows, technology, resources, geopolitics, and culture) into probabilistic investment signals across three horizons (short-term: days–weeks; medium-term: 1–12 months; long-term: 1–5 years), and outputs sized trade ideas with robust risk controls for personal execution.

The system is designed to provide a strategic advantage by focusing on large, repeatable money flows rather than modeling every market variable, creating a concise, adaptive "macro brain."

1.2. Top-3 Immediate Actions
	•	Establish Environment: Set up the project repository (Git) and install the core Python data science stack (pandas, numpy, etc.).
	•	Implement Tier 1 Data Pipeline: Use macOS launchd scheduler for daily 6:00 AM automated execution of Python scripts for data ingestion of core market prices and macroeconomic series (e.g., S&P 500, US yields, CPI).
	•	Build Week 1 Notebook: Create the first analytical notebook to compute starter features (e.g., yield curve slope) and implement the initial 5–10 rule-based backtests for historical performance comparison.

2. System Architecture and Components

The system is structured as a resilient pipeline, dividing responsibilities across six distinct, interconnected layers.

2.1. High-Level Architecture (Six Layers)
Layer
Responsibility
Simple Explanation
1. Data Layer (Observation)
Collection, storage, and standardization of all raw market, macro, and alternative data.
The engine's eyes and ears; gathers and stores the raw fuel.
2. Feature/Signal Layer (Interpretation)
Transformation of raw data into quantitative, predictive variables (features) and interpretable indicators (signals).
Translates raw data into actionable concepts like 'rising demand' or 'recession risk.'
3. Modeling Layer
Runs the core algorithms (Rule-Based, Statistical, and Machine Learning) to produce probability estimates and directional forecasts.
The brain; uses different methods to predict the market's likely direction.
4. Backtest & Risk Layer
Historical simulation of model performance, calculation of optimal position sizes, and implementation of safety controls.
The conscience and quality control; ensures the model works and limits potential losses.
5. Action Layer
Generates final trade alerts, ranks ideas by conviction, and connects (optionally) to brokers for automated or semi-automated execution.
The hands; turns forecasts into immediate, actionable instructions.
6. Ops & Automation
Scheduled orchestration of all tasks. Python scripts run locally on your Mac via launchd scheduler. The process will stop if the Mac is shut down. The system uses deterministic Python scripts without AI orchestration for maximum safety. The core pipeline runs daily at 6:00 AM.
The automated workforce; keeps the system running, healthy, and up-to-date.

2.2. Definitions and Simple Explanations (Glossary)
Term
Simple Explanation
Global Forces
Large-scale, long-lasting trends that shape economies and markets over months to years (e.g., geopolitical shifts, technology adoption).
Feature
A single processed data point or engineered variable used as an input to the models (e.g., the slope of the yield curve).
Signal
A computed indicator suggesting a likely direction for an asset, combining several features into an interpretable measure (e.g., 'dollar weakening').
Conviction Score
A final, probability-like score (e.g., 0 to 100%) expressing how strongly the entire system believes in a specific prediction.
Regime
A distinct market state (e.g., 'risk-on' or 'bear market') where the relationships between variables fundamentally change.
Backtesting
The process of testing an investment strategy on historical data to simulate how it would have performed in the past.
Ensemble
The technique of combining predictions from multiple different models (e.g., rule-based, statistical, and ML) to create a more robust final forecast.
launchd
The built-in macOS service management framework used to schedule and run Python scripts at specified times (e.g., daily at 6:00 AM). It runs locally on your computer, meaning the process will stop if the machine is shut down.
Workers
Deterministic Python scripts that perform specific tasks (data ingestion, feature engineering, signal generation). These scripts cannot 'hallucinate' as they execute fixed code logic.
MVP
Minimum Viable Product. The smallest, most essential version of the system that can run end-to-end (targeted for a two-week build).
DXY
Dollar Index. A measure of the value of the US Dollar relative to a basket of foreign currencies.
Parquet
A columnar storage file format, optimized for storing large amounts of time-series data efficiently.
FAISS
A library for efficient similarity search and clustering of dense vectors, planned for local news embeddings.

3. Core Global Forces to Track

The engine is built around forecasting where capital is likely to flow by tracking the most impactful, repeatable global forces.

3.1. The Five Global Forces

The engine will initially focus on five primary forces, expanding the list over time:
	•	Evolution of Technology: Tracks the adoption rate of new technologies (like AI, biotech) and their impact on productivity, capital expenditure (capex), and labor demand.
	•	Money and Financial Flows: Monitors interest rates, credit conditions, and the movement of liquidity between different asset classes and geographical regions.
	•	Geopolitical Power Shifts: Analyzes changes in trade relations, sanctions, supply chain vulnerabilities, and national strategies that affect resource allocation and market stability.
	•	Resource Scarcity: Tracks the availability and pricing of key industrial and energy commodities (oil, copper, lithium, water) as leading indicators of economic cycles.
	•	Cultural and Consumer Behavior Shifts: Observes long-term changes in consumer tastes, spending patterns, and social trends that create structural winners and losers in equity markets.

3.2. Decomposing Forces into Measurable Signals

Each global force must be decomposed into concrete, measurable signals.
Global Force
Measurable Signals / Proxies
Evolution of Technology
Chip demand (via manufacturers), cloud capex announcements, patent filing rates, software job posting trends, venture investment flows.
Money and Financial Flows
Yield curve slope (10y-2y), Credit Spreads (IG vs HY), ETF/Fund flows, DXY change, Central Bank statements (text analysis).
Geopolitical Power Shifts
Trade policy news sentiment, defense spending trends, commodity ratios (e.g., copper/gold), foreign exchange reserve movements.
Resource Scarcity
Baltic Dry Index (shipping), port congestion metrics, oil/gas inventory levels, price of industrial metals (copper, iron ore).
Cultural/Consumer Shifts
Google Trends z-scores for major product categories, retail sales momentum, unemployment rates, aggregate news sentiment by sector.

4. Data and Inputs

Data sources are structured in tiers, prioritizing availability and ease of implementation (Tier 1) before moving to high-value and proprietary sources for a true competitive edge (Tier 3).

4.1. Tier 1: Must-Have Data (The Foundation)

This data is generally free, public, and forms the starting point for the Two-Week MVP.
	•	Market Prices: Daily and high-frequency prices for major indices (S&P 500, NASDAQ, Russell), Cryptocurrencies (BTC, ETH), Oil (WTI), Gold, and Copper.
	•	Fixed Income: US Treasury yields (1m, 3m, 2y, 5y, 10y, 30y) from sources like FRED (Federal Reserve Economic Data).
	•	Core Macro Series: CPI, unemployment, retail sales, and Purchasing Managers' Index (PMI) data.
	•	Economic Calendar: Dates for key events like Fed meetings and major data releases.
	•	Volatility: Implied volatility indices (VIX) and realized volatility estimates for major indices.
	•	News: Basic news headlines and sentiment feeds from major financial outlets (FT, Reuters, WSJ).
	•	
4.2. Tier 2: High-Value Data (Next-Level Edge)

This data is added immediately after the MVP to boost predictive power.
	•	Credit/Liquidity: Credit spreads (e.g., Investment Grade vs. High Yield) and Credit Default Swap (CDS) indices.
	•	Fund Flows: Detailed ETF fund flows and Assets Under Management (AUM) changes.
	•	Search Trends: Google Trends data for thematic keywords and economic concepts.
	•	Supply Chain: Shipping and trade indices (Baltic Dry Index, container indices).
	•	Crypto: Basic on-chain crypto metrics (exchange net inflows/outflows, active addresses).
	•	Labor: Job posting and hiring trends data (from aggregators or platforms like LinkedIn APIs).
4.3. Tier 3: Advanced/Alternative Data (Proprietary Edge)

These are advanced, often costly or proprietary datasets that provide a significant competitive advantage.
	•	Economic Activity Proxies: Nighttime lights satellite data (as a proxy for granular economic activity).
	•	Physical Flows: AIS ship tracking and port congestion metrics.
	•	Innovation: Patent filings and detailed venture capital investment flow datasets.
	•	Specialty: Proprietary scraped datasets (conference transcripts, specialty research reports).

4.4. Data Governance and Licensing

For a professional system, data must be managed with compliance in mind.
Issue
Why it Matters
Fix/Mitigation
Licensing
Commercial use of some public APIs (e.g., some Bloomberg or Quandl data) is prohibited without a paid license.
Maintain a Data Governance Table listing license, cost, and usage restrictions for every Tier 2/3 dataset. Start with free sources only.
Data Freshness
Missing or late data can lead to stale features and incorrect signals.
Implement monitoring alerts (Section 7.3) with specific thresholds (e.g., 'Tier 1 pipeline latency > 2 hours → Alert').
Schema
Feature engineering relies on consistent column names, types, and frequencies.
Maintain an Appendix detailing the exact Parquet schema (field names, data types, update frequency) for the Feature Store.

5. Modeling Approach

The system achieves robustness by combining three distinct modeling paradigms using an Ensemble approach. This avoids relying on a single, potentially fragile methodology.
The core relationship can be expressed as: Forecast = f(Rule-based, Statistical, ML, Regime).

5.1. Paradigm 1: Theory-Derived Rule Engine

	•	Purpose: To encode human logic and known, causal macro relationships (e.g., Dalio-style economic cycles). Rules act as necessary safety checks and sanity filters for automated signals.
	•	Implementation: The engine uses a series of nested IF/THEN statements.
	•	Example Rule (for medium-term horizon): If (Yield Curve Slope (10y-2y) < 0) AND (Credit Spread Widening > 20% vs. 6-month Average) THEN Increase Recession Probability AND Reduce Equity Exposure (6-18 months).

5.2. Paradigm 2: Statistical Models and Econometrics

	•	Purpose: To quantify the strength and persistence of relationships and lead-lag effects between variables.
	•	Implementation: Techniques include Vector Autoregression (VAR) models, Granger Causality tests (to see if one time series is useful in forecasting another), and Impulse-Response Analysis. Regime-Switching Models (like Hidden Markov Models) will be implemented later to allow statistical relationships to change based on the detected market state.


5.3. Paradigm 3: Machine Learning Ensemble
	•	Purpose: To capture complex, nonlinear patterns in the data and effectively incorporate high-dimensional or alternative datasets (like news sentiment and Google Trends).
	•	Implementation:

	•	Core Models: Gradient Boosted Trees (XGBoost) for structured data; Recurrent Neural Networks (LSTMs) or Transformers for sequential features and alternative data.

	•	Validation: Strict temporal cross-validation (walk-forward validation) is non-negotiable to prevent look-ahead bias and overfitting. The model is trained on data up to time t and tested on t+1.


5.4. The Meta-Model: Bayesian Combination and Conviction Score

	•	Goal: To combine the outputs of the three paradigms into a single, actionable score.
	•	Combination: A Bayesian Updater or Stacking Classifier is used as the meta-model, which learns the optimal weights for blending the probabilistic outputs from the Rule Engine, Statistical Models, and ML Models.
	•	Conviction Score Formalization:
	•	Range: 0% to 100%, where 50% is neutral, and the score represents the system's belief in the forecast direction (e.g., a score of 85% bullish conviction for BTC means the system believes there is an 85% probability of the asset moving up over the target horizon).
	•	Thresholds: A conviction score must exceed a predefined Action Threshold (e.g., 75%) to generate a trade alert.

6. Risk Management and Safe Practices

Risk control must be integrated at every level of the system to prevent catastrophic losses and runaway automation.

6.1. Position Sizing and Portfolio Logic

	•	Methodology: Position size will be calculated using a combination of Volatility Parity (allocating less to more volatile assets) and the Kelly Criterion Fraction (to prevent over-leveraging based on historical edge).
	•	Formula (Concept):
	•	text
	•	Position Size ∝ (Target Portfolio Volatility / Asset Volatility) × Kelly Fraction × Conviction Score
	•	Drawdown Control: A Maximum Allowed Drawdown threshold (e.g., X% loss from peak-to-trough) will be maintained. A breach of this threshold must trigger an automatic switch to a low-risk, defensive allocation (e.g., 100% cash reserves).
	•	
6.2. System Kill-Switches and Emergency Procedures

The system must have defined and easily executable safety controls.
	•	Operational Kill-Switch: A defined, one-step process (e.g., a single command-line script) that immediately stops all launchd scheduled jobs, prevents further trade generations, and closes any open positions. This must be a simple, human-triggered action.
	•	Human-in-the-Loop (HITL): All high-conviction trades must be subject to a HITL check, requiring manual sign-off before a broker execution API is called. The automated execution remains semi-automated until the system achieves consistent, audited performance.
	•	
6.3. Model Governance and Auditability

	•	Version Control: Every version of the data, the features, the models, and the code must be logged and stored. This allows for absolute reproducibility of any trade signal.
	•	Performance Baselines: The system performance must be constantly compared against a simple, passive baseline strategy (e.g., a Buy-and-Hold strategy for the S&P 500) and a chance-level model (e.g., a simple 50/50 prediction). This ensures any recorded edge is real and not due to market tailwinds.
	•	Security: Credentials (API keys for brokers and data feeds) must be secured in a local key vault or encrypted storage.

7. Evaluation Metrics and Monitoring

The system is evaluated across three categories: the quality of its signals, the performance of the resulting portfolio, and the health of the underlying operations.

7.1. Predictive Metrics (Signal-Level)

These measure how accurate the model is at forecasting.
	•	AUC/ROC: Area Under the Curve (Receiver Operating Characteristic) to measure the classifier's performance across all thresholds.
	•	Precision@k: Measures the accuracy of the model's top-ranked predictions (e.g., how often the top 10% most convicted signals were correct).
	•	Brier Score: A measure of the calibration of the conviction score (ensures that when the system says 85% conviction, the trade is correct 85% of the time).
	•	Economic Alignment: Uses lead-lag correlation and Granger causality tests to prove that a signal is a leading indicator of the targeted macro outcome.
	•	
7.2. Portfolio Metrics (Strategy-Level)

These measure the real-world performance of the entire trading strategy.
	•	CAGR (Compounded Annual Growth Rate): The average annual growth over the backtested period.
	•	Sharpe/Sortino Ratio: Measures risk-adjusted returns (return earned per unit of risk).
	•	Max Drawdown: The largest peak-to-trough drop in the portfolio's capital. This is a critical risk metric.

7.3. Operational Monitoring

These ensure the system is running smoothly and reliably.
	•	Data Freshness: Daily check to confirm all Tier 1 and Tier 2 data feeds are updated within their required latency window.
	•	Pipeline Success Rate: Measures the percentage of scheduled nightly or event-driven jobs that complete without error.
	•	Script Execution Monitoring: Monitoring the successful completion of Python scripts via launchd scheduler logs.

8. Detailed Project Roadmap (Milestones and Tasks)

The plan is structured for rapid deployment, prioritizing the two-week Minimum Viable Product (MVP).

8.1. Week 1 — Data Pipeline and Simple Signals (MVP)
Milestone/Task
Owner
Estimated Time
Dependencies
Success Criteria (Acceptance Test)
M0: Project Setup
(Self)
1 Day
None
Git repository created, Python environment installed with core packages.
M1: Tier 1 Data Ingestion
(Self)
2 Days
M0
Ingestion scripts working for S&P 500, US Yields, BTC, DXY, and CPI data. 90 days of data ingested and stored as Parquet files with >99% daily freshness.
M2: Starter Feature Engineering
(Self)
2 Days
M1
Script to compute yield curve slope, DXY change, and VIX gap features. Normalized feature store created with lagged values (t, t-1).
M3: Rule Engine & Simple Backtest
(Self)
2 Days
M2
5-10 initial macro rules implemented and successfully backtested on historical data to show comparative performance against a simple Buy-and-Hold strategy.

8.2. Week 2 — ML, News, and Dashboard (MVP Complete)
Milestone/Task
Owner
Estimated Time
Dependencies
Success Criteria (Acceptance Test)
M4: News & Sentiment Pipeline
(Self)
2 Days
M0
Automated scraping of news headlines working. Simple sentiment (e.g., VADER) computed and aggregated into daily and weekly sentiment scores.
M5: Basic ML Modeling
(Self)
2 Days
M2, M4
Basic XGBoost classifier trained (predicting 1-month equity return). Walk-forward validation implemented with no look-ahead bias confirmed.
M6: Dashboard & Alerts
(Self)
3 Days
M5
Streamlit dashboard live showing signals, conviction score, and backtest results. Telegram/Email alerts triggered when conviction ≥ 75%.
M7: Paper Trading
(Self)
Ongoing
M6
Live signals tracked manually or via paper-trading API for 30 days. Performance logs collected daily and weekly.

8.3. Milestone 7 to 9: Scale and Automation
Milestone/Task
Focus
Primary Goal
M8: Scale & Advanced Data
Data & Modeling
Add Tier 2 and Tier 3 datasets. Implement more advanced models, including Regime Detection (e.g., Hidden Markov Models).
M9: Execution & Risk Automation
Operations & Safety
Connect to broker APIs (e.g., Alpaca, Interactive Brokers) for semi-automated execution with the Human-in-the-Loop safety step. Implement robust, automated kill-switches.

9. Future Improvements & Advanced Ideas

These upgrades will make the system more accurate, powerful, and defensive.
	•	Regime Detection (HMM, Clustering): Automatically detect the current market regime (e.g., 'inflationary,' 'recessionary,' 'growth') and dynamically adjust model weights and position sizes based on the regime. This prevents models trained in one environment from failing in another.
	•	Causal Graph & Counterfactuals: Build a visual causal network showing how features influence each other (e.g., 'Oil price leads CPI by 3 months'). This allows running 'what-if' scenarios (e.g., "what happens to the portfolio if the DXY spikes 5% in one week?").
	•	Satellite & Supply Chain Data Integration: Ingest specific high-value alternative data (nighttime lights, AIS shipping metrics) to generate earlier, proprietary signals for commodity and economic shifts.
	•	Explainable AI (XAI): Integrate a feature that produces a natural language summary explaining the Top 3 Drivers for every trade prediction (e.g., "Conviction is 82% because of rising credit spreads, strong tech capex, and a weakening dollar.").
	•	Meta-Learning & Continual Retraining: Develop a model that continuously adjusts the blending weights of the Rule, Statistical, and ML models based on their recent out-of-sample performance, ensuring the system adapts as global relationships change over time.
	•	Risk-Aware Optimization: Move beyond simple mean-variance optimization for portfolio construction and utilize more advanced methods like Conditional Value-at-Risk (CVaR) to better manage the potential for extreme losses.

10. Local Execution Plan and Runbook

This section details the daily, automated process using macOS launchd scheduler. The scheduling is set for daily at 6:00 AM to ensure a fresh signal before the market opens.

10.1. macOS launchd Configuration

The system uses macOS's built-in launchd service manager for scheduled execution. A launchd plist configuration file defines the daily 6:00 AM schedule and ensures reliable, automated execution of the Python pipeline.


10.2. Local Execution Architecture

	•	Execution Model: Pure deterministic Python scripts executed via launchd scheduler
	•	Runtime Environment: Local Mac only - scripts will stop if the Mac is shut down
	•	Safety Structure: No AI "Manager" component; only deterministic Python scripts that cannot hallucinate
	•	Cost Structure: Free (no cloud hosting costs)
	•	Dependency: Requires Mac to be powered on and awake at scheduled execution time

10.3. Daily Operations Runbook

	•	6:00 AM Daily Run: launchd executes the main orchestration script
	•	Script Execution Order:
	•	python scripts/agent_nightly_ingest.py - Fetch Tier 1 & 2 data
	•	python scripts/agent_feature_engineer.py - Calculate features and signals
	•	python scripts/agent_signal_generator.py - Generate trade signals
	•	python scripts/agent_news_scraper.py - Update news sentiment
	•	python scripts/agent_report_generator.py - Build daily PDF report
	•	python scripts/agent_telegram_alert.py - Send alerts for high-conviction signals
	•	Constraint: If any script fails, the entire pipeline stops and sends an alert
	•	Manual Review (7:00 AM): Review PDF report and Telegram/email alerts
	•	Market Open (Execution): Manual review of high-conviction signals and execution via broker API (Human-in-the-Loop)
	•	Logging: Save all predictions and inputs for auditing and future model retraining
            Weekly and Monthly Review Checklist
	•	Weekly: Evaluate past week's signals, update model performance logs, check data freshness, and analyze any operational failures.
	•	Monthly: Re-run full backtest on latest data, review feature importance, and analyze missed opportunities.
	•	Quarterly: Add new data sources, validate regime detection, and update risk parameters.

