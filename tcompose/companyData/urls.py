from django.urls import path
from . import views


# URLConf
urlpatterns = [
    path('company/', views.getCompanyData)
]