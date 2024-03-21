from newsapi import NewsApiClient
api_key = "abf021202ad3499caff08a2ec72fad74"
newsapi = NewsApiClient(api_key=api_key)

all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

print(all_articles)