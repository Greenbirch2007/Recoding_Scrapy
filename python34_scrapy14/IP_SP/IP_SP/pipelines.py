# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class IpSpPipeline(object):

    def process_item(self, item,spider):

        connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='web_monitor',
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = 'insert into proxy (ip,port,type) values (%s,%s,%s)'
        contents=(item['ip'],item['port'],item['type'])

        cursor.executemany(sql,contents)
        connection.commit()
        cursor.close()
        connection.close()
        return item









