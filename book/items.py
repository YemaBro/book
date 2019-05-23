# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class BookJDTest(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    pub = scrapy.Field()
    sell_url = scrapy.Field()
    book_info = scrapy.Field()
    recommend = scrapy.Field()


class BooksChinaTest(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    pub = scrapy.Field()
    sell_url = scrapy.Field()
    specialist = scrapy.Field()
    brief = scrapy.Field()


class DangDangTest(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    pub = scrapy.Field()
    sell_url = scrapy.Field()
    abstract = scrapy.Field()
    content = scrapy.Field()
