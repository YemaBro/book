# -*- coding: utf-8 -*-
import re
import scrapy
from book.items import BooksChinaTest


class BookschinaSpider(scrapy.Spider):
    name = 'bookschina'
    allowed_domains = ['bookschina.com']
    base_url = 'http://www.bookschina.com/24hour/30_0_'

    def start_requests(self):
        for page in range(1, 35):
            url = self.base_url + str(page) + '/'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        books = response.css('.bookList ul li')
        for book in books:
            item = BooksChinaTest()
            item['rank'] = int(book.css('.num span::text').extract_first())
            item['title'] = book.css('.infor .name a::text').extract_first()
            item['author'] = book.css('.infor .author a::text').extract_first()
            item['price'] = book.css('.infor .priceWrap .sellPrice::text').extract_first()
            item['pub'] = book.css('.infor .publisher a::text').extract_first()
            item['sell_url'] = 'http://www.bookschina.com' + book.css('.infor .name a::attr(href)').extract_first()
            yield scrapy.Request(url=item['sell_url'],
                                 callback=self.parse_content,
                                 dont_filter=True,
                                 meta={'item': item})

    def parse_content(self, response):
        item = response.meta.get('item')
        item['specialist'] = ''.join(response.css('#specialist p::text').extract())
        item['brief'] = ''.join(response.css('#brief p::text').extract())
        yield item
