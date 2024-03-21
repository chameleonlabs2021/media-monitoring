from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from sentianaylib import sentianaylib
import os

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=ChromeOptions)

current_directory = os.path.dirname(os.path.abspath(__file__))
# Initialize sentianalib with the appropriate driver
sentianaylib_instance = sentianaylib(driver)

# Perform sentiment analysis on a webpage
url = 'https://www.yahoo.com/'
keyword = 'wilmar child labour'
sentianaylib_instance.dataprocessor(url, keyword, current_directory)