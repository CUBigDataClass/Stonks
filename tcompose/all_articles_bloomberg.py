from newsapi import NewsApiClient
from request_parameters import * 
from keys import *
import os
from google.cloud import storage
from datetime import datetime, timedelta
import time
from companies import *
from db_keys import *
from postGres import *
from json import dumps
from json import loads
# from kafka import KafkaProducer
import requests
import schedule
import json

from pathlib import Path

class NewsArticles(NewsApiClient):
    """Using from newsapi's NewsApiClient. Adding functions to get our customized queries."""

    def __init__(self,API_KEY_NEWSAPI, companies,sources, languages):
        self.newsapi = NewsApiClient(api_key=API_KEY_NEWSAPI)  # Open connection to newsapi API 
        self.companies = companies
        self.sources = sources
        self.languages = languages
        self.page = 1 
        self.page_size = 100

    #currently O(n^2) time complexity, could optimize
    #maybe use dict
    def get_everything(self):
        
        #initializing connection
        pg = GCP_PostGreSQL(con_name, user, pw, db, tickers)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
        bucket_name = 'stonksbucket'
        destination_blob_name = 'news'
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        with pg.pool.connect() as db_conn:
        # Loop through specificied companies
            for company in self.companies:
                # ticker name
                ticker=map1[company]
                from_time = self.get_from_time(ticker)
                
                #company = str(self.companies[i])
                # /v2/ All articles published some time ago of company
                raw_data = self.newsapi.get_everything(
                    q=company,
                    sources=self.sources,
                    language=self.languages[0],
                    from_param=from_time,
                    page=self.page,
                    page_size=self.page_size)
                #articles = self.addCompanyUniqueField(raw_data, companyName, companyTicker)

                #raw_data['articles'] contains a list of articles
                #thus for loop to iterate through each of the article
                for article in raw_data['articles']:

                    #upload each article's bytes representation to bucket in a blob
                    blob.upload_from_string(json.dumps(article))
                    #parse then insert in to the news table

                    #map1 allows it to convert to the ticker given company name.
                    ticker=map1[company]
                    title = article['title']
                    author = article['author']
                    url = article['url']
                    urlimage = article['urlToImage']
                    description = article['description']
                    date=article['publishedAt']

                    """
                    print(ticker)
                    print(title)
                    print(author)
                    print(url)
                    print(urlimage)
                    print(description)
                    print(date)
                    """

                    #print(article)
                    statement = """ INSERT INTO news(company_ticker, title, author, article_URL, url_image, article_description, date_published) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                    db_conn.execute(statement,(ticker,title,author,url,urlimage,description,date))
                    #sleep is needed, because it resulted in error 429 ratelimit exceeded
                    #only 1 modification/second is allowed, thus sleep for 1 second
                    #revisit if performance becomes an issue
                    time.sleep(1)
                # print(raw_data['articles'][0]['author'])
                # the json file where the output must be stored
                self.saveJson(raw_data, ticker=ticker,company=company,file_name_ending="_all_articles.json", )

        return



    # Helper func: save json/json
    def saveJson(self,raw_data,ticker,company,file_name_ending):
        # TODO: How to save when (time) query was made
        # TODO: Change hard code folder

        # Get home directory
        home = str(Path.home())+'/' # `/root/` for docker containers
        
        # Save as json file        
        company_no_space = str(company.replace(" ", "")) # Remove space in company name (for filename)
        out_filename = company_no_space + file_name_ending
        out_file = open(home + out_filename, "w")  
        json.dump(raw_data, out_file, indent = 6) 
        out_file.close() 

        #Send json file to kafka (Currently commented out)
        out_file = open(home + out_filename) 
        response=json.load(out_file)
        #print(response)
        
        ## TODO: DEBUG with for spending to kafka
        #responseloads = loads(str(raw_data))
        #print('rk', responseloads)
        #producer.send(TOPIC_NAME, responseloads)
        #producer.send(TOPIC_NAME, responseloads['articles'])
        out_file.close() 
        
        #######################################################################
        # Update request timestamp
        filename = 'last_request_date.json'
        last_request_date = self.get_last_request_date(filename)
        last_request_date[ticker]=time.time()        
        self.save_last_request_date(last_request_date,filename)
        
    def get_filepath(self, filename, root=None):
        if root == None:
            root = os.path.dirname(__file__)
        filepath = os.path.join(root,filename)
        
        return filepath

    def get_last_request_date(self,filename,root=None):
        filepath = self.get_filepath(filename,root=root)
        
        with open(filepath, 'r') as f:
            last_request_date = json.load(f)
        return last_request_date
    
    def save_last_request_date(self, last_request_date,filename, root=None):
        filepath = self.get_filepath(filename,root=root)
        
        with open(filepath, 'w') as f:
            json.dump(last_request_date, f)       
        
        
    # Helper func: add unique company identifier
    def addCompanyUniqueField(self, raw_data, companyName='', companyTicker=''):
        articles = raw_data["articles"]
        for article in articles:
            article["companyName"] = companyName
            article["companyTicker"] = companyTicker

        return articles

        # Helper func: Get previous time parameters
    def get_from_time(self,ticker):
        
        # Default to initalized value
        now = datetime.now()
        day = timedelta(days=1)
        prev_time = day            
        
        #month = datetime.timedelta(weeks=4)
        
        # First request
        filename = 'last_request_date.json'
        last_request_date = self.get_last_request_date(filename)
        if last_request_date[ticker] == 'None':
            return None
        
        #previous_timestamp = datetime.datetime.fromtimestamp(last_request_date_NEWSAPI)
        previous_timestamp=datetime.fromtimestamp(last_request_date[ticker])
        days_delta = now - previous_timestamp
        
        # more than than 1 month ago/4 weeks
        if 28 < days_delta.days :
            return None
        
        # Calc from last day request made within 1 month/4weeks
        num_prev_days_ago = days_delta.days*day            
        from_time = now - num_prev_days_ago
        
        from_time = from_time.replace(microsecond=0)
        return from_time.isoformat()


# Get articles
if __name__=="__main__":

    """
    newsArticles = NewsArticles(
        API_KEY_NEWSAPI, 
        companies,
        sources, 
        languages)
    """
#replaced company names to the one in companies file to use the map to ticker
    newsArticles = NewsArticles(
            API_KEY_NEWSAPI,
            top100,
            SOURCES,
            LANGUAGES)

    print(__file__)
    # newsArticles.get_everything()

    #print(companies)
    
    
