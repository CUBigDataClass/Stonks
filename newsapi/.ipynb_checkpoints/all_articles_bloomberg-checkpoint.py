from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key=API_KEY)

# /v2/everything
newsapi.get_everything(domains='bloomberg.com',
                                      page=1)
