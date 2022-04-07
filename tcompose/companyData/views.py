from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def getCompanyData(request):
    # return HttpResponse('hello Word')
    displayDict = {'company_name': 'Microsoft'}
    return render(request, 'company.html', displayDict)
