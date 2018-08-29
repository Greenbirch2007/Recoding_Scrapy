# -*- coding: utf-8 -*-
import scrapy
from ImageSpider.items import ImagespiderItem
import urllib.request
class ImgspiderSpider(scrapy.Spider):
    name = 'ImgSpider'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/archives/55.html']

    def parse(self, response):
        item = ImagespiderItem()
        imgurls = response.css(".post img::attr(src)").extract()
        # imgurls = response.xpath('//img/@src').extract()
        # item['imgurl'] = imgurls
        for one_image in imgurls:
            yield urllib.request.urlretrieve(one_image, '/home/karson/PICS/%s.jpg' % one_image[-10:-1])

        yield item

#1.需要yield item  不能把组件隔断，顶多是不用而已！用pass让它过去

#2.直接在spider中编辑就好！
