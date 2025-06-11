import requests
from datetime import datetime
import os

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = "TikTokIdeas"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

def post_to_airtable(data):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    for item in data:
        print("Uploading:", item)  # DEBUG
        record = {
            "fields": {
                "Hook": item["hook"],
                "Caption": item["caption"],
                "Likes": item["likes"],
                "Video URL": item["url"],
                "Hashtags": item["hashtags"],
            }
        }
        response = requests.post(url, headers=HEADERS, json=record)
        print("Status:", response.status_code)
        print("Response:", response.text)

def scrape_tiktoks():
    # This is fake data for now — we’ll automate real scraping later
    sample_data = [
        {
            "hook": "Did you know you can get money back from insurance?",
            "caption": "Most people don’t know this hidden hack...",
            "likes": 124000,
            "url": "https://www.tiktok.com/@user/video/1234567890",
            "hashtags": "#insurance #moneyback #claim"
        }
    ]
    return sample_data

if __name__ == "__main__":
    print("Running TikTok scraper...")
    data = scrape_tiktoks()
    if not data:
        print("⚠️ No data returned by scrape_tiktoks(). Exiting.")
    else:
        print(f"✅ {len(data)} TikTok(s) found. Uploading to Airtable...")
        post_to_airtable(data)
