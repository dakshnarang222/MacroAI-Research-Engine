import requests
import os
import glob

# --- CONFIGURATION (PATH FIX) ---
import os
# Get absolute path of THIS script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up to Project Root
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Your Keys (Keep these!)
BOT_TOKEN = "8561041292:AAGgvtrs-f3Mi6gMUYqwUq2tQUEpNO16CoY"
CHAT_ID = "8260272777"

# Define absolute paths
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")

def send_latest_report():
    print("🚀 AGENT: Telegram Alert Initiated...")

    # 1. Find the latest PDF in the outputs folder
    # We look for any file ending in .pdf
    list_of_files = glob.glob(os.path.join(OUTPUT_DIR, "*.pdf"))
    
    if not list_of_files:
        print("❌ No PDF report found to send.")
        print("   (Make sure Agent #4 ran successfully first!)")
        return

    # Get the most recent file based on creation time
    latest_file = max(list_of_files, key=os.path.getctime)
    filename = os.path.basename(latest_file)
    print(f"📄 Found report: {filename}")

    # 2. Send to Telegram API
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    try:
        print("   Sending to phone...")
        with open(latest_file, "rb") as f:
            # Prepare the payload
            files = {"document": f}
            data = {
                "chat_id": CHAT_ID, 
                "caption": f"🦅 **MacroAI Update**\nHere is your strategy note for today."
            }
            
            # Post the request
            response = requests.post(url, data=data, files=files)
        
        # 3. Check Success
        if response.status_code == 200:
            print("✅ Message sent successfully! Check your Telegram.")
        else:
            print(f"❌ Failed to send. Telegram says: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_latest_report()