import os
import csv
import time
import traceback
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
NUM_PAGES = int(os.getenv("NUM_PAGES"))
RATE_LIMIT = int(os.getenv("RATE_LIMIT"))
CSV_FILENAME = os.getenv("CSV_FILENAME")

# Set up headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

def scrape_quicket_events():
    events = []
    try:
        driver.get(BASE_URL)
    except Exception as e:
        print(f"Error loading BASE_URL: {BASE_URL}")
        print(traceback.format_exc())
        return

    pages_scraped = 0

    while pages_scraped < NUM_PAGES:
        try:
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            events_container = soup.select_one("ol.l-event-container")
            if not events_container:
                print(f"No events container found on {driver.current_url}")
                print(driver.page_source[:500])
                break

            event_items = events_container.select("li.l-event-item")
            if not event_items:
                print(f"No event items found on {driver.current_url}")
                break

            for item in event_items:
                try:
                    title_tag = item.select_one("ais-highlight")
                    title = title_tag.get_text(strip=True) if title_tag else "N/A"
                    location_tag = item.select_one("div.l-hit-venue")
                    location = location_tag.get_text(strip=True) if location_tag else "N/A"
                    date_container = item.select_one("div.l-date-container")
                    if date_container:
                        date_divs = date_container.select("div.l-date")
                        if len(date_divs) >= 2:
                            event_date = date_divs[0].get_text(strip=True)
                            event_time = date_divs[1].get_text(strip=True)
                        elif len(date_divs) == 1:
                            event_date = date_divs[0].get_text(strip=True)
                            event_time = "N/A"
                        else:
                            event_date, event_time = "N/A", "N/A"
                    else:
                        event_date, event_time = "N/A", "N/A"
                    events.append([title, location, event_date, event_time])
                except Exception as inner_e:
                    print(f"Error parsing an event item: {inner_e}")
                    print(traceback.format_exc())
                    continue
            pages_scraped += 1
            print(f"Scraped page {pages_scraped}: {driver.current_url}")

            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "li.ais-Pagination-item--nextPage a.ais-Pagination-link"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)
                next_button.click()
                time.sleep(RATE_LIMIT)
            except (NoSuchElementException, TimeoutException) as nav_e:
                print("No next page found, ending pagination.")
                break
            except ElementClickInterceptedException as click_e:
                print(f"Error clicking next button: {click_e}")
                print(traceback.format_exc())
                break
            except Exception as nav_generic:
                print(f"Unexpected error during navigation: {nav_generic}")
                print(traceback.format_exc())
                break
        except Exception as general_e:
            print(f"Error scraping page {pages_scraped + 1}: {general_e}")
            print(traceback.format_exc())
            break

    try:
        with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Event Title", "Event Location", "Event Date", "Event Time"])
            writer.writerows(events)
        print(f"Scraping complete. Data saved to {CSV_FILENAME}")
    except Exception as file_e:
        print(f"Error writing CSV file: {file_e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    scrape_quicket_events()
    driver.quit()
