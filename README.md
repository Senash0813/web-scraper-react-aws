# Web Scraper for React and AWS Lambda Documentation

This Python script scrapes content from React and AWS Lambda documentation websites. The scraped data is stored in a JSON file.

---

## Requirements

Before running the script, make sure you have the following installed:

- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

---

## Setup Instructions

### 1. Install Dependencies

Install the required Python libraries using `pip`:
pip install -r requirements.txt


### 2. Download chromedriver

Download the appropriate ChromeDriver version for your Chrome browser from the official site.
Update the path in the script to point to your ChromeDriver executable. Modify this line in the code:

service = Service('/Users/senash/Downloads/chromedriver/chromedriver') 

### 3. Run script

open terminal
run 'python scrape.py'



