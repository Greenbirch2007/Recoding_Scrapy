# -*- coding: utf-8 -*-
import scrapy
from doubanbook_trip.items import DoubanbookTripItem


class DoubanBookTripSpider(scrapy.Spider):
    name = 'douban_book_trip'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/%E6%97%85%E8%A1%8C?start']

    def parse(self, response):
        item = response.xpath("//li[@class='subject-item']/div[@class='info']")  #模块整理拔下来，方面后面进行整体遍历

        for sel in item:
            book_item = DoubanbookTripItem()  #整体实例化 注意实例化的位置是在单个模块内

            book_item['title'] = sel.xpath('./h2/a/@title').extract_first()
            book_item['book_link'] = sel.xpath('./h2/a/@href').extract_first()

            all_descs = sel.xpath("./div[@class='pub']/text()").extract() #为了便于遍历，取全部的内容
            for descs in all_descs:
                co_desc = "".join(descs.split())
                book_item['co_desc'] = co_desc   #尝试遍历列表去除空格  要对字符串进行切割，然后再拼接

            book_item['star'] = sel.xpath("./div[@class='star clearfix']/span[@class='rating_nums']/text()").extract_first()
            all_commtents = sel.xpath("./div[@class='star clearfix']/span[@class='pl']/text()").extract()
            for commtents in all_commtents:
                comtent = "".join(commtents.split())
                book_item['comment'] = comtent
            book_item['intro'] = sel.xpath("./p/text()").extract_first()

            yield book_item  #再送入实例化的管道里面去


        next_page = response.xpath("//span[@class='next']/a/@href").extract()
        if next_page is not None:

            next_page = next_page[0]

            yield scrapy.Request("https://book.douban.com/" + next_page,callback=self.parse)






