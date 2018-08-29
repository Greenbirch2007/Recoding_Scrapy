# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanreadingTravellingItem(scrapy.Item):
    image = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()
    star = scrapy.Field()
    value = scrapy.Field()
    image = scrapy.Field()

