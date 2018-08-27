# -*- coding: utf-8 -*-
import scrapy

from scrapytest.items import ScrapytestItem



class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['anjuke.com']
    start_urls = ['http://https://xa.fang.anjuke.com/loupan/all/p%s'% p for p in range(25)]

    def parse(self, response):

        #实例化一个容器保存爬去的信息
        item = CourseItem()
        item['name'] = response.xpath('//div[@class="infos"]/div[@class="lp-name"]/h3/a[@class="items-name"]/text()').extract()
        item['region'] = response.xpath('//div[@class="infos"]/p[@class="address"]/a[@class="list-map"]/text()').extract()
        item['price']=response.xpath('//p[@class="price"]/span/text()').extract()
        yield item


