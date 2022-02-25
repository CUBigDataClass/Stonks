from newsapi import NewsApiClient
from request_parameters import * 
import datetime
import json

from json import loads
from keys import * #?
import json

# from kafka import KafkaProducer
# import numpy as np
# import statistics as stats
# import requests
# from finviz.screener import Screener

class NewsArticles(NewsApiClient):
    # "Inherits from newsapi's NewsApiClient class. Adding functions to get our customized queries."
    # # Kafka definition
    # TOPIC_NAME = 'stock_data'
    # KAFKA_SERVER = 'localhost:9093'
    # producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def __init__(self,API_KEY, companies,domains, languages):
        self.newsapi = NewsApiClient(api_key=API_KEY)  # Open connection to newsapi API 
        self.companies = companies
        self.domains = domains
        self.languages = languages
        self.page = 1 # TODO: Change if more than 100 articles in 'totalResults'
        self.page_size = 100

    def get_everything(self):

        # Params
        # Query string of all companies we want to query
        q = self.get_query_string()

        # Error Check: Only from one month ago
        from_time = self.get_from_time()
        if self.test_get_time(from_time) == False:
            print('Query time error')
            return -1 # TODO: Change return of error  (Need? api does handle errors)
        print('from_time', from_time)

        # /v2/ All articles published AN HOUR AGO about some companies in english from Bloomberg (pg1)
        all_articles = self.newsapi.get_everything(
            q=str(q),        
            domains=str(self.domains),
            language=str(self.languages[0]),
            from_param=from_time,
            page=self.page,
            page_size=self.page_size)

        # the json file where the output must be stored 
        # TODO: How to save when (time) query was made
        out_file = open("articles.json", "a") 
        json.dump(all_articles, out_file, indent = 6) 
        out_file.close() 

    def get_top_headlines(self):
        # TODO
        return

    # Helper funcs
    def get_query_string(self):
        "Return a string with companies to query."
        q = ''
        for i in range(len(self.companies)):
            # If empty string add company name
            if len(q) == 0:
                q = str(self.companies[i])

            else:
                q = q+'OR'+str(self.companies[i])
        
        return q

    def get_from_time(self):
        # TODO: [prev_hr_call_error] Add in something that knows if previous hour(s) calls failed to also add those hours in this time
        now = datetime.datetime.now()

        # Get previous hour(s)/ [TODO] month ago
        hours = 1 # TODO: Change per [prev_hr_call_error] 
        previous_hour_time = int(now.hour) - hours
        
        # Change query time to hours(s)/ [TODO] month ago
        from_time = now.replace(hour=previous_hour_time, microsecond=0) # TODO: Change [year, month, day] per [prev_hr_call_error]
        
        return from_time.isoformat()


    def test_get_time(self, from_time):
        "Check if query time is valid for our plan (1 month ago)"
        month_ago = int(datetime.datetime.now().month) - 1
        month_ago_query = datetime.datetime.now().replace(month=month_ago,microsecond=0).isoformat()

        if month_ago_query <= from_time:
            return True
        else:
            return False


# Get articles
if __name__=="__main__":
    # # Kafka definition
    # TOPIC_NAME = 'stock_data'
    # KAFKA_SERVER = 'localhost:9093'
    # producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    newsArticles = NewsArticles(
        API_KEY, 
        companies,
        domains, 
        languages)

    newsArticles.get_everything()
    
    
