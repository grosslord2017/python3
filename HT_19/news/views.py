from django.shortcuts import render
from django.http import HttpResponse
import time
import requests
from .models import JobStories, NewStories, AskStories, ShowStories


# Create your views here.

def news_list(request):
    return render(request, 'news/news_choice.html')

def scrape(request):
    if request.method == 'POST':
        category = request.POST.get('news_category')
        articles = ScrapeArticles(category)
        articles.start_program()

        return render(request, 'news/info.html', {'category': category})


class ScrapeArticles(object):

    def __init__(self, category):
        self.url = 'https://hacker-news.firebaseio.com/v0/'
        self.category = category

    def start_program(self):
        list_ids = self.getting_list_ids()
        self.receiving_articles(list_ids)

    def getting_list_ids(self):
        url = self.url + f'{self.category}.json'
        r = requests.get(url)
        submission_ids = r.json()
        return submission_ids

    def receiving_articles(self, list_ids):
        response_list = []
        for submission_id in list_ids:

            exam = self.examination(submission_id)

            if exam == False:
                url = f'{self.url}item/{submission_id}.json'
                submission_r = requests.get(url)
                response_dict = submission_r.json()
                if response_dict != None:
                    response_list.append(response_dict)
            else:
                continue
        self.writer_to_db(response_list)

    def writer_to_db(self, response_list):
        if self.category == 'jobstories':
            for rl in response_list:
                obj = JobStories.objects.create(
                    by=rl.get('by', ''),
                    id_news=rl['id'],
                    score=rl.get('score', ''),
                    title=rl.get('title', ''),
                    text=rl.get('text', ''),
                    time=rl.get('time', ''),
                    type=rl.get('type', ''),
                    url=rl.get('url', '')
                    )
                obj.save()
        elif self.category == 'newstories':
            for rl in response_list:
                obj = NewStories.objects.create(
                    by=rl.get('by', ''),
                    descendants=rl.get('descendants', ''),
                    id_news=rl['id'],
                    kids=rl.get('kids', ''),
                    score=rl.get('score', ''),
                    title=rl.get('title', ''),
                    text=rl.get('text', ''),
                    time=rl.get('time', ''),
                    type=rl.get('type', ''),
                    url=rl.get('url', ''),
                    )
                obj.save()
        elif self.category == 'askstories':
            for rl in response_list:
                obj = AskStories.objects.create(
                    by=rl.get('by', ''),
                    descendants=rl.get('descendants', ''),
                    id_news=rl['id'],
                    kids=rl.get('kids', ''),
                    score=rl.get('score', ''),
                    title=rl.get('title', ''),
                    text=rl.get('text', ''),
                    time=rl.get('time', ''),
                    type=rl.get('type', ''),
                    )
                obj.save()
        elif self.category == 'showstories':
            for rl in response_list:
                obj = ShowStories.objects.create(
                    by=rl.get('by', ''),
                    descendants=rl.get('descendants', ''),
                    id_news=rl['id'],
                    kids=rl.get('kids', ''),
                    score=rl.get('score', ''),
                    title=rl.get('title', ''),
                    text=rl.get('text', ''),
                    time=rl.get('time', ''),
                    type=rl.get('type', ''),
                    url=rl.get('url', ''),
                    )
                obj.save()

    def examination(self, submission_id):
        if self.category == 'jobstories':
            try:
                return JobStories.objects.get(id_news=submission_id)
            except:
                return False
        elif self.category == 'newstories':
            try:
                NewStories.objects.get(id_news=submission_id)
                return True
            except:
                return False
        elif self.category == 'askstories':
            try:
                return AskStories.objects.get(id_news=submission_id)
            except:
                return False
        elif self.category == 'showstories':
            try:
                return ShowStories.objects.get(id_news=submission_id)
            except:
                return False

    # def writer_to_db(self, response_list):
    #     if self.category == 'jobstories':
    #         print(len(response_list))
    #         for rl in response_list:
    #             try:
    #                 examination = JobStories.objects.get(id_news=rl['id'])
    #             except:
    #                 obj = JobStories.objects.create(
    #                     by=rl.get('by', ''),
    #                     id_news=rl['id'],
    #                     score=rl.get('score', ''),
    #                     title=rl.get('title', ''),
    #                     text=rl.get('text', ''),
    #                     time=rl.get('time', ''),
    #                     type=rl.get('type', ''),
    #                     url=rl.get('url', '')
    #                     )
    #                 obj.save()
    #
    #     elif self.category == 'newstories':
    #         print(len(response_list))
    #         for rl in response_list:
    #             try:
    #                 NewStories.objects.get(id_news=rl['id'])
    #             except:
    #                 obj = NewStories.objects.create(
    #                     by=rl.get('by', ''),
    #                     descendants=rl.get('descendants', ''),
    #                     id_news=rl['id'],
    #                     kids=rl.get('kids', ''),
    #                     score=rl.get('score', ''),
    #                     title=rl.get('title', ''),
    #                     text=rl.get('text', ''),
    #                     time=rl.get('time', ''),
    #                     type=rl.get('type', ''),
    #                     url=rl.get('url', ''),
    #                     )
    #                 obj.save()
    #
    #     elif self.category == 'askstories':
    #         print(len(response_list))
    #         for rl in response_list:
    #             try:
    #                 examination = AskStories.objects.get(id_news=rl['id'])
    #             except:
    #                 obj = AskStories.objects.create(
    #                     by=rl.get('by', ''),
    #                     descendants=rl.get('descendants', ''),
    #                     id_news=rl['id'],
    #                     kids=rl.get('kids', ''),
    #                     score=rl.get('score', ''),
    #                     title=rl.get('title', ''),
    #                     text=rl.get('text', ''),
    #                     time=rl.get('time', ''),
    #                     type=rl.get('type', ''),
    #                     )
    #                 obj.save()
    #
    #     elif self.category == 'showstories':
    #         print(len(response_list))
    #         for rl in response_list:
    #             try:
    #                 examination = ShowStories.objects.get(id_news=rl['id'])
    #             except:
    #                 obj = ShowStories.objects.create(
    #                     by=rl.get('by', ''),
    #                     descendants=rl.get('descendants', ''),
    #                     id_news=rl['id'],
    #                     kids=rl.get('kids', ''),
    #                     score=rl.get('score', ''),
    #                     title=rl.get('title', ''),
    #                     text=rl.get('text', ''),
    #                     time=rl.get('time', ''),
    #                     type=rl.get('type', ''),
    #                     url=rl.get('url', ''),
    #                 )
    #                 obj.save()



