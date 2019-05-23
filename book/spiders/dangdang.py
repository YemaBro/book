# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_splash import SplashRequest
from book.items import DangDangTest


class DangdangSpider(scrapy.Spider):
    name = 'dangbook'
    allowed_domains = ['dangdang.com']
    base_url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2018-0-1-'

    def start_requests(self):
        for page in range(1, 26):
            url = self.base_url + str(page)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        books = response.css('.bang_list_box ul li')
        for book in books:
            item = DangDangTest()
            item['rank'] = int(book.css('.list_num::text').extract_first().strip('.'))
            item['title'] = book.css('.name a::text').extract_first()
            item['author'] = book.css('div:nth-child(5) a::text').extract_first()
            item['pub'] = book.css('div:nth-child(6) a::text').extract_first()
            item['price'] = book.css('.price .price_n::text').extract_first()
            item['sell_url'] = book.css('.name a::attr(href)').extract_first()
            yield SplashRequest(url=item['sell_url'],
                                callback=self.parse_content,
                                dont_filter=True,
                                meta={'item': item},
                                args={'wait': 2},
                                encoding='utf-8')

    def parse_content(self, response):
        pattern = re.compile(r'<[^>]+>', re.S)
        item = response.meta.get('item')
        content = response.xpath("//div[@id='detail']/div[@id='content']/div[@class='descrip']").extract_first()
        item['content'] = pattern.sub('', content)
        yield item
