# -*- coding: utf-8 -*-
import scrapy


class BooksTravellingSpider(scrapy.Spider):
    name = 'books_travelling'
    allowed_domains = ['book.douban.com']
    start_urls = ['http://book.douban.com/']

    def parse(self, response):
        pass
