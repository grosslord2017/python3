# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import sqlite3
from pathlib import Path
from datetime import datetime



# class VikkaDbPipeline:
#     def process_item(self, item, spider):
#         return item


class VikkaDbPipeline(object):
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS news (
    #         id integer NOT NULL PRIMARY KEY,
    #         title text NOT NULL,
    #         text_news text NOT NULL,
    #         tags text NOT NULL,
    #         url text NOT NULL
    #     );''')

    # at startup
    def open_spider(self, spider):
        # self.cursor.execute('''
        #         CREATE TABLE IF NOT EXISTS news (
        #             id integer NOT NULL PRIMARY KEY,
        #             title text NOT NULL,
        #             text_news text NOT NULL,
        #             tags text NOT NULL,
        #             url text NOT NULL
        #         );''')

    # at finish spider work
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                date text NOT NULL,
                title text NOT NULL,
                text_news text NOT NULL,
                tags text NOT NULL,
                url text NOT NULL
        );''')


    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        news = [item['news_date'], item['title'], item['text'], item['tags'], item['url']]
        url = self.cursor.execute("SELECT date, url FROM news").fetchall()
        # for i in url:
        #     print('=' * 50)
        #     print(i)
        #     print('=' * 50)
        if (news[0], news[4]) not in url:
            self.cursor.execute("INSERT INTO news (date, title, text_news, tags, url) VALUES (?, ?, ?, ?, ?);", news)
        return item

    # def repeat_check(self, item):
    #     # rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
    #     check = self.cursor.execute("SELECT date, url FROM news").fetchall()
    #     if [item['news_date'], item['url']] not in check:
    #         self.cursor.execute("INSERT INTO news (date, title, text_news, tags, url) VALUES (?, ?, ?, ?, ?);", news)


