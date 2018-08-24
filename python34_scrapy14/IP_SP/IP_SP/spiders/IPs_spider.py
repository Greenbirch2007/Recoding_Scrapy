# -*- coding:utf-8 -*-



import scrapy
from scrapy import Request
from IP_SP.items import IpSpItem

class xicispider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']

    start_urls = ('http://www.xicidaili.com/')

    def start_requests(self):

        for i in range(1,10):
            yield Request('http://www.xicidaili.com/nn/%s'%i)

    def parse(self, response):
        for sel in response.xpath('//table[@id="ip_list"]/tr[position()>1]'):
            ip = sel.css('td:nth-child(2)::text').extract_first()
            port = sel.css('td:nth-child(4)::text').extract_first()
            type = sel.css('td:nth-child(6)::text').extract_first().lower()

            #
sdf

 
dsfa  