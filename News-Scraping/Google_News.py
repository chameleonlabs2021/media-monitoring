import requests
import pandas as pd
from bs4 import BeautifulSoup

keyword = 'wilmar child labour'
api_url = 'https://api.scrape-it.cloud/scrape/google'

headers = {'x-api-key': '51957f6d-0477-4ca9-8427-3664c2e745fa'}

params = {
    'q': keyword,
    'domain': 'google.com',
    'tbm': 'nws'
}

response = requests.get(api_url, params=params, headers=headers)

data = response.json()

news = data['newsResults']

full_content = []

for item in news:
    url = item['link']
    article_response = requests.get(url)
    soup = BeautifulSoup(article_response.content, 'html.parser')
    content = soup.get_text()
    item['full_content'] = content
    full_content.append(item)

df = pd.DataFrame(full_content)

df.to_csv("news_result.csv", index=False)
