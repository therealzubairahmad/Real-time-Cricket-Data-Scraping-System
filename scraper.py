import os
import json
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from utils.helpers import save_json  # assuming get_text_safe not used here

# Fixtures URL (main match list)
FIXTURE_URL = "https://crex.live/fixtures/match-list"

# Set output directory
FIXTURE_OUTPUT = "data/fixtures/fixtures.json"
MATCH_DIR = "data/matches/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_fixtures():
    print("[INFO] Scraping match fixtures...")

    response = requests.get(FIXTURE_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    matches = []
    match_cards = soup.find_all("div", class_="cb-mtch-lst-itm")

    for card in match_cards:
        link_tag = card.find("a")
        team_tag = card.find("div", class_="cb-mtch-tm-nm")
        time_tag = card.find("div", class_="cb-mtch-dt-tm")

        if link_tag and team_tag and time_tag:
            matches.append({
                "teams": team_tag.text.strip(),
                "start_time": time_tag.text.strip(),
                "url": "https://crex.live" + link_tag["href"]
            })

    save_json(matches, FIXTURE_OUTPUT)
    print(f"[INFO] Fixtures saved to {FIXTURE_OUTPUT}")


def scrape_match_details(match_url):
    print(f"[INFO] Scraping match details from: {match_url}")

    response = requests.get(match_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    match_data = {"url": match_url}

    def get_tab_content(tab_name, class_name):
        tab_link = soup.find("a", string=tab_name)
        if not tab_link or not tab_link.get("href"):
            return "Not found"
        tab_url = "https://crex.live" + tab_link.get("href")
        tab_response = requests.get(tab_url, headers=headers)
        tab_soup = BeautifulSoup(tab_response.text, "html.parser")
        content = tab_soup.find("div", class_=class_name)
        return content.text.strip() if content else "Not found"

    match_data["match_info"] = get_tab_content("Match Info", "cb-mtch-dtl")
    match_data["squads"] = get_tab_content("Squads", "cb-mtch-sqd")
    match_data["scorecard"] = get_tab_content("Scorecard", "cb-scrcrd-cntnr")
    match_data["live"] = get_tab_content("Live", "cb-mtch-lv")

    match_id = match_url.strip('/').split('/')[-1]
    output_path = os.path.join(MATCH_DIR, f"{match_id}.json")
    save_json(match_data, output_path)
    print(f"[INFO] Match data saved: {output_path}")


if __name__ == "__main__":
    scrape_fixtures()

    with open(FIXTURE_OUTPUT, 'r') as f:
        fixtures = json.load(f)

    for match in fixtures[:2]:
        scrape_match_details(match['url'])
