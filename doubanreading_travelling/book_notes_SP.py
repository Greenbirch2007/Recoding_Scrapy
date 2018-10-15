import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None




def parse_note(html):

    selector = etree.HTML(html)

    title = selector.xpath('//*[@id="wrapper"]/h1/span/text()')
    short_comment = selector.xpath('//*[@id="comments"]/ul/li[1]/div/p/span/text()')
    book_notes = selector.xpath('//*[@id="content"]/div/div[1]/div[3]/div[14]/div[2]/ul[2]/li[1]/div[2]/div[2]/div/div[1]/span/text()')
    








def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='DB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(1,1001):
        sql = 'select coding from js_infos where id = %s ' % i
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        url = data['book_link']
        yield url




def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='DB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    cur.executemany('insert into book_contents (title,short_comment,book_notes) values (%s,%s,%s)', content)
    connection.commit()
    connection.close()
    print('向MySQL中添加数据成功！')

url = 'https://book.douban.com/subject/5414391/'
html = call_page(url)
content =parse_note(html)
insertDB(content)

# create table book_contents(
# id int not null primary key auto_increment,
# title varchar(20),
# short_comment text,
# book_notes text
# )engine=InnoDB  charset=utf8;
#
