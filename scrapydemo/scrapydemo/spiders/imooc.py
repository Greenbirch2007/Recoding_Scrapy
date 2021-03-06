# -*- coding: utf-8 -*-

import scrapy
from urllib import parse as urlparse
from scrapydemo.items import ImoocCourseItem


# 慕课网爬取
class ImoocSpider(scrapy.Spider):
    # spider的名字定义了Scrapy如何定位(并初始化)spider，所以其必须是唯一的
    name = "imooc"

    # URL列表
    start_urls = ['http://www.imooc.com/course/list']
    #  域名不在列表中的URL不会被爬取。
    allowed_domains = ['www.imooc.com']

    def parse(self, response):
        learn_nodes = response.css('a.course-card')

        item = ImoocCourseItem()
        # 遍历该页上所有课程列表
        for learn_node in learn_nodes:
            course_url = learn_node.css("::attr(href)").extract_first()
            # 拼接课程详情页地址
            course_url = urlparse.urljoin(response.url, course_url)
            # 课程地址
            item['course_url'] = course_url
            # 课程图片
            item['image'] = learn_node.css(
                "img.course-banner::attr(src)").extract_first()
            # 进入课程详情页面
            yield scrapy.Request(
                url=course_url, callback=self.parse_learn, meta=item)

        # 下一页地址
        next_page_url = response.css(
            u'div.page a:contains("下一页")::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(
                url=urlparse.urljoin(response.url, next_page_url),
                callback=self.parse)

    def parse_learn(self, response):
        item = response.meta
        # 课程标题
        item['title'] = response.xpath(
            '//h2[@class="l"]/text()').extract_first()
        # 课程简介
        item['brief'] = response.xpath(
            '//div[@class="course-brief"]/p/text()').extract_first()
        yield item