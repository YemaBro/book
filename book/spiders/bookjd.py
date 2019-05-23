# -*- coding: utf-8 -*-
import json
import scrapy
import re
from book.items import BookJDTest
from scrapy_splash import SplashRequest


class BookjdSpider(scrapy.Spider):
    name = 'bookjd'
    allowed_domains = ['book.jd.com']
    base_url = 'https://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10005-'
    price_url = 'https://p.3.cn/prices/mgets?type=1&skuIds={book_price_id}'

    def start_requests(self):
        for page in range(1, 6):
            url = self.base_url + str(page)
            yield scrapy.Request(url=url, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        books = response.css('.mc ul li')
        for book in books:
            item = BookJDTest()
            item['rank'] = int(book.css('.p-num::text').extract_first().strip())
            item['title'] = book.css('.p-detail a::text').extract_first()
            item['author'] = book.css('.p-detail dl:nth-child(2)  a::text').extract_first()
            item['pub'] = book.css('.p-detail dl:nth-child(3) dd a::text').extract_first()
            item['sell_url'] = 'https://' + book.css('.p-detail a::attr(href)').extract_first().lstrip('/')
            book_price_id = 'J_' + book.css('.p-detail dl:nth-child(5) dd em::attr(data-price-id)').extract_first()
            yield SplashRequest(url=item['sell_url'],
                                callback=self.parse_content,
                                dont_filter=True,
                                meta={'item': item,
                                      'book_price_id': book_price_id},
                                args={'wait': 10},
                                encoding='utf8')

    def parse_content(self, response):
        pattern = re.compile(r'<[^>]+>', re.S)
        book_price_id = response.meta.get('book_price_id')
        item = response.meta.get('item')
        book_info = response.xpath("//div[@id='J-detail-content']/div[@id='detail-tag-id-3']/div[@class='item-mc']/div[@class='book-detail-content']").extract_first()
        recommend = response.xpath("//div[@id='J-detail-content']/div[@id='detail-tag-id-2']/div[@class='item-mc']/div[@class='book-detail-content']").extract_first()
        if book_info is not None:
            item['book_info'] = pattern.sub('', book_info).strip()
        else:
            pass
        if recommend is not None:
            item['recommend'] = pattern.sub('', recommend).strip()
        else:
            pass
        yield scrapy.Request(url=self.price_url.format(book_price_id=book_price_id),
                             callback=self.parse_price,
                             dont_filter=True,
                             meta={'item': item})

    def parse_price(self, response):
        price = json.loads(response.text)
        item = response.meta.get('item')
        item['price'] = '¥' + price[0].get('op')
        yield item
