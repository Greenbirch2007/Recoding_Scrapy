# -*- coding: utf-8 -*-
import scrapy
from daili_ips.items import DailiIpsItem


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["xicidaili.com"]
    start_urls = (
        'http://www.xicidaili.com/',
    )

    def start_requests(self):
        res = []
        for i in range(1, 2):
            url = 'http://www.xicidaili.com/nn/%d'%i
            req = scrapy.Request(url)
            # 存储所有对应地址的请求
            res.append(req)
        return res

    def parse(self, response):
        table = response.xpath('//table[@id="ip_list"]')[0]
        trs = table.xpath('//tr')[1:]   #去掉标题行
        items = []
        for tr in trs:
            pre_item = DailiIpsItem()
            pre_item['ip'] = tr.xpath('td[2]/text()').extract()[0]
            pre_item['port'] = tr.xpath('td[3]/text()').extract()[0]
            pre_item['position'] = tr.xpath('string(td[4])').extract()[0].strip()
            pre_item['type'] = tr.xpath('td[6]/text()').extract()[0]
            pre_item['speed'] = tr.xpath('td[7]/div/@title').re('\d+\.\d*')[0]
            pre_item['last_check_time'] = tr.xpath('td[10]/text()').extract()[0]
            items.append(pre_item)
        return items

# 表格数据的层级一层一层取剥离！这就是表格类数据的处理
# table -->>trs --->td