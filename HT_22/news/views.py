from celery.result import AsyncResult
from django.shortcuts import render
from .models import JobStories, NewStories, AskStories, ShowStories
from news.tasks import start_scrap


# Create your views here.

def news_list(request):
    return render(request, 'news/news_choice.html')

def scrape(request):
    if request.method == 'POST':
        category = request.POST.get('news_category')
        result = start_scrap.delay(category)
        print(result.id)
        print(result)
    return render(request, 'news/news_choice.html')

def viewing_news(request):
    category = request.POST.get('news')
    all_news_in_category = None

    if category == 'jobstories':
        all_news_in_category = JobStories.objects.all()
    elif category == 'newstories':
        all_news_in_category = NewStories.objects.all()
    elif category == 'showstories':
        all_news_in_category = ShowStories.objects.all()
    elif category == 'askstories':
        all_news_in_category = AskStories.objects.all()
    return render(request, 'news/info.html', {'category': category, 'news_category': all_news_in_category})
