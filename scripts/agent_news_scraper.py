import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION (PATH FIX) ---
import os
# Get absolute path of THIS script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up to Project Root
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Define absolute paths
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")
TODAY_STR = datetime.now().strftime("%Y%m%d")

# RSS Feeds (The "Eyes")
RSS_FEEDS = {
    "Reuters_World": "https://feeds.reuters.com/Reuters/worldNews",
    "Reuters_Biz": "https://feeds.reuters.com/Reuters/businessNews",
    "CNBC_Top": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "Investing_Forex": "https://www.investing.com/rss/news_1.rss"
}

def analyze_news():
    print(f"🚀 AGENT: News Scraper Initiated [{TODAY_STR}]...")
    analyzer = SentimentIntensityAnalyzer()
    
    all_headlines = []
    
    # 1. SCRAPE FEEDS
    for source, url in RSS_FEEDS.items():
        try:
            print(f"   Reading feed: {source}...")
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:10]: # Top 10 per feed
                title = entry.title
                # 2. SCORE SENTIMENT
                # Compound score: -1 (Negative) to +1 (Positive)
                sentiment = analyzer.polarity_scores(title)['compound']
                
                all_headlines.append({
                    "Source": source,
                    "Title": title,
                    "Sentiment": sentiment,
                    "Link": entry.link
                })
        except Exception as e:
            print(f"   ❌ Error reading {source}: {e}")

    if not all_headlines:
        print("❌ No news found.")
        return

    # 3. AGGREGATE
    df = pd.DataFrame(all_headlines)
    avg_sentiment = df['Sentiment'].mean()
    
    # Determine Mood
    if avg_sentiment < -0.05: mood = "FEAR / NEGATIVE"
    elif avg_sentiment > 0.05: mood = "GREED / POSITIVE"
    else: mood = "NEUTRAL"
    
    # Find Top "Risk" Headlines (Most Negative)
    risk_stories = df.sort_values(by="Sentiment").head(3)
    
    print(f"\n📊 GLOBAL SENTIMENT: {avg_sentiment:.4f} ({mood})")
    print("   Top Risk Stories:")
    for i, row in risk_stories.iterrows():
        print(f"   - {row['Title']} ({row['Sentiment']})")

    # 4. SAVE SUMMARY FOR REPORT AGENT
    # We save a simple text file that Agent #4 can read easily
    summary_path = os.path.join(OUTPUT_DIR, "daily_news_summary.txt")
    
    with open(summary_path, "w") as f:
        f.write(f"Global Sentiment: {mood} (Score: {avg_sentiment:.2f})\n")
        f.write("Top Geopolitical Risks:\n")
        for i, row in risk_stories.iterrows():
            clean_title = row['Title'].replace("\n", " ").strip()
            f.write(f"- {clean_title}\n")
    
    print(f"✅ News Summary Saved: {summary_path}")

if __name__ == "__main__":
    analyze_news()