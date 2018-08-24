# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
class DangdangPipeline(object):
    def process_item(self, item, spider):
        con=pymysql.connect('127.0.0.1','root','123456','dangdang',charset='utf8')
        cursor = con.cursor()
        for i in range(len(item['title'])):
            title=item['title'][i]
            link = item['link'][i]
            comment = item['comment'][i]
            sql="""insert into books(title,link,comment) VALUES(%s,%s,%s)"""
            cursor.execute(sql,(title,link,comment))
            con.commit()
        con.close()
        return item


