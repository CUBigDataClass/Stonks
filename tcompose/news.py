from newsapi import NewsApiClient
from request_parameters import * 
from keys import *
from last_request_date import *

from datetime import datetime, timedelta
import time
from json import dumps
from json import loads
from kafka import KafkaProducer
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

    def get_everything(self):
        from_time = self.get_from_time()

        # Loop through specificied companies
        for i in range(len(self.companies)):
            company = str(self.companies[i])          
            
            # /v2/ All articles published some time ago of company
            raw_data = self.newsapi.get_everything(
                q=company,        
                sources=self.sources,
                language=self.languages[0],
                from_param=from_time,
                page=self.page,
                page_size=self.page_size)            
            
            # the json file where the output must be stored
            self.saveJson(raw_data,companyName=company,companyTicker='')
        return

    # Helper func: save json/json
    def saveJson(self,raw_data,companyName='',companyTicker=''):
        # Add company field in raw_data["articles"] json 
        articles = self.addCompanyUniqueField(raw_data,companyName,companyTicker)
        #print("articles:",articles)
        for article in articles:
            response=loads(json.dumps(article))
            producer.send(TOPIC_NAME, response["content"])
            # print("article:",article)
            producer.flush()
        
        #######################################################################
        # Update request timestamp
        out_filename = 'last_request_date.py'
        # Get home directory
        home = str(Path.home())+'/' # `/root/` for docker containers
        out_file = open(home + out_filename, "w")
        ## - Save varable (source:https://www.pythonpool.com/python-save-variable-to-file/)
        out_file.write("%s = %f\n" %("last_request_date_NEWSAPI", time.time()))
        out_file.close()
        
    #Helper func: add unique company identifier
    def addCompanyUniqueField(self, raw_data,companyName='', companyTicker=''):
        articles = raw_data["articles"]
        for article in articles:
            article["companyName"]=companyName
            article["companyTicker"]=companyTicker

        return articles   
    
    # Helper func: Get previous time parameters
    def get_from_time(self):
        
        # Default to initalized value
        now = datetime.now()
        day = timedelta(days=1)
        prev_time = day            
        
        #month = datetime.timedelta(weeks=4)
        
        # First request
        if last_request_date_NEWSAPI is None:
            return None
        
        #previous_timestamp = datetime.datetime.fromtimestamp(last_request_date_NEWSAPI)
        previous_timestamp=datetime.fromtimestamp(last_request_date_NEWSAPI)
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
if __name__ == "__main__":
    print('init news.py')
    TOPIC_NAME = 'news'
    KAFKA_SERVER = 'kafka-1:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v:dumps(v).encode('utf-8'))

    newsArticles = NewsArticles(
        API_KEY_NEWSAPI, 
        companies,
        sources, 
        languages)

    newsArticles.get_everything()
    print('news.py done')
    producer.flush
    print('end news.py')