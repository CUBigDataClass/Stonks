from newsapi import NewsApiClient
from request_parameters import * 
from keys import *
from last_request_date import *
import os
from google.cloud import storage
from datetime import datetime, timedelta
import time
from companies import *
from db_keys import *
from postGres import *
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

                #raw_data['articles'] contains a list of articles
                #thus for loop to iterate through each of the article
                for article in raw_data['articles']:
                    #upload each article's bytes representation to bucket in a blob
                    blob.upload_from_string(json.dumps(article))
                    #parse then insert in to the news table
                    url=article['url']
                    #map1 allows it to convert to the ticker given company name.
                    ticker=map1[company]
                    date=article['publishedAt']
                    content=article['content']
                    statement = """ INSERT INTO news(company_ticker, article_URL, article_content,date_published) VALUES (%s,%s,%s,%s)"""
                    db_conn.execute(statement,(ticker,url,content,date))
                    #sleep is needed, because it resulted in error 429 ratelimit exceeded
                    #only 1 modification/second is allowed, thus sleep for 1 second
                    #revisit if performance becomes an issue
                    time.sleep(1)
                # print(raw_data['articles'][0]['author'])
                # the json file where the output must be stored
                self.saveJson(raw_data, company=company,file_name_ending="_all_articles.json", )

        return



    # Helper func: save json/json
    def saveJson(self,raw_data,company,file_name_ending):
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
        out_filename = 'last_request_date.py'
        out_file = open(home + out_filename, "w")  
        
        ## - Save varable (source:https://www.pythonpool.com/python-save-variable-to-file/)
        out_file.write("%s = %f\n" %("last_request_date_NEWSAPI", time.time()))
        out_file.close()
        
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
if __name__=="__main__":

    newsArticles = NewsArticles(
        API_KEY_NEWSAPI, 
        companies,
        sources, 
        languages)

    newsArticles.get_everything()

    #print(companies)
    
    
