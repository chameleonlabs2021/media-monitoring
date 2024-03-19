import sys
import requests as rq
from bs4 import BeautifulSoup as bs
from time import sleep
from time import time
from random import randint
from warnings import warn
import json
import pandas as pd 
from scraper import Scraper

import csv


website_url = ''
output_file = 'json'
from_date = ''
to_date = ''


class capture_json_creator:
    pass





# Define the base URL for the CDX API
base_url = 'http://web.archive.org/cdx/search/cdx'

# Define your query parameters
query_params = {
    'url': 'timesofindia.indiatimes.com/india/',  # Specify the URL you want to search for
    'output': 'json',      # Request JSON format for the response
    'from': '20201203',        # Specify the start date (YYYYMMDD format)
    'to': '20231230'           # Specify the end date (YYYYMMDD format)
}

# Make the HTTP request to the CDX API
response = rq.get(base_url, params=query_params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    results = response.json()
    # Process the results as needed

    # Write the results to a JSON file
    with open('wayback_data.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print('Data has been successfully saved to wayback_data.json')
    # for snapshot_info in results:
    #     # Extract relevant data from the snapshot_info
    #     print(snapshot_info)
else:
    print('Error: Failed to retrieve data from the CDX API')


import json

def create_archive_urls(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    archive_urls = []
    for item in data:
        timestamp = item[1]
        original_url = item[2]

        archive_url = f"https://web.archive.org/web/{timestamp}/{original_url}"
        archive_urls.append(archive_url)

    return archive_urls

# Example usage:
json_file = 'wayback_data.json'  # Replace 'your_json_file.json' with the path to your JSON file
urls = create_archive_urls(json_file)
for url in urls:
    print(url)
    # scraper.scraper
        # Initialize Scraper
    scraper = Scraper(url)

    # Read company names and keywords from CSV file
    with open('keywords.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            companyname, keyword = row[0], row[1]
            scraper.scrape_links_with_keywords(companyname, keyword)


