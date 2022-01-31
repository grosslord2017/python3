from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list),
    path('scrape/', views.scrape)
]
