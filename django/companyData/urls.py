from django.urls import path
from . import views


# URLConf
urlpatterns = [
    path('company/<str:company_ticker>/<str:days>/', views.getCompanyDataStr),
    path('company/<str:company_ticker>/<int:days>/', views.getCompanyDataStr),
    path('company/<str:company_ticker>/<int:days>/', views.getCompanyData),
    path('company/<str:company_ticker>/<str:days>', views.getCompanyDataStr),
    path('company/<str:company_ticker>/<int:days>', views.getCompanyData),
    path('company/<str:company_ticker>/', views.getCompanyData),
    path('company/<str:company_ticker>', views.getCompanyData),
    path('company/', views.listCompanies),
]