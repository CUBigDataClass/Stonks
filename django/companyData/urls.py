from django.urls import path,include
from . import views

# https://docs.djangoproject.com/en/4.0/topics/http/urls/
# # URLConf
urlpatterns = [
    path('<str:company_ticker>/<int:days>/', include([
        path('stock/open/', views.getStock, {'fields':['open']}),
        path('stock/close/', views.getStock, {'fields':['close']}),
        path('stock/low/', views.getStock, {'fields':['low']}),
        path('stock/high/', views.getStock, {'fields':['high']}),
        path('stock/', views.getStock),
        path('news/', views.getNews),
        path('tweets/',views.getTweets),
        path('companyInfo/', views.getCompanyInfo),
        ])),
    path('company/', views.listCompanies),
]


# urlpatterns = [
#     path('company/<str:company_ticker>/<int:days>/stock/open/', views.getStockOpen),
#     # path('company/<str:company_ticker>/<int:days>/stock/close/', views.getStockClose),
#     # path('company/<str:company_ticker>/<int:days>/stock/high/', views.getStockHigh),
#     # path('company/<str:company_ticker>/<int:days>/stock/low/', views.getStockLow),
#     # path('company/<str:company_ticker>/<int:days>/', views.getCompanyData),
#     # path('company/<str:company_ticker>/<int:days>', views.getCompanyData),
#     # path('company/<str:company_ticker>/<str:days>', views.getCompanyDataStr),
#     # path('company/<str:company_ticker>/<str:days>/', views.getCompanyDataStr),
#     # path('company/<str:company_ticker>/<str:days>', views.getCompanyDataStr),
#     # path('company/<str:company_ticker>/<int:days>/', views.getCompanyData),
#     # path('company/<str:company_ticker>/<int:days>', views.getCompanyData),
#     path('company/<str:company_ticker>/', views.getCompanyData),
#     path('company/<str:company_ticker>', views.getCompanyData),
#     path('company/', views.listCompanies),
# ]