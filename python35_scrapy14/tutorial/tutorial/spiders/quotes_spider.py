# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'


    def start_requests(self):
        url = 'http://http://quotes.toscrape.com/tag/humor/'
        yield scrapy.Request(url)


    def parse(self, response):
        item = TutorialItem()
        for quote in response.css('div.quote'):
            item['body'] = quote.css('span.text::text').extract_first()
            item['author'] = quote.css('small.author::text').extract_first()
            yield item
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
