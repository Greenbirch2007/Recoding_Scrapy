# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class IpSpPipeline(object):
    def process_item(self, item, spider):
        DBS = spider.setting.get('DBS')
        con = pymysql.connect(**DBS)
        #使用utf8字符集
        con.set_charset('utf8')
        cur = con.cursor()
        insert_sql = ('insert in')
        return item
