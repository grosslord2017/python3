'''Використовуючи бібліотеку requests написати скрейпер для отримання статей / записів із АПІ
Документація на АПІ:
https://github.com/HackerNews/API
Скрипт повинен отримувати із командного рядка одну із наступних категорій:
askstories, showstories, newstories, jobstories
Якщо жодної категорії не указано - використовувати newstories.
Якщо категорія не входить в список - вивести попередження про це і завершити роботу.
Результати роботи зберегти в CSV файл. Зберігати всі доступні поля. Зверніть увагу - інстанси різних типів мають різний набір полів.
Код повинен притримуватися стандарту pep8.
Перевірити свій код можна з допомогою ресурсу http://pep8online.com/
Для тих, кому хочеться зробити щось "додаткове" - можете зробити наступне: другим параметром cкрипт може приймати
назву HTML тега і за допомогою регулярного виразу видаляти цей тег разом із усим його вмістом із значення атрибута "text"
(якщо він існує) отриманого запису.'''


import csv
import json
import sys

import requests
from pprint import pprint


class BadInput(Exception):
    def __init__(self, msg):
        self.msg = msg


class ScrapeArticles(object):

    def __init__(self, category):
        self.category = self.choice_category(category)
        self.url = 'https://hacker-news.firebaseio.com/v0/'

    def start_program(self):
        list_ids = self.getting_list_ids()
        self.receiving_articles(list_ids)

    def choice_category(self, category):
        if category in ['askstories', 'showstories', 'newstories', 'jobstories']:
            return category
        elif category == '':
            return 'newstories'
        else:
            raise BadInput('No such category!')

    def getting_list_ids(self):
        url = self.url + f'{self.category}.json'
        r = requests.get(url)
        submission_ids = r.json()
        return submission_ids

    def receiving_articles(self, list_ids):
        response_list = []
        for submission_id in list_ids:
            url = f'{self.url}item/{submission_id}.json'
            submission_r = requests.get(url)
            response_dict = submission_r.json()
            response_list.append(response_dict)
        self.writer_to_csv(response_list)

    def writer_to_csv(self, response_list):
        with open(f'{self.category}.csv', "w", encoding='UTF-8', newline='') as file:
            writer = csv.DictWriter(file, restval='', extrasaction='ignore',
                                    fieldnames=['by', 'descendants', 'id', 'kids', 'score',
                                                'text', 'time', 'title', 'type', 'url'], delimiter=';')
            writer.writeheader()
            writer.writerows(response_list)

if __name__ == '__main__':
    category = sys.argv[1]
    articles = ScrapeArticles(category)
    articles.start_program()
