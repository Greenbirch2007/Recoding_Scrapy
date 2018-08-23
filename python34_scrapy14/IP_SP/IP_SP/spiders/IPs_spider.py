# -*- coding:utf-8 -*-



import scrapy
from IP_SP.items import IpSpItem

class xicispider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']

    start_urls = ('http://www.xicidaili.com/')


    def start_requests(self):
        res = []
        for i in range(1,2):
            url = 'http://www.xicidaili.com/nn/%d' % i
            req = scrapy.Request(url)
            res.append(req)
        return res
    #解析是要把css和xpath两种方法都些出来！
    def parse(self, response):
        table = response.xpath('//table[@id="ip_list"]')[0]
        trs = table.xpath('//tr')[1:] #去掉标题行
        items = []
        for tr in trs:

            pre_item = IpSpItem()   #使用到了存储的自定义字段
            pre_item['ip'] = tr.xpath('td[2]/text()').extract()[0]

            pre_item['port'] = tr.xpath('td[3]/text()').extract()[0]

            pre_item['type']=tr.xpath('td[6]/text()').extract()[0]
            items.append(pre_item)

 #将自定义的字段作为一个整体塞入一个空列表中
        return items