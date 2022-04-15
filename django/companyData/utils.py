import csv 
## DEBUG imports #@todo: remove
from django.http import QueryDict
from django.shortcuts import render
from django.http import HttpResponse

import zipfile
# from io import StringIO 
import io

from .models import *

header_stocks = ['date', 'company_ticker', 'open', 'high', 'low', 'close']

header_tweets = [
    'date_published',
    'sentiment', 
]

header_news = [
    'date_published',
    'title', 
    'author',
    'article_url',
    'url_image',
    'article_description'
]

headers = header_stocks + header_tweets + header_news

def write_helper_fn(header, displayDict, key,filename='csv_file.csv', writer=None):
       
    
    csv_file = open(key+filename, 'w')

    writer = csv.writer(csv_file)
    writer.writerow(header)
       
    for value in displayDict[key]:
        writer.writerow(list(value.values()))
    return writer

# TODO or JSON: https://docs.djangoproject.com/en/4.0/ref/request-response/#jsonresponse-objects
# # https://docs.djangoproject.com/en/4.0/howto/outputting-csv/
def csv_helper_fn(request,displayDict, filename='csv_file.csv'):

    # stocks 
    # writer_stocks = csv.writer(response)   
    writer_stocks = write_helper_fn(header_stocks, displayDict, 'stocks')
    
    # # twitters
    writer_twitters = write_helper_fn(header_tweets, displayDict, 'tweets')    
    
    # # news
    writer_news = write_helper_fn(header_news, displayDict, 'news')

    #################
    
    header_response = header_stocks
    key_response = 'stocks'
    
    header_response = header_tweets
    key_response = 'tweets'
    
    header_response = header_news
    key_response = 'news'
    
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename='+filename}
    )
    writer_response = csv.writer(response)
    writer_response.writerow(header_response)
       
    for value in displayDict[key_response]:
        writer_response.writerow(list(value.values()))
    
    # return render(request, 'company.html', displayDict)
    return response

# # TODO remove 
# def csv_helper_fn(request, displayDict,filename='csv_file.csv'):
#     response = HttpResponse(
#         content_type='text/csv',
#         headers={'Content-Disposition': 'attachment; filename='+filename},
#     )
    
#     writer = csv.writer(response)
#     writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
#     writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    
#     return response