import os
import time
import random
import json
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
import nltk
from nltk.corpus import wordnet

# Download WordNet corpus if not already downloaded
nltk.download('wordnet')

class Scraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
    
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def get_synonyms(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return list(synonyms)
    
    def filter_content(self, data, keyword):
        filtered_data = []
        synonyms = self.get_synonyms(keyword)
        keyword_found = False
        for item in data:
            content = item['Content']
            if keyword.lower() in content.lower():
                filtered_data.append(item)
                keyword_found = True
            elif not keyword_found:
                for synonym in synonyms:
                    if synonym.lower() in content.lower():
                        filtered_data.append(item)
                        break  # Break the loop if a synonym is found
        return filtered_data
    
    def scrape_links_with_keywords(self, companyname, keyword):
        self.driver.get(self.url)

        # Get initial page height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        time.sleep(random.uniform(1, 3))  # Random delay between 1 to 3 seconds

        # Scroll down and wait for some time for more content to load
        while True:
            # Scroll down to the bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for some random time to let the page load
            time.sleep(random.uniform(2, 4))  # Random delay between 2 to 4 seconds
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same, no more new content is loaded, exit the loop
                break
            last_height = new_height

        # Get the HTML content of the page
        html_content = self.driver.page_source

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract links containing the company name
        matching_links = []
        for link in soup.find_all('a', href=True):
            # print(link)
            link_text = link.text.strip()
            if companyname.lower() in link_text.lower():
                print("====================",companyname)
                matching_links.append((link['href'], link_text))
                print("matching_links",matching_links)

        # Visit each matching link and extract content if keyword is found
        for link, text in matching_links:
            # Check if the link is a relative path
            if not link.startswith("http"):
                link = urljoin(self.url, link)  # Convert relative path to absolute URL
            
            self.driver.get(link)
            time.sleep(random.uniform(3, 6))  # Random delay between 3 to 6 seconds
            
            # Get the HTML content of the current page
            page_html = self.driver.page_source
            
            # Parse the HTML content of the current page
            page_soup = BeautifulSoup(page_html, 'html.parser')
            
            # Extract main content from different HTML elements
            main_content = ''
            for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                elements = page_soup.find_all(tag)
                for element in elements:
                    main_content += element.text + '\n'
            
            # Check if keyword is present in the main content
            if keyword.lower() in main_content.lower():
                print("keyword=========",keyword)
                # Store the data
                data = {
                    'Company Name': companyname,
                    'URL': link,
                    'Link Text': text,
                    'Content': main_content
                }

                # Write data to a JSON file
                json_file_path = f'{companyname}_matching_links_with_content.json'
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)

                print(f'Matching links and their content saved to {json_file_path}')
                break  # Exit loop after finding the first matching link

if __name__ == "__main__":
    # Define the URL
    url = "https://web.archive.org/web/20201203004302/https://timesofindia.indiatimes.com/india"

    # Initialize Scraper
    scraper = Scraper(url)

    # Read company names and keywords from CSV file
    with open('keywords.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            companyname, keyword = row[0], row[1]
            scraper.scrape_links_with_keywords(companyname, keyword)
