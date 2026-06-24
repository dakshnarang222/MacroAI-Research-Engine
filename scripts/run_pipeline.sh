#!/bin/bash

# 1. Force navigation
cd /Users/dakshnarang/Desktop/MacroAI_ResearchEngine || exit

# 2. Activate Python
source venv/bin/activate

echo "=========================================="
echo " MacroAI Automation Pipeline Started"
echo "=========================================="

# 3. Run Agents in Order

echo "Step 0: Generating Asset Universe..."
python scripts/utils_universe_generator.py

echo "Step 1: Running Nightly Ingest..."
python scripts/agent_nightly_ingest.py

echo "Step 2: Running Feature Engineer..."
python scripts/agent_feature_engineer.py

echo "Step 3: Running Signal Generator..."
python scripts/agent_signal_generator.py

echo "Step 4: Running News Scraper..."
python scripts/agent_news_scraper.py

echo "Step 5: Running AI Model Trainer..."
python scripts/agent_model_trainer.py

echo "Step 6: Running Report Generator..."
python scripts/agent_report_generator.py

echo "Step 7: Sending Telegram Alert..."
python scripts/agent_telegram_alert.py

echo "=========================================="
echo " ✔ Pipeline Completed Successfully"
echo "=========================================="#!/bin/bash

# --- CONFIGURATION ---
# Robust way to find the script's directory (works from anywhere)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."
LOG_DIR="$PROJECT_ROOT/logs"
DATE_STR=$(date +%Y%m%d)
LOG_FILE="$LOG_DIR/pipeline_$DATE_STR.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Helper function for logging (Prints to Screen AND File)
log() {
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [$1] $2" | tee -a "$LOG_FILE"
}

# START
echo "==================================================" | tee -a "$LOG_FILE"
echo "   🚀 MACRO AI AUTO-PILOT STARTED" | tee -a "$LOG_FILE"
echo "   📝 Logs saved to: $LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"

# Activate Python Virtual Environment
source "$PROJECT_ROOT/venv/bin/activate"

# --- STEP 0: MAP MAINTENANCE ---
log "INFO" "Step 0/7: Generating Asset Universe (Map Hygiene)..."
python "$SCRIPT_DIR/utils_universe_generator.py" >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then log "ERROR" "Universe Generation Failed."; exit 1; fi

# --- STEP 1: INGESTION (Layer 1) ---
log "INFO" "Step 1/7: Running Nightly Ingestion (Data Lake)..."
python "$SCRIPT_DIR/agent_nightly_ingest.py" >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then log "ERROR" "Ingestion Failed."; exit 1; fi

# --- STEP 2: INTELLIGENCE (Layer 2) ---
log "INFO" "Step 2/7: Feature Engineering (Math Engine)..."
python "$SCRIPT_DIR/agent_feature_engineer.py" >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then log "ERROR" "Feature Engineering Failed."; exit 1; fi

# --- STEP 3: DECISION (Layer 3) ---
log "INFO" "Step 3/7: Running Signal Engine (Rule-Based)..."
# We allow this to print to screen so you see the report immediately
python "$SCRIPT_DIR/signal_engine.py" | tee -a "$LOG_FILE"

# --- STEP 4: SENTIMENT (Future Layer) ---
log "INFO" "Step 4/7: Scrape News Sentiment..."
if [ -f "$SCRIPT_DIR/agent_news_scraper.py" ]; then
    python "$SCRIPT_DIR/agent_news_scraper.py" >> "$LOG_FILE" 2>&1
else
    log "WARN" "agent_news_scraper.py not found. Skipping."
fi

# --- STEP 5: PREDICTION (Future Layer) ---
log "INFO" "Step 5/7: Training AI Models..."
if [ -f "$SCRIPT_DIR/agent_model_trainer.py" ]; then
    python "$SCRIPT_DIR/agent_model_trainer.py" >> "$LOG_FILE" 2>&1
else
    log "WARN" "agent_model_trainer.py not found. Skipping."
fi

# --- STEP 6: REPORTING ---
log "INFO" "Step 6/7: Generating PDF Report..."
if [ -f "$SCRIPT_DIR/agent_report_generator.py" ]; then
    python "$SCRIPT_DIR/agent_report_generator.py" >> "$LOG_FILE" 2>&1
else
    log "WARN" "agent_report_generator.py not found. Skipping."
fi

# --- STEP 7: ALERTING ---
log "INFO" "Step 7/7: Sending Telegram Alerts..."
if [ -f "$SCRIPT_DIR/agent_telegram_alert.py" ]; then
    python "$SCRIPT_DIR/agent_telegram_alert.py" >> "$LOG_FILE" 2>&1
else
    log "WARN" "agent_telegram_alert.py not found. Skipping."
fi

echo ""
log "DONE" "Pipeline Finished Successfully."