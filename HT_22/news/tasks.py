import requests
from .models import JobStories, NewStories, AskStories, ShowStories
from app.celery import celery_app

@celery_app.task(name='news.start_scrap', queue='news')
def start_scrap(category):
    articles = ScrapeArticles(category)
    articles.start_program()

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
        for submission_id in list_ids:

            exam = self.examination(submission_id)

            if not exam:
                url = f'{self.url}item/{submission_id}.json'
                submission_r = requests.get(url)
                response_dict = submission_r.json()
                if response_dict != None:
                    self.writer_to_db(response_dict)
            else:
                continue

    def writer_to_db(self, rl):
        if self.category == 'jobstories':
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
                return NewStories.objects.get(id_news=submission_id)
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