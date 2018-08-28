# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DbSpider(scrapy.Spider):
    name = 'DB'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']


      #默认解析方法
    def parse(self, response):
        # 把要爬取的数据作为一个item_list整理爬取下来再进行遍历
        #xpath 注意别忘了 “ .  ” 另外是extract()还是extract_first()要思考

        #
        item_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in item_list:

            #item文件导入，类实例化
            DBitem = DoubanItem()
            DBitem['rank'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            DBitem['name'] = i_item.xpath(".//div[@class='hd']/a/span[1]//text()").extract_first()
            alld_content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()

            #数据处理
            for i_content in alld_content:
                contents_s = "".join(i_content.split())
                DBitem['content'] = contents_s
            DBitem['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            DBitem['comment'] = i_item.xpath("./div[@class='star']//span[4]/text()").extract_first()
            DBitem['des'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()

            #需要把数据yield到pipelines进行数据
            yield DBitem

            #拿到属性，而不是内容！
         #解析下一页规则，取后页的xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
         #注意extract_first() 返回一个字符串，可用于字符串拼接 ，
        #extract()返回一个列表，可以用于遍历列表中的元素！
        if next_link:
            next_link = next_link[0] #翻页时要注意url的拼接！
            yield scrapy.Request('https://movie.douban.com/top250'+ next_link,callback=self.parse)














