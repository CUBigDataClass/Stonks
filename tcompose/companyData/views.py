from django.shortcuts import render
from django.http import HttpResponse

# from .models import Companies, News, Stocks, Tweets
from .models import Companies, News, Stocks, Tweets

from datetime import datetime, timedelta
import json

## DEBUG imports #@todo: remove
from django.http import QueryDict

# Create your views here.
def getCompanyData(request):
    
    # Default display settings
    company_ticker = 'AAPL' # default ticker
    date_range = timedelta(days=7)
    to_date = datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0)
    from_date = to_date - date_range
    displayDict = {}
    
    get_request = request.GET # @todo: check if this is right 'get flag'
    # Company specificed
    if get_request.get('company_ticker') != None:
        company_ticker = get_request.get('company_ticker') # expecting ONE company ticker at a time
    company_name = Companies.objects.values_list('company_name', flat=True).get(pk=company_ticker)
    displayDict['company_name'] = company_name
    
    ## Dates
    if get_request.get('to_date') != None:
        to_date = get_request.get('to_date') # @todo: in UTC iso format?
        
    if get_request.get('from_date') != None:
        from_date = get_request.get('from_date') # @todo: in UTC iso format?
        
    if get_request.get('date_range') != None:
        date_range = timedelta(days=7)
        from_date = to_date - date_range
        
    # Get filtered data    
    query_set = Stocks.objects.filter(pk=company_ticker).filter(date__range=(from_date,to_date))
    displayDict['stocks'] = list(query_set)
    
    query_set = News.objects.filter(pk=company_ticker).filter(date_published__range=(from_date,to_date))
    displayDict['news'] = list()

    ##@todo: how to get DAILY sentiment (not individual tweets)    
    # query_set = Tweets.objects.filter(company_ticker__contains=company_ticker).filter(date_published__range=(from_date,to_date))
    # displayDict['news'] = list(query_set)
    
    # ##@todo: Make into JSON
    # { date1: [
    #     open:_, 
    #     close:_,
    #     news: [
    #         Article: [
    #             title:_,
    #             image:_,
    #             description:_                
    #         ]
    #     ],
    #     date2:....
    # ]}

    return render(request, 'company.html', displayDict)
