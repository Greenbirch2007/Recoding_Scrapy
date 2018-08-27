

import pymysql

class MysqlPipelien(object):
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self,spider):

        #连接数据库
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user=root,
            password='123456',
            db='test',
            charset='utf8mb4'
        )
        self.cur = pymysql.connect.cursor() #游标

    def process_item(self,item,spider):
        pass
    #sql语句
    self.cur.execute(sql,content)
    self.conn.commit()
    return item


    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()
