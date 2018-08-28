# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import json
#还是用正常的翻页不要自己乱拼接
class XiciSpider(scrapy.Spider):
    name = 'xici'

    start_urls = ['http://www.xicidaili.com/nn/1']
    #字符串没有xpath命令！只能用css?用正则？
    def parse(self, response):
        for sel in response.xpath("//table[@id='ip_list']/tr[position()>1]").extract():
            print(sel)
            # patt = re.compile('<td>(.*?).(.*?).(.*?).(.*?)</td>')
            # items = re.findall(patt,sel)
            # print(items)


            # ip = sel.css('td:nth-child(2)').extract_first()
            # print(ip)
            #


#ip_list > tbody > tr:nth-child(2) > td:nth-child(2)