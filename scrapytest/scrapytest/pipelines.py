# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
import pymysql
import pymysql.cursors
import codecs
from twisted.enterprise import adbapi






class ScrapytestPipeline(object):





    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            charset = 'utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode = True,
         )
        dbpool = adbapi.ConnectionPool('pymysql',**dbargs)
        return cls(dbpool)


    def __init__(self,dbpool):
        self.dbpool = dbpool.run



        #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert,item,spider)
        log.msg("-------------连接好了---------------------")
        d.addErrback(self._handle_error,item,spider)
        d.addBoth(lambda _:item)
        return d
    def _conditional_insert(self,conn,item,spider):
        log.msg('----------------打印----------------')
        conn.execute('insert into test(name,region,price) values(%s,%s,%s)',(item['name'],item['region'],item['price']))
        log.msg('---------------一轮循环完毕---------------------')
    def _handle_error(self,failure,item,spider):
        print(failure)




