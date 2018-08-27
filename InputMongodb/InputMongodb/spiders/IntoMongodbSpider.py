# -*- coding: utf-8 -*-
import scrapy
from InputMongodb.items import InputmongodbItem

class IntomongodbspiderSpider(scrapy.Spider):
    name = 'IntoMongodbSpider'
    allowed_domains = ['lab.scrapyd.cn/']
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        mingyan = response.css('div.quote')

        item = InputmongodbItem()  # 实例化item类
        for v in mingyan:  # 循环获取每一条名言里面的：名言内容、作者、标签
            item['cont']=v.css('.text::text').extract_first()
            # 提取名言
            tags = v.css('.tags .tag::text').extract()
            item['tag'] = ','.join(tags)
            # 把取到的数据提交给pipline处理
            yield item
        # css选择器提取下一页链接
        next_page = response.css('li.next a::attr(href)').extract_first()
        # 判断是否存在下一页
        if next_page is not None:
            next_page = response.urljoin(next_page)
            # 提交给parse继续抓取下一页
            yield scrapy.Request(next_page, callback=self.parse)














          
