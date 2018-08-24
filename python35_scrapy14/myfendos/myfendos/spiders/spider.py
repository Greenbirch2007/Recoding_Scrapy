# -*- coding: utf-8 -*-
import scrapy
from myfendos.items import MyfendoItem


class MyfendosSpider(scrapy.Spider):
    name = "myfendos"
    allowed_domains = ["csdn.net"]
    start_urls = [
        "http://blog.csdn.net/u011781521/article/details/70182815",
    ]

    def parse(self, response):
        item = MyfendoItem()
        item['title'] = response.xpath('//h1/span/a/text()')
        item['link'] = response.xpath("//span/a[@href='https://scrapy.org/']/text()")
        item['desc'] = response.xpath("//meta[@name='description']")
        yield item
