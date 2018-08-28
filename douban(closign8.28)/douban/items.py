# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    rank = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    star = scrapy.Field()
    comment = scrapy.Field()
    des = scrapy.Field()



#
# create table movies(
# id int not null primary key auto_increment,
# rank int not null,
# name varchar(16),
# content varchar(66),
# star char(10),
# comment varchar(10),
# des varchar(50)
# ) engine=InnoDB  charset=utf8;