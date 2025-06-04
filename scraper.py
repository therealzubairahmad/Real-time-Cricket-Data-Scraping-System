import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.helpers import save_json, get_text_safe

# Setup Selenium options (headless mode)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Fixtures URL (main match list)
FIXTURE_URL = "https://crex.live/fixtures/match-list"

# Set output directory
FIXTURE_OUTPUT = "data/fixtures/fixtures.json"
MATCH_DIR = "data/matches/"


def scrape_fixtures():
    """Scrapes the fixture list from CREX and saves it."""
    print("[INFO] Scraping match fixtures...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(FIXTURE_URL)
    time.sleep(3)  # wait for JS to load

    matches = []
    match_cards = driver.find_elements(By.CLASS_NAME, "cb-mtch-lst-itm")

    for card in match_cards:
        try:
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            teams = card.find_element(By.CLASS_NAME, "cb-mtch-tm-nm").text
            datetime_str = card.find_element(By.CLASS_NAME, "cb-mtch-dt-tm").text

            matches.append({
                "teams": teams,
                "start_time": datetime_str,
                "url": link
            })
        except NoSuchElementException:
            continue

    driver.quit()
    save_json(matches, FIXTURE_OUTPUT)
    print(f"[INFO] Fixtures saved to {FIXTURE_OUTPUT}")


def scrape_match_details(match_url):
    """Scrape individual match tabs: Match Info, Squads, Live, Scorecard."""
    print(f"[INFO] Scraping match details from: {match_url}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(match_url)
    time.sleep(3)

    match_data = {"url": match_url}

    try:
        # Match Info Tab
        info_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Match Info')]")
        info_tab.click()
        time.sleep(1)
        info_content = driver.find_element(By.CLASS_NAME, "cb-mtch-dtl").text
        match_data["match_info"] = info_content
    except NoSuchElementException:
        match_data["match_info"] = "Not found"

    try:
        # Squads Tab
        squads_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Squads')]")
        squads_tab.click()
        time.sleep(1)
        squads = driver.find_element(By.CLASS_NAME, "cb-mtch-sqd").text
        match_data["squads"] = squads
    except NoSuchElementException:
        match_data["squads"] = "Not found"

    try:
        # Scorecard Tab
        scorecard_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Scorecard')]")
        scorecard_tab.click()
        time.sleep(2)
        scorecard = driver.find_element(By.CLASS_NAME, "cb-scrcrd-cntnr").text
        match_data["scorecard"] = scorecard
    except NoSuchElementException:
        match_data["scorecard"] = "Not available"

    try:
        # Live Tab
        live_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Live')]")
        live_tab.click()
        time.sleep(2)
        live = driver.find_element(By.CLASS_NAME, "cb-mtch-lv").text
        match_data["live"] = live
    except NoSuchElementException:
        match_data["live"] = "Not available"

    match_id = match_url.strip('/').split('/')[-1]
    output_path = os.path.join(MATCH_DIR, f"{match_id}.json")
    save_json(match_data, output_path)
    driver.quit()
    print(f"[INFO] Match data saved: {output_path}")


if __name__ == "__main__":
    # Run full scrape once (for testing)
    scrape_fixtures()
    with open(FIXTURE_OUTPUT, 'r') as f:
        fixtures = json.load(f)

    # Scrape first 2 matches as example
    for match in fixtures[:2]:
        scrape_match_details(match['url'])
