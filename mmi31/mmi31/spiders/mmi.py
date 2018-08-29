# -*- coding: utf-8 -*-
import scrapy
from mmi31.items import Mmi31Item
import urllib.request
class MmiSpider(scrapy.Spider):
    name = 'mmi'
    allowed_domains = ['mm131.com']
    start_urls = ['http://www.mm131.com/xinggan/4292_2.html']
                  # 'http://www.mm131.com/qingchun/',
                  # 'http://www.mm131.com/xiaohua/',
                  # 'http://www.mm131.com/chemo/',
                  # 'http://www.mm131.com/qipao/',
                  # 'http://www.mm131.com/mingxing/']
    #分层爬取链接  #
    # def parse(self, response):
    #     fulllist = response.xpath("//dl[@class='list-left public-box']")  #单个页面的所有链接（1）
    #     for img1 in fulllist:
    #         url1 = img1.xpath("//a[@target='_blank']/@href").extract_first()   #爬取单个页面的图片链接（2）
    #         url2 = str(url1)               #定位倒数第二个元素
    #         next_page = response.xpath("//dd[@class='page']/a[last()-1]/@href").extract_first() #翻页的url链接 （3）
    #         if next_page is not None:
    #             yield response.follow(next_page, callback=self.parse)  #爬取页面的相对链接
    #         yield scrapy.Request(url2, callback=self.content)




#翻页都是相对链接，也就是response.follow 嵌套的太复杂！
    def content(self,response):
        item = Mmi31Item()  #这里是要解析图片链接
        images = response.xpath("//div[@class='content-pic']/a/img/@src").extract()
        for one_image in images:
            yield urllib.request.urlretrieve(one_image, '/home/karson/PICS/%s.jpg' % one_image[-20:-1])
        yield item



        #此时 实在一个绝对链接中拼接出相对地址 a 定位最后一个
        next_url = response.xpath('/html/body/div[6]/div[3]/a[last()]/@href').extract_first()  #用浏览器开发者工具定位xpath

        #一次性爬取链接，然后拼接，不要啰嗦






