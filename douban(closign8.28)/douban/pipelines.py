# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from douban.settings import mongo_host,mongo_port,mongo_db_name,mongo_db_collection
import pymysql
# 注意self.post的方法
class DoubanPipeline(object):

    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        tabname = mongo_db_collection
        client = pymongo.MongoClient(host=host,port=port)
        mydb = client[dbname]
        self.post = mydb[tabname]

    def process_item(self, item, spider):

        data = dict(item)
        self.post.insert(data)
        return item


#使用mysql分布式存储成功！
from twisted.enterprise import adbapi

class MySQLAsyncPipelne:
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DB_NAME','douban')
        host = spider.settings.get('MYSQL_HOST','localhost')
        port = spider.settings.get('MYSQL_PORT',3306)
        user = spider.settings.get('MYSQL_USER','root')
        password = spider.settings.get('MYSQL_PASSWORD','123456')

        self.dbpool = adbapi.ConnectionPool('pymysql',host=host,db=db,user=user,\
                                            password=password,charset='utf8')

    def close_spider(self,spider):
        self.dbpool.close()

    def process_item(self,item,spider):
        self.dbpool.runInteraction(self.insert_db,item)
        return item

    def insert_db(self,text,item):
        values = (item['rank'],item['name'],item['content'],item['star'],item['comment'],item['des'])

        sql = 'insert into movies(rank,name,content,star,comment,des) values(%s,%s,%s,%s,%s,%s)'
        text.execute(sql,values)  #替代了游标


#
# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect('127.0.0.1','root','123456','douban',charset='utf8')
#         self.cursor = self.conn.cursor()
#
#     def process_item(self,item,spider):
#         insert_sql = """insert"""