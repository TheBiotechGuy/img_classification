from . import views
from django.urls import path

urlpatterns = [
    path('', views.BlogList, name='blog'),
]