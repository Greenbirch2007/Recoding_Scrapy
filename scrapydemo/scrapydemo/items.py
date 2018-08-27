# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class ImoocCourseItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    # cate = scrapy.Field()
    image = scrapy.Field()
    # desc = scrapy.Field()
    brief = scrapy.Field()
    # cate = scrapy.Field()
    course_url = scrapy.Field()
    pass
