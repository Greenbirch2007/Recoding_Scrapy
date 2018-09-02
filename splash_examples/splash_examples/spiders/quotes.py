# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        for sel in response.xpath("//div[@class='quote']"):
            quote = sel.xpath("./span[@class='text']/text()").extract_first()
            author = sel.xpath("./span[2]/small[@class='author']/text()").extract_first()
            yield {'quote':quote,'author':author}

        href = response.xpath("//ul[@class='pager']/li/a/@href").extract_first()

        if href is not None:
            url = response.urljoin(href)

            yield SplashRequest(url,cargs={'images':0,'timeout':3})
