from django.urls import path
from . import views

urlpatterns = [
    # path('', views.news_list),
    path('', views.scrape, name='scrape'),
    path('news/', views.viewing_news, name='news')
]
