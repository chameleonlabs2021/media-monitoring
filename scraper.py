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
from sentimental import *

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
        company_found = False
        for link in soup.find_all('a', href=True):
            # print(link)
            link_text = link.text.strip()
            if companyname.lower() in link_text.lower():
                print(f"Company name '{companyname}' found in link: {link_text}")
                matching_links.append((link['href'], link_text))
                company_found = True
                print("matching_links",matching_links)
        if not company_found:
            print(f"Company name '{companyname}' not found in any link.")

        # Visit each matching link and extract content if keyword is found
        keyword_found = False
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
                keyword_found = True
                print(f"Keyword '{keyword}' found in content of link: {link}")
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

        if not keyword_found:
            print(f"Keyword '{keyword}' not found in content of any link for company '{companyname}'.")

if __name__ == "__main__":
    # Define the URL
    # url = "https://timesofindia.indiatimes.com/india"  
    # url ="https://web.archive.org/web/20230927222838/http://new.yahoo.com/"
    # url ="https://web.archive.org/web/20201203004302/https://timesofindia.indiatimes.com/india/"
    url = "https://news.yahoo.com"
    companyname="congress"
    keyword="Wildfires"
    # Get URL from prompt
    url = input("Enter the URL: ")

    # Get keywords from prompt
    # companyname = input("Enter companyname: ")
    keyword = input("Enter keyword to search on this company: ")
    # Initialize Scraper
    scraper = Scraper(url)

    # # Read company names and keywords from CSV file
    # with open('keywords.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     next(reader)  # Skip the header row
    #     for row in reader:
    #         companyname, keyword = row[0], row[1]
    #         scraper.scrape_links_with_keywords(companyname, keyword)
    scraper.scrape_links_with_keywords(companyname, keyword)

    json_file_path = f'{companyname}_matching_links_with_content.json'
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Extract the "Link Text" data
    link_text = data.get("Link Text", "")

    # Example texts
    text1 = link_text  # You can replace these with the actual text from the JSON file

    # Call sentiment analysis functions with the extracted text
    print(give_score_textblob_sentiment(text1))

    print(give_score_vadare_sentiment(text1))

    print(give_score_flair_sentiment(text1))
