


#scrapy数据的存储主要是靠pipelines模块


import codecs
#python编码解码器的基类

import json

from scrapy.pipeline.images import ImagesPipeline
#scrapy 自带的图片处理的类
from scrapy.exporters import JsonItemExporter
#scrapy 导出json类 JsonItemExporter

import pymysql
import pymysql.cursors
#导入 pymysql 数据包

import pymongo
#导入 pymongo

from twisted.enterprise import adbapi

'''twisted 是一个异步网络框架
twisted.enterprise.adbapi就是DB-API 2.0 API的非阻塞接口，可以访问各种关系型数据库'''



#mysq 数据导出

class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1','root','123456','test',charset='utf8')
        #连接mysql数据库
        self.cursors = self.conn.cursor()
        #获取 mysql 数据库指针
    def process_item(self,item,spider):
        insert_sql = '''insert into test(title,url,create_date) values(%s,%s,%s)）'''
        self.cursor.execute(insert_sql,(item['title'],item['url'],item['create_date']))
        #执行导入数据
        self.conn.commit()
        #提交数据


#Mysql非阻塞 数据存储：

class MysqlTwistedPipeline(object):
    '''异步存储数据  非阻塞型 '''
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db= settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='urt8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode=True,)
        dbpool= adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        #使用twisted将mysql 插入变成异步执行
        query = self.dbpool.runInteraction(self,db_insert,item)
        query.addErrback(self.handle_error,item,spider) #处理异常
    def handle_error(self,failure,item,spider):
        #处理异步插入的异常
        print(failure)
    def do_insert(self,cursor,item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入mysql
        insert_sql,params = item.get_insert_sql()
        print(insert_sql,params)
        cursor.execute(insert_sql,params)



#json数据存储


class JsonExporterPipeline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii='Flase')
        #打开文件
        self.exporter.start_exporting()
        #导出文件
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    #文件关闭
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

# mongodb 数据库存储

class MongoPipeline(object):
    #mongodb 数据库存储
    collection_name = 'scrapy_items'
    #数据库名称

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongodb = mongodb

    @classmethod
    def from_crawler(cls,crawler):
        #从settings 获取MONGO_URI,MONGO_DB
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('mongo_db','items'))

    def open_spider(self,spider):
        #数据库打开配置
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def close_spider(self,spier):
        #数据库关闭
        self.client.close()
    def process_item(self,item,spier):
        #数据库存储
        self.db[self.collection_name].insert_one(dict(item))
        return item
        # 切记 一定要返回item进行后续的pipelines 数据处理


