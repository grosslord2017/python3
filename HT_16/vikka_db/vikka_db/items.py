# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class VikkaDbItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    news_date = scrapy.Field()