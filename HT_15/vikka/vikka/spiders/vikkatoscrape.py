import os
import csv
import scrapy
import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from vikka.items import NewsItem

class BadDate(Exception):
    def __init__(self, msg):
        self.msg = msg

class BadInput(Exception):
    def __init__(self, msg):
        self.msg = msg

class VikkatoscrapeSpider(scrapy.Spider):
    name = 'vikkatoscrape'
    allowed_domains = ['vikka.ua']
    start_urls = ['https://vikka.ua/']
    user_date = None
    save_path = Path(__file__).parent.parent / 'news'
    news_link = None
    # start_url = None

    def start_requests(self):
        self.user_date = input('enter date in format YYYY/MM/DD:' )
        self.check_correct_input()
        self.remove_duplicate()
        print('-' * 50)
        start_url = f'{self.start_urls[0]}{self.user_date}/'
        yield scrapy.Request(url=start_url, callback=self.parse_vikka_page)

    def parse_vikka_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        for news in soup.select('ul.cat-posts-wrap li.item-cat-post'):
            self.news_link = self.all_news_link(news) # pars first page and return link to news
            # if self.news_link:
            #     yield scrapy.Request(url=self.news_link, callback=self.parse_url_page)
            yield scrapy.Request(url=self.news_link, callback=self.parse_url_page)
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
        item['url'] = self.news_link
        self.writer_item(item)
        # button = soup.select_one('.nav-links .next').get('href')
        return item

    # format in correct tags
    def page_tags(self, page_news):
        temp = page_news.select('div .post-container .entry-tags .post-tag')
        t = []
        for teg in temp:
            t.append(f'#{teg.text}')
        result_temp = ' '.join(t)
        return result_temp

    # block for write in to csv file.
    def writer_item(self, item):
        outpath_tmp = Path(self.save_path) / f'{self.name_file(self.user_date)}.csv'

        if not Path.is_dir(self.save_path):
            Path.mkdir(self.save_path)

        with open(outpath_tmp, 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            news = [item['title'], item['text'], item['tags'], item['url']]
            writer.writerow(news)

    # formating correct filename
    def name_file(self, date_user):
        date_user = date_user.split('/')
        new_date = '_'.join(date_user)
        return new_date

    # if such a date has already been requested, delete file with this date
    def remove_duplicate(self):
        check_file = f"{self.save_path}/{self.name_file(self.user_date)}.csv"
        if os.path.isfile(check_file):
            os.remove(check_file)

    # check actual date
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

