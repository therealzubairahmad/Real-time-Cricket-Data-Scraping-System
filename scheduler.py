import json
import time
from datetime import datetime, timedelta
from scraper import scrape_match_details

FIXTURE_FILE = "data/fixtures/fixtures.json"

def is_match_due(start_time):
    """ Check if current time is close to match start time (within ±5 minutes).
    Expects start_time in format like: "Thu, 06 Jun 2024, 03:30 PM" """
    try:
        match_dt = datetime.strptime(start_time, "%a, %d %b %Y, %I:%M %p")
        now = datetime.now()
        return abs((now - match_dt).total_seconds()) <= 300  # 5 minutes
    except Exception as e:
        print("[ERROR] Date parsing failed:", e)
        return False

def run_scheduler():
    """ Loads fixture list and scrapes only matches that are starting. """
    print("[INFO] Running scheduler...")
    try:
        with open(FIXTURE_FILE, 'r') as f:
            matches = json.load(f)
    except FileNotFoundError:
        print("[ERROR] Fixtures file not found.")
        return

    for match in matches:
        if is_match_due(match['start_time']):
            print(f"[INFO] Triggering scrape for match: {match['teams']}")
            scrape_match_details(match['url'])
        else:
            print(f"[SKIP] {match['teams']} not yet due.")

if __name__ == "__main__":
    # Run this periodically using cron or schedule
    run_scheduler()
