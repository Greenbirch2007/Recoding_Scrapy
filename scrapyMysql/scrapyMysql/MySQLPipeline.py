# -*- coding: utf-8 -*-


import pymysql.cursors




class MySQLPipeline(object):
    def __init__(self):

        # 连接数据库
        self.connect = pymysql.connect(
            host = '127.0.0.1',  # 数据库地址
            port = 3306,  # 数据库端口
            db = 'scrapyMysql',  # 数据库名
            user = 'root',  # 数据库用户名
            passwd = 'root',  # 数据库密码
            charset = 'utf8',  # 编码方式
            use_unicode = True)
        # 通过cursor执行增删查改

        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        self.cursor.execute("""insert into mingyan(tag, cont)value (%s, %s)""", (item['tag'],item['cont'],))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回
