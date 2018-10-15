# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanbookTripItem(scrapy.Item):
    title = scrapy.Field()
    co_desc = scrapy.Field()
    star = scrapy.Field()
    comment = scrapy.Field()
    intro = scrapy.Field()
    book_link = scrapy.Field()


# create table DBbook_trip
# (id int not null primary key auto_increment,
# title varchar(20),
# co_desc varchar(50),
#         star char(10),
#              comment varchar(12),
#                      intro varchar(255),
# book_link varchar(50)
# ) engine=InnoDB  charset=utf8;


#  建表时desc 关键字慎用！