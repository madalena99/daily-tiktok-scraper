import os
import requests
from TikTokApi import TikTokApi

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "TikTokIdeas"

HEADERS = {
    "Authorization": f"Bearer " + AIRTABLE_API_KEY,
    "Content-Type": "application/json"
}

HASHTAGS = [
    "insurance", "insuranceclaims", "claimdenied", "healthinsurance",
    "moneytips", "reimbursement", "medicalbills", "lifehack", "adulting"
]

def post_to_airtable(item):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_NAME}"
    response = requests.post(url, headers=HEADERS, json={"fields": item})
    print(f"Uploaded: {item['Hook'][:50]}... | Status: {response.status_code}")

def run_scraper():
    print("Launching TikTok scraper...")
    api = TikTokApi()
    for hashtag in HASHTAGS:
        print(f"Searching #{hashtag}")
        try:
            results = api.hashtag(name=hashtag).videos(count=10)
            for video in results:
                try:
                    data = {
                        "hook": video.desc[:80],
                        "caption": video.desc,
                        "likes": video.stats.digg_count,
                        "url": f"https://www.tiktok.com/@{video.author.username}/video/{video.id}",
                        "hashtags": "#" + " #".join([tag.name for tag in video.hashtags]) if video.hashtags else ""
                    }
                    if data["likes"] >= 500:
                        post_to_airtable({
                            "Hook": data["hook"],
                            "Caption": data["caption"],
                            "Likes": data["likes"],
                            "Video URL": data["url"],
                            "Hashtags": data["hashtags"]
                        })
                except Exception as e:
                    print("⚠️ Error parsing video:", e)
        except Exception as e:
            print("❌ Error fetching hashtag:", e)
    api.close()

if __name__ == "__main__":
    run_scraper()
