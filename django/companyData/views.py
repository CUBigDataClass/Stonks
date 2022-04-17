import csv
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core import serializers

# from django.

# from .models import Companies, News, Stocks, Tweets
# from .models import Companies, News, Stocks, Tweets
from .models import *
from .utils import *

from datetime import datetime, timedelta
import json


# DEBUG imports #@todo: remove
from django.http import QueryDict

# Create your views here.


def getStock(request, company_ticker='AAPL', days=365,fields=['open', 'close','low','high']):
    date_range = timedelta(days=days)
    to_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    from_date = to_date - date_range
    
    # # Get filtered data
    
    # https://d3-graph-gallery.com/graph/dendrogram_basic.html
    # https://d3-graph-gallery.com/graph/treemap_json.html
    # https://stackoverflow.com/questions/15874233/output-django-queryset-as-json
    data ={}
    data['date'] = list( Stocks.objects.filter(pk=company_ticker).filter(date__range=(from_date, to_date)).values_list('date',flat=True))
    
    for field in fields:
        data[field] = list( Stocks.objects.filter(pk=company_ticker).filter(date__range=(from_date, to_date)).values_list(field,flat=True))
    
    return JsonResponse({'stock': data})

def getNews(request, company_ticker='AAPL', days=365):
    date_range = timedelta(days=days)
    to_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    from_date = to_date - date_range
    
    # # Get filtered data

    query_set = News.objects.filter(company_ticker__contains=company_ticker).filter(date_published__range=(from_date, to_date)).order_by(
        '-date_published').values('date_published', 'title', 'author', 'article_url', 'url_image', 'article_description', 'company_ticker')

    # data = {}
    # fields = ['date_published', 'title', 'author', 'article_url', 'url_image', 'article_description', 'company_ticker']
    # for field in fields:
    #     query_set = News.objects.filter(company_ticker__contains=company_ticker).filter(date_published__range=(from_date, to_date)).order_by('-date_published').values_list(field, flat=True)
    #     data[field] = list( ewNs.objects.filter(company_ticker__contains=company_ticker).filter(date__range=(from_date, to_date)).values_list(field,flat=True))
    

    num_articles_ret = 5
    list1 = list(query_set)
    data = list1[0:num_articles_ret]
    
    return JsonResponse({'news': data})

def getTweets(request, company_ticker='AAPL', days=365):
    date_range = timedelta(days=days)
    to_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    from_date = to_date - date_range
    
    query_set = Tweets.objects.filter(company_ticker__contains=company_ticker).filter(
        date_published__range=(from_date, to_date)).values('date_published', 'sentiment','compound_score')
    data = getSentiment(query_set)
    return JsonResponse({'tweets': data})
    # return JsonResponse(data, save=False)
    
def getCompanyInfo(request, company_ticker='AAPL'):

    data = list(Companies.objects.filter(company_ticker__contains=company_ticker).values())
    return JsonResponse({'company_info': data})

    

    

# (OLD) query string: url = 'http://127.0.0.1:8000/companyData/company/TICKER?q=7' ## where q=7,14,31
# (NEW TO USE): query string:
# url = 'http://127.0.0.1:8000/companyData/company/TICKER/7'
# url = 'http://127.0.0.1:8000/companyData/company/TICKER/14'
# url = 'http://127.0.0.1:8000/companyData/company/TICKER/365'

def getCompanyDataStr(request, company_ticker='AAPL', days='365'):
    days = int(days)
    return getCompanyData(request, company_ticker, days)


def getCompanyData(request, company_ticker='AAPL', days=365):
    date_range = timedelta(days=days)
    to_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    from_date = to_date - date_range
    
    displayDict = {}
    resType = list

    # Company specificed
    company = Companies.objects.filter(company_ticker__contains=company_ticker).values()

    displayDict['company_info'] = resType(company)

    # Get filtered data

    # query_set = Stocks.objects.filter(pk=company_ticker).filter(date__range=(from_date,to_date)).values(values)
    query_set = Stocks.objects.filter(pk=company_ticker).filter(date__range=(from_date, to_date)).values('date',
                                                                                                         'company_ticker',
                                                                                                         'open',
                                                                                                         'high',
                                                                                                         'low',
                                                                                                         'close',)
    displayDict['stocks'] = resType(query_set)

    query_set = Tweets.objects.filter(company_ticker__contains=company_ticker).filter(
        date_published__range=(from_date, to_date)).values('date_published', 'sentiment','compound_score')
    displayDict['tweets'] = getSentiment(query_set)

    query_set = News.objects.filter(company_ticker__contains=company_ticker).filter(date_published__range=(from_date, to_date)).order_by(
        '-date_published').values('date_published', 'title', 'author', 'article_url', 'url_image', 'article_description', 'company_ticker')

    num_articles_ret = 5
    list1 = list(query_set)
    list2 = list1[0:num_articles_ret]
    displayDict['news'] = list2

    return JsonResponse(displayDict)


from django.urls import reverse
def listCompanies(request):
    companies = {}

    # company_names = list(Companies.objects.values_list('company_name', flat=True).get(pk=company_ticker))
    company_tickers = list(Companies.objects.values_list('company_ticker', flat=True))
    
    # from django.urls import include, path
    
    # print(path())
    # url = 'http://127.0.0.1:8000/companyData/company/' ## Can change
    # url = request.build_absolute_uri()
    
    # from django.core.urlresolvers import reverse
    # print(reverse('stocks-default'), args(company_tickers[c]))
    # url = reverse('companyData.view.listCompanies')

    url = 'http://'+ request.META['HTTP_HOST']
    
    for c in range(len(company_tickers)):
        url = url + reverse('stocks-default', args=(company_tickers[c],365))
        companies[company_tickers[c]] = url
    return JsonResponse(companies)


def getSentiment(query_set):
    t = list(query_set)
    val = 0
    pos_count = 0
    n_count = 0
    ne_count = 0
    for x in t:
        if x['sentiment'] > 0:
            pos_count += 1
        elif x['sentiment'] == 0:
            n_count += 1
        elif x['sentiment'] < 0:
            ne_count += 1

    psenti = pos_count/len(t)
    nsenti = n_count/len(t)
    nesenti = ne_count/len(t)

    # list1=[psenti,nsenti,nesenti]

    dict1 = {'positive': psenti, 'neutral': nsenti, 'negative': nesenti}

    return dict1
