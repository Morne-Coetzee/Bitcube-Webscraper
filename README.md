# Bitcube-Webscraper

Bitcube-Webscraper is a Python-based web scraper designed to extract event data from the Quicket website and export it to a CSV file. This project uses Selenium for browser automation, BeautifulSoup for parsing HTML, and dotenv for managing environment variables.

## Features

- Headless Chrome browser integration for scraping without a GUI.
- Extraction of event title, location, date, and time.
- Pagination handling with robust error checking.
- CSV export with configurable filename.

## Prerequisites

- [Python 3.7+](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (compatible with your Chrome version)
- Required Python libraries:
  - `selenium`
  - `beautifulsoup4`
  - `python-dotenv`

You can install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone the Repo
`git clone https://github.com/Morne-Coetzee/Bitcube-Webscraper.git`
Then cd to the repo:
`cd Bitcube-Webscraper`

2. Create a Virtual Environment
`python -m venv venv`
- `venv\Scripts\activate` on windows
- `source venv/bin/activate` macOS/Linux

3. Install Dependencies
`pip install -r requirements.txt`

4. Configure Environment Variables
Create a .env file in the project root with the following content:
`
BASE_URL=https://www.quicket.co.za/your-target-url
NUM_PAGES=5
RATE_LIMIT=3
CSV_FILENAME=events.csv
`

BASE_URL: Starting URL for scraping.
NUM_PAGES: Number of pages to scrape.
RATE_LIMIT: Wait time (in seconds) between page navigations.
CSV_FILENAME: Output CSV filename.

## Usage

Run the scraper with:
`python scraper.py`

The script will start a headless Chrome session, navigate through the specified number of pages, and save the scraped event data to the CSV file defined by CSV_FILENAME.

If you want to view the web version, run this command:
`python -m http.server`

Navigate to the following page:
`http://127.0.0.1:8000/quicket-events.html`

## Troubleshooting

- ChromeDriver Issues: Ensure ChromeDriver matches your installed version of Google Chrome and is in your system's PATH or correctly specified.
- Environment Variables: Verify the .env file for correct variable names and values.
- Permissions: Check folder permissions if you have issues writing the CSV file.
