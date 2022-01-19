import os
import csv
import scrapy
import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from vikka_db.items import NewsItem

class BadDate(Exception):
    def __init__(self, msg):
        self.msg = msg

class BadInput(Exception):
    def __init__(self, msg):
        self.msg = msg

class VikkatoscrapeSpider(scrapy.Spider):
    name = 'vikka2'
    allowed_domains = ['vikka.ua']
    start_urls = ['https://vikka.ua/']
    user_date = None
    save_path = Path(__file__).parent.parent / 'news'

    def start_requests(self):
        self.user_date = input('enter date in format YYYY/MM/DD:' )
        self.check_correct_input()
        print('-' * 50)
        # yield Date(self.user_date)
        start_url = f'{self.start_urls[0]}{self.user_date}/'
        yield scrapy.Request(url=start_url, callback=self.parse_vikka_page)

    def parse_vikka_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        for news in soup.select('ul.cat-posts-wrap li.item-cat-post'):
            news_link = self.all_news_link(news) # pars first page and return link to news
            yield scrapy.Request(url=news_link, callback=self.parse_url_page)

        try:
            button_url = soup.select_one('.nav-links a.next').get('href')
            if button_url is not None:
                yield scrapy.Request(url=button_url, callback=self.parse_vikka_page)
        except:
            pass


    # collect all news in selected day
    def all_news_link(self, news_soup):
        return news_soup.select_one('div.justify-content-start > a').get('href')

    # pars every news
    def parse_url_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = NewsItem()
        item['title'] = soup.select_one('div .post-container .post-title').text
        item['text'] = soup.select_one('div .post-container .entry-content').text
        item['tags'] = self.page_tags(soup)
        item['url'] = str(response).split(' ')[1].rstrip('>')
        item['news_date'] = self.user_date
        return item

    # format in correct tags
    def page_tags(self, page_news):
        temp = page_news.select('div .post-container .entry-tags .post-tag')
        t = []
        for teg in temp:
            t.append(f'#{teg.text}')
        result_temp = ' '.join(t)
        return result_temp

    def check_date(self):
        format = datetime.datetime.strptime(self.user_date, '%Y/%m/%d')
        now = datetime.datetime.now()
        if format > now:
            raise BadDate('the date is not yet!')

    def check_correct_input(self):
        try:
            self.user_date.split('/')
            self.check_date()
        except:
            raise BadInput('date entered incorrectly')

