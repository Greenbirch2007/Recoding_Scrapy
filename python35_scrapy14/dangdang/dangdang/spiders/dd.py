# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from dangdang.items import DangdangItem



class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://dangdang.com/']

    ua = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'

    }

    def start_requests(self):
        return [Request('http://search.dangdang.com/?key=python&act=input&show=big&page_index=1#J_tab',headers=self.ua,callback=self.parse)]
    def parse(self, response):
        item=DangdangItem()
        item['title']=response.xpath("//a[@class='pic']/@title").extract()
        item['link'] = response.xpath("//a[@class='pic']/@href").extract()
        item['comment'] = response.xpath("//a[@dd_name='单品评论']/text()").extract()
        yield item
        for i in range(2,33):
            url='http://search.dangdang.com/?key=python&act=input&show=big&page_index='+str(i)+'#J_tab'
