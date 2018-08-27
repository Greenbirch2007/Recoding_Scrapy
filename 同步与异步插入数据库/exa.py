
接下来保存数据库两种方法：

同步操作：数据少可以
异步操作：大数据（scrapy爬取得速度快于数据库插入速度，当数据量大时，就会出现阻塞，异步就能解决）
1.同步

修改数据，由于我们抓取的时间格式是str 需要转换成date存入数据库



import  datetime

try:
    create_date=datetime.datetime.strptime('create_date',"%Y/%m/%d").date()
except Exception as e:
    create_date =datetime.datetime.now().date()  #如果没有就取当前时间
article_item['create_date'] =create_date




import MySQLdb

class MysqlPipeline(object):
    def __init__(self):
        self.conn=MySQLdb.connect('localhost','root','root','article',charset='utf8',use_unicode=True)
        self.cursor=self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql="""
            insert into article(title,url,create_date,url_object_id,front_image_url,front_image_path,
            praise,collect_nums,comment_nums,contents,tags)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item['title'],item['url'],item['create_date'],item['url_object_id'],
        item['front_image_url'],item['front_image_path'],item['praise'],item['collect_nums'],item['comment_nums'],item['contents'],item['tags'] ))
        self.conn.commit()










import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class MysqlTwistPipeline(object):

    @classmethod
    def from_settings(cls,settings):#名称固定 会被scrapy调用 直接可用setting的值
        adbparams=dict(
            host=settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
            )
        #这是链接数据库的另一种方法，在settings中写入参数
        dbpool=adbapi.ConnectionPool('MySQLdb',**adbparams)
        return cls(dbpool)

    def __init__(self,dbpool):
        self.dbpool=dbpool

    def process_item(self, item, spider):
        #使用twiest将mysql插入变成异步
        query=self.dbpool.runInteraction(self.do_insert,item)
        #因为异步 可能有些错误不能及时爆出
        query.addErrback(self.handle_error)

    #处理异步的异常
    def handle_error(self,failure):
        print('failure')

    def do_insert(self,cursor,item):
        insert_sql = """
                    insert into article(title,url,create_date,url_object_id,front_image_url,front_image_path,
                    praise,collect_nums,comment_nums,contents,tags)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['url_object_id'],item['front_image_url'], item['front_image_path'], item['praise'],item['collect_nums'], item['comment_nums'], item['contents'], item['tags']))

        ITEM_PIPELINES = {
            'spider_first.pipelines.ArticleImagePipeline': 1,
            'spider_first.pipelines.MysqlPipeline': 2,
        }