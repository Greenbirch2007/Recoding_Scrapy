#第八章
#8.3 爬虫的浏览器伪装技术实战
#(1)
import urllib.request
import http.cookiejar
url= "http://news.163.com/16/0825/09/BVA8A9U500014SEH.html"
cjar=http.cookiejar.CookieJar()
proxy= urllib.request.ProxyHandler({'http':"127.0.0.1:8888"})
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler,urllib.request.HTTPCookieProcessor(cjar))
urllib.request.install_opener(opener)
data=urllib.request.urlopen(url).read()
fhandle=open("D:/Python35/myweb/part8/1.html","wb")
fhandle.write(data)
fhandle.close()

#(2)
import urllib.request
import http.cookiejar
url= "http://news.163.com/16/0825/09/BVA8A9U500014SEH.html"
#以字典的形式设置headers
headers={ "Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language":" zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
                        "Connection": "keep-alive",
                        "referer":"http://www.163.com/"}
#设置cookie
cjar=http.cookiejar.CookieJar()
proxy= urllib.request.ProxyHandler({'http':"127.0.0.1:8888"})
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler,urllib.request.HTTPCookieProcessor(cjar))
#建立空列表，为了以指定格式存储头信息
headall=[]
#通过for循环遍历字典，构造出指定格式的headers信息
for key,value in headers.items():
    item=(key,value)
    headall.append(item)
#将指定格式的headers信息添加好
opener.addheaders = headall
#将opener安装为全局
urllib.request.install_opener(opener)
data=urllib.request.urlopen(url).read()
fhandle=open("D:/Python35/myweb/part8/2.html","wb")
fhandle.write(data)
fhandle.close()

#(3)
import urllib.request
import http.cookiejar
#注意，如果要通过fiddler调试，则下方网址要设置为"http://www.baidu.com/"
url= "http://www.baidu.com"
headers={ "Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Encoding":" gb2312,utf-8",
                        "Accept-Language":" zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
                        "Connection": "keep-alive",
                        "referer":"baidu.com"}
cjar=http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
headall=[]
for key,value in headers.items():
    item=(key,value)
    headall.append(item)
opener.addheaders = headall
urllib.request.install_opener(opener)
data=urllib.request.urlopen(url).read()
fhandle=open("D:/Python35/myweb/part8/3.html","wb")
fhandle.write(data)
fhandle.close()

# 第20章模拟登录爬虫项目
# 20.3 模拟登录爬虫项目编写实战
# (1)
# -*- coding: utf-8 -*-
import scrapy
import urllib.request
from scrapy.http import Request, FormRequest


class LoginspdSpider(scrapy.Spider):
    name = "loginspd"
    allowed_domains = ["douban.com"]
    # 设置头信息变量，供下面的代码中模拟成浏览器爬取
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}

    # 编写start_requests()方法，第一次会默认调取该方法中的请求
    def start_requests(self):
        # 首先爬一次登录页，然后进入回调函数parse()
        return [Request("https://accounts.douban.com/login", meta={"cookiejar": 1}, callback=self.parse)]

    def parse(self, response):
        # 获取验证码图片所在地址，获取后赋给captcha变量，此时captcha为一个列表
        captcha = response.xpath('//img[@id="captcha_image"]/@src').extract()
        # 因为登录时有时网页有验证码，有时网页没有验证码
        # 所以需要判断此时是否需要输入验证码，若captcha列表中有元素，说明有验证码信息
        if len(captcha) > 0:
            print("此时有验证码")
            # 设置将验证码图片存储到本地的本地地址
            localpath = "D:/Python35/myweb/part20/loginpjt/captcha.png"
            # 将服务器中的验证码图片存储到本地，供我们在本地直接进行查看
            urllib.request.urlretrieve(captcha[0], filename=localpath)
            print("请查看本地图片captcha.png并输入对应验证码：")
            # 通过input()等待我们输入对应的验证码并赋给captcha_value变量
            captcha_value = input()
            # 设置要传递的post信息
            data = {
                # 设置登录账号，格式为账号字段名:具体账号
                "form_email": "weisuen007@163.com",
                # 设置登录密码，格式为密码字段名:具体密码，读者需要将账号密码换成自己的
                # 因为笔者完成该项目后已经修改密码
                "form_password": "weijc7789",
                # 设置验证码，格式为验证码字段名:具体验证码
                "captcha-solution": captcha_value,
                # 设置需要转向的网址，由于我们需要爬取个人中心页，所以转向个人中心页
                "redir": "https://www.douban.com/people/151968962/",
            }
        # 否则说明captcha列表中没有元素，即此时不需要输入验证码信息
        else:
            print("此时没有验证码")
            # 设置要传递的post信息，此时没有验证码字段
            data = {
                "form_email": "weisuen007@163.com",
                "form_password": "weijc7789",
                "redir": "https://www.douban.com/people/151968962/",
            }
        print("登录中…")
        # 通过FormRequest.from_response()进行登录
        return [FormRequest.from_response(response,
                                          # 设置cookie信息
                                          meta={"cookiejar": response.meta["cookiejar"]},
                                          # 设置headers信息模拟成浏览器
                                          headers=self.header,
                                          # 设置post表单中的数据
                                          formdata=data,
                                          # 设置回调函数，此时回调函数为next()
                                          callback=self.next,
                                          )]

    def next(self, response):
        print("此时已经登录完成并爬取了个人中心的数据")
        # 此时response为个人中心网页中的数据
        # 以下通过Xpath表达式分别提取个人中心中该用户的相关信息
        # 网页标题Xpath表达式
        xtitle = "/html/head/title/text()"
        # 日记标题Xpath表达式
        xnotetitle = "//div[@class='note-header pl2']/a/@title"
        # 日记发表时间Xpath表达式
        xnotetime = "//div[@class='note-header pl2']//span[@class='pl']/text()"
        # 日记内容Xpath表达式
        xnotecontent = "//div[@class='mbtr2']/div[@class='note']/text()"
        # 日记链接Xpath表达式
        xnoteurl = "//div[@class='note-header pl2']/a/@href"

        # 分别提取网页标题、日记标题、日记发表时间、日记内容、日记链接
        title = response.xpath(xtitle).extract()
        notetitle = response.xpath(xnotetitle).extract()
        notetime = response.xpath(xnotetime).extract()
        notecontent = response.xpath(xnotecontent).extract()
        noteurl = response.xpath(xnoteurl).extract()
        print("网页标题是：" + title[0])
        # 可能有多篇日记，通过for循环依次遍历
        for i in range(0, len(notetitle)):
            print("第" + str(i + 1) + "篇文章的信息如下:")
            print("文章标题为：" + notetitle[i])
            print("文章发表时间为：" + notetime[i])
            print("文章内容为：" + notecontent[i])
            print("文章链接为：" + noteurl[i])

            print("------------")







#第九章
#9.3 定向抓取实战
#（1）
import urllib.request
import http.cookiejar
import re
#视频编号
vid="1472528692"
#刚开始时候的评论ID
comid="6173403130078248384"
url= "http://coral.qq.com/article/"+vid+"/comment?commentid="+comid+"&reqnum=20"
headers={ "Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Encoding":" gb2312,utf-8",
                        "Accept-Language":" zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
                        "Connection": "keep-alive",
                        "referer":"qq.com"}
cjar=http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
headall=[]
for key,value in headers.items():
    item=(key,value)
    headall.append(item)
opener.addheaders = headall
urllib.request.install_opener(opener)
#建立一个自定义函数craw(vid,comid),实现自动抓取对应评论网页并返回抓取数据
def craw(vid,comid):
    url= "http://coral.qq.com/article/"+vid+"/comment?commentid="+comid+"&reqnum=20"
    data=urllib.request.urlopen(url).read().decode("utf-8")
    return data
idpat='"id":"(.*?)"'
userpat='"nick":"(.*?)",'
conpat='"content":"(.*?)",'
#第一层循环，代表抓取多少页，每一次外层循环抓取一页
for i in range(1,10):
    print("------------------------------------")
    print("第"+str(i)+"页评论内容")
    data=craw(vid,comid)
    #第二层循环，根据抓取的结果提取并处理每条评论的信息，一页20条评论
    for j in range(0,20):
        idlist=re.compile(idpat,re.S).findall(data)
        userlist=re.compile(userpat,re.S).findall(data)
        conlist=re.compile(conpat,re.S).findall(data)
        print("用户名是 :"+eval('u"'+userlist[j]+'"'))
        print("评论内容是:"+eval('u"'+conlist[j]+'"'))
        print("\n")
    #将comid改变为该页的最后一条评论id，实现不断自动加载
    comid=idlist[19]

# 第十八章 第四篇 实战项目案例
# 18.3 和讯博客爬虫项目编写实战
# （1）
Create
database
hexun;

# (2)
Use
hexun;
Create
table
myhexun(id
int(10)
auto_increment
primary
key
not null, name
varchar(30), url
varchar(100), hits
int(15), comment
int(15));

# (3)
D:\Python35\myweb\part18 > scrapy
startproject
hexunpjt
New
Scrapy
project
'hexunpjt', using
template
directory
'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
D:\Python35\myweb\part18\hexunpjt
You
can
start
your
first
spider
with:
    cd
    hexunpjt
    scrapy
    genspider
    example
    example.com

# (4)
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HexunpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 建立name存储文章名
    name = scrapy.Field()
    # 建立url存储文章url网址
    url = scrapy.Field()
    # 建立hits存储文章阅读数
    hits = scrapy.Field()
    # 建立comment存储文章评论数
    comment = scrapy.Field()


# (5)
# -*- coding: utf-8 -*-
import pymysql


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HexunpjtPipeline(object):

    def __init__(self):
        # 刚开始时连接对应数据库
        self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="hexun")

    def process_item(self, item, spider):
        # 每一个博文列表页中包含多篇博文的信息，我们可以通过for循环一次处理各博文的信息
        for j in range(0, len(item["name"])):
            # 将获取到的name、url、hits、comment分别赋给各变量
            name = item["name"][j]
            url = item["url"][j]
            hits = item["hits"][j]
            comment = item["comment"][j]
            # 构造对应的sql语句，实现将获取到的对应数据插入数据库中
            sql = "insert into myhexun(name,url,hits,comment) VALUES('" + name + "','" + url + "','" + hits + "','" + comment + "')"
            # 通过query实现执行对应的sql语句
            self.conn.query(sql)
        return item

    def close_spider(self, spider):
        # 最后关闭数据库连接
        self.conn.close()


# (6)

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'hexunpjt.pipelines.HexunpjtPipeline': 300,
}

# (7)
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# (8)
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# (9)
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# (10)
# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from hexunpjt.items import HexunpjtItem
from scrapy.http import Request


class MyhexunspdSpider(scrapy.Spider):
    name = "myhexunspd"
    allowed_domains = ["hexun.com"]
    # 设置要爬取的用户的uid，为后续构造爬取网址做准备
    uid = "19940007"

    # 通过start_requests方法编写首次的爬取行为
    def start_requests(self):
        # 首次爬取模拟成浏览器进行
        yield Request("http://" + str(self.uid) + ".blog.hexun.com/p1/default.html", headers={
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})

    def parse(self, response):
        item = HexunpjtItem()
        item['name'] = response.xpath("//span[@class='ArticleTitleText']/a/text()").extract()
        item["url"] = response.xpath("//span[@class='ArticleTitleText']/a/@href").extract()
        # 接下来需要使用urllib和re模块获取博文的评论数和阅读数
        # 首先提取存储评论数和点击数网址的正则表达式
        pat1 = '<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        # hcurl为存储评论数和点击数的网址
        hcurl = re.compile(pat1).findall(str(response.body))[0]
        # 模拟成浏览器
        headers2 = ("User-Agent",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers2]
        # 将opener安装为全局
        urllib.request.install_opener(opener)
        # data为对应博客列表页的所有博文的点击数与评论数数据
        data = urllib.request.urlopen(hcurl).read()
        # pat2为提取文章阅读数的正则表达式
        pat2 = "click\d*?','(\d*?)'"
        # pat3为提取文章评论数的正则表达式
        pat3 = "comment\d*?','(\d*?)'"
        # 提取阅读数和评论数数据并分别赋值给item下的hits和comment
        item["hits"] = re.compile(pat2).findall(str(data))
        item["comment"] = re.compile(pat3).findall(str(data))
        yield item
        # 提取博文列表页的总页数
        pat4 = "blog.hexun.com/p(.*?)/"
        # 通过正则表达式获取到的数据为一个列表，倒数第二个元素为总页数
        data2 = re.compile(pat4).findall(str(response.body))
        if (len(data2) >= 2):
            totalurl = data2[-2]
        else:
            totalurl = 1
        # 在实际运行中，下一行print的代码可以注释掉，在调试过程中，可以开启下一行print的代码
        # print("一共"+str(totalurl)+"页")
        # 进入for循环，依次爬取各博文列表页的博文数据
        for i in range(2, int(totalurl) + 1):
            # 构造下一次要爬取的url，爬取一下页博文列表页中的数据
            nexturl = "http://" + str(self.uid) + ".blog.hexun.com/p" + str(i) + "/default.html"
            # 进行下一次爬取，下一次爬取仍然模拟成浏览器进行
            yield Request(nexturl, callback=self.parse, headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})


# 第十二章
# 12.3 常用工具命令
# (1)
from scrapy.spiders import Spider


class FirstSpider(Spider):
    name = "first"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.baidu.com",
    ]

    def parse(self, response):
        pass

# (2)
>> > ti = sel.xpath("/html/head/title")
>> > print(ti)
[ < Selector
xpath = '/html/head/title'
data = '<title>百度一下，你就知道</title>' >]
>> >

# (3)
>> > exit()
D:\Python35\myweb\part12 >


# 12.4 实战Items
# (1)
class MyfirstpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    urlname = scrapy.Field()
    urlkey = scrapy.Field()
    urlcr = scrapy.Field()
    urladdr = scrapy.Field()

# (2)
>> > import scrapy
>> >

class person(scrapy.Item):
    name = scrapy.Field()
    job = scrapy.Field()
    email = scrapy.Field()

# (3)
>> > weisuen = person(name="weiwei", job="teacher", email="qiansyy@iqianyue.com")

# (4)
>> > print(weisuen)
{'email': 'qiansyy@iqianyue.com', 'job': 'teacher', 'name': 'weiwei'}

# (5)
>> > weisuen["job"]
'teacher'

# (6)
>> > weisuen["email"]
'abc@sina.com'

# (7)
>> > weisuen.keys()
dict_keys(['job', 'email', 'name'])

# (8)
>> > weisuen.items()
ItemsView({'email': 'abc@sina.com', 'job': 'teacher', 'name': 'weiwei'})

# 12.5 实战Spider类
# (1)
# -*- coding: utf-8 -*-
import scrapy
from myfirstpjt.items import MyfirstpjtItem


class WeisuenSpider(scrapy.Spider):
    name = "weisuen"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
        'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )

    def parse(self, response):
        item = MyfirstpjtItem()
        item["urlname"] = response.xpath("/html/head/title/text()")
        print(item["urlname"])


# (2)
# -*- coding: utf-8 -*-
import scrapy
from myfirstpjt.items import MyfirstpjtItem


class WeisuenSpider(scrapy.Spider):
    name = "weisuen"
    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
        'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )
    # 定义了新属性url2
    urls2 = ("http://www.jd.com",
             "http://sina.com.cn",
             "http://yum.iqianyue.com",
             )

    # 重写了start_requests()方法
    def start_requests(self):
        # 在该方法中将起始网址设置为从新属性url2中读取
        for url in self.urls2:
            # 调用默认make_requests_from_url()方法生成具体请求并通过yield返回
            yield self.make_requests_from_url(url)

    def parse(self, response):
        item = MyfirstpjtItem()
        item["urlname"] = response.xpath("/html/head/title/text()")
        print(item["urlname"])


# 12.7 	Spider类参数传递
# (1)
# -*- coding: utf-8 -*-
import scrapy
from myfirstpjt.items import MyfirstpjtItem


class WeisuenSpider(scrapy.Spider):
    name = "weisuen"
    # 此时虽然还在此定义了start_urls属性，但不起作用，因为在构造方法进行了重写
    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
        'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )

    # 重写初始化方法__init__()，并设置参数myurl
    def __init__(self, myurl=None, *args, **kwargs):
        super(WeisuenSpider, self).__init__(*args, **kwargs)
        # 输出要爬的网址，对应值为接收到的参数
        print("要爬取的网址为：%s" % myurl)
        # 重新定义start_urls属性，属性值为传进来的参数值
        self.start_urls = ["%s" % myurl]

    def parse(self, response):
        item = MyfirstpjtItem()
        item["urlname"] = response.xpath("/html/head/title/text()")
        print("以下将显示爬取的网址的标题")
        print(item["urlname"])


# (2)
# -*- coding: utf-8 -*-
import scrapy
from myfirstpjt.items import MyfirstpjtItem


class WeisuenSpider(scrapy.Spider):
    name = "weisuen"

    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
        'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )

    def __init__(self, myurl=None, *args, **kwargs):
        super(WeisuenSpider, self).__init__(*args, **kwargs)
        # 通过split()将传递进来的参数以“|”为切割符进行分隔，分隔后生成一个列表并赋值给myurllist变量
        myurllist = myurl.split("|")
        # 通过for循环遍历该列表myurllist，并分别输出传进来要爬取的各网址
        for i in myurllist:
            print("要爬取的网址为：%s" % i)
        # 将起始网址设置为传进来的参数中各网址组成的列表
        self.start_urls = myurllist

    def parse(self, response):
        item = MyfirstpjtItem()
        item["urlname"] = response.xpath("/html/head/title/text()")
        print("以下将显示爬取的网址的标题")
        print(item["urlname"])


# 12.8 用XMLFeedSpider来分析XML源
# (1)
D:\Python35\myweb\part12 > scrapy
startproject
myxml
New
Scrapy
project
'myxml', using
template
directory
'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
D:\Python35\myweb\part12\myxml

You
can
start
your
first
spider
with:
    cd
    myxml
    scrapy
    genspider
    example
    example.com

# (2)
import scrapy


class MyxmlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 存储文章标题
    title = scrapy.Field()
    # 存储对应链接
    link = scrapy.Field()
    # 存储对应文章作者
    author = scrapy.Field()


定义好要存储的结构化数据之后，可以创建一个爬虫文件用于分析XML源，如下所示。
D:\Python35\myweb\part12 > cd
myxml \
    D:\Python35\myweb\part12\myxml > scrapy
genspider - l
Available
templates:
basic
crawl
csvfeed
xmlfeed
D:\Python35\myweb\part12\myxml > scrapy
genspider - t
xmlfeed
myxmlspider
sina.com.cn
Created
spider
'myxmlspider'
using
template
'xmlfeed' in module:
myxml.spiders.myxmlspider

# (3)
# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from myxml.items import MyxmlItem


class MyxmlspiderSpider(XMLFeedSpider):
    name = 'myxmlspider'
    allowed_domains = ['sina.com.cn']
    # 设置要分析的XML文件地址
    start_urls = ['http://blog.sina.com.cn/rss/1615888477.xml']
    iterator = 'iternodes'  # you can change this; see the docs
    # 此时将开始迭代的节点设置为第一个节点rss
    itertag = 'rss'  # change it accordingly

    def parse_node(self, response, node):
        i = MyxmlItem()
        # 利用XPath表达式将对应信息提取出来，并存储到对应的Item中
        i['title'] = node.xpath("/rss/channel/item/title/text()").extract()
        i['link'] = node.xpath("/rss/channel/item/link/text()").extract()
        i['author'] = node.xpath("/rss/channel/item/author/text()").extract()
        # 通过for循环以此遍历出提取出来存在item中的信息并输出
        for j in range(len(i['title'])):
            print("第" + str(j + 1) + "篇文章")
            print("标题是：")
            print(i['title'][j])
            print("对应链接是：")
            print(i['link'][j])
            print("对应作者是：")
            print(i['author'][j])
            print("----------------------")
        return i


# (4)
D:\Python35\myweb\part12\myxml > scrapy
genspider - t
xmlfeed
person
iqianyue.com
Created
spider
'person'
using
template
'xmlfeed' in module:
myxml.spiders.person

# (5)
# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from myxml.items import MyxmlItem


class PersonSpider(XMLFeedSpider):
    name = 'person'
    allowed_domains = ['iqianyue.com']
    # 设置XML网址
    start_urls = ['http://yum.iqianyue.com/weisuenbook/pyspd/part12/test.xml']
    iterator = 'iternodes'  # you can change this; see the docs
    # 设置开始迭代的节点
    itertag = 'person'  # change it accordingly

    def parse_node(self, response, selector):
        i = MyxmlItem()
        # 提取邮件信息
        i['link'] = selector.xpath('/person/email/text()').extract()
        # 输出提取到的邮件信息
        print(i['link'])
        return i


# 12.9 学会使用CSVFeedSpider
# (1)
D:\Python35\myweb\part12 > scrapy
startproject
mycsv
New
Scrapy
project
'mycsv', using
template
directory
'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
D:\Python35\myweb\part12\mycsv

You
can
start
your
first
spider
with:
    cd
    mycsv
    scrapy
    genspider
    example
    example.com

# (2)
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
import scrapy


class MycsvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()


# (3)
D:\Python35\myweb\part12\mycsv > scrapy
genspider - t
csvfeed
mycsvspider
iqianyue.com
Created
spider
'mycsvspider'
using
template
'csvfeed' in module:
mycsv.spiders.mycsvspider

# (4)
# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider
from mycsv.items import MycsvItem


class MycsvspiderSpider(CSVFeedSpider):
    name = 'mycsvspider'
    allowed_domains = ['iqianyue.com']
    # 定义要处理的csv文件所在的网址
    start_urls = ['http://yum.iqianyue.com/weisuenbook/pyspd/part12/mydata.csv']
    # 定义headers
    headers = ['name', 'sex', 'addr', 'email']
    # 定义间隔符


delimiter = ','


# Do any adaptations you need here
# def adapt_response(self, response):
#    return response
def parse_row(self, response, row):
    i = MycsvItem()
    # 提取各行的name这一列的信息
    i['name'] = row['name'].encode()
    # 提取各行的sex这一列的信息
    i['sex'] = row['sex'].encode()
    # 进行信息输出
    print("名字是：")
    print(i['name'])
    print("性别是：")
    print(i['sex'])
    # 输出完一个记录的对应列的信息后，输出一个间隔符，显示起来方便观察
    print("--------------------")
    return i


# 12.10  Scrapy爬虫多开技能
# (1)
D:\Python35\myweb\part12 > scrapy
startproject
mymultispd
New
Scrapy
project
'mymultispd', using
template
directory
'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
D:\Python35\myweb\part12\mymultispd

You
can
start
your
first
spider
with:
    cd
    mymultispd
    scrapy
    genspider
    example
    example.com

# (2)
D:\Python35\myweb\part12 > cd
mymultispd

D:\Python35\myweb\part12\mymultispd > scrapy
genspider - t
basic
myspd1
sina.com.cn
Created
spider
'myspd1'
using
template
'basic' in module:
mymultispd.spiders.myspd1

D:\Python35\myweb\part12\mymultispd > scrapy
genspider - t
basic
myspd2
sina.com.cn
Created
spider
'myspd2'
using
template
'basic' in module:
mymultispd.spiders.myspd2

D:\Python35\myweb\part12\mymultispd > scrapy
genspider - t
basic
myspd3
sina.com.cn
Created
spider
'myspd3'
using
template
'basic' in module:
mymultispd.spiders.myspd3

# (3)
import os
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.python import without_none_values
from scrapy.exceptions import UsageError


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return "[options] <spider>"

    def short_desc(self):
        # 命令描述信息，可以根据个人喜好适当修改一下
        return "Run all spider"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        if opts.output:
            if opts.output == '-':
                self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
            else:
                self.settings.set('FEED_URI', opts.output, priority='cmdline')
            feed_exporters = without_none_values(
                self.settings.getwithbase('FEED_EXPORTERS'))
            valid_output_formats = feed_exporters.keys()
            if not opts.output_format:
                opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
            if opts.output_format not in valid_output_formats:
                raise UsageError("Unrecognized output format '%s', set one"
                                 " using the '-t' switch or as a file extension"
                                 " from the supported list %s" % (opts.output_format,
                                                                  tuple(valid_output_formats)))
            self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')

    # 主要修改这里
    def run(self, args, opts):
        # 获取爬虫列表
        spd_loader_list = self.crawler_process.spider_loader.list()
        # 遍历各爬虫
        for spname in spd_loader_list or args:
            self.crawler_process.crawl(spname, **opts.spargs)
            print("此时启动的爬虫为：" + spname)
        self.crawler_process.start()


# 12.11 避免被ban
# (1)
# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.7

# (2)
# IP池设置
IPPOOL = [
    {"ipaddr": "121.33.226.167:3128"},
    {"ipaddr": "118.187.10.11:80"},
    {"ipaddr": "123.56.245.138:808"},
    {"ipaddr": "139.196.108.68:80"},
    {"ipaddr": "36.250.87.88:47800"},
    {"ipaddr": "123.57.190.51:7777"},
    {"ipaddr": "171.39.26.176:8123"}
]

# (3)
# middlewares下载中间件
# 导入随机数模块，目的是随机挑选一个IP池中的ip
import random
# 从settings文件（myfirstpjt.settings为settings文件的地址）中导入设置好的IPPOOL
from myfirstpjt.settings import IPPOOL
# 导入官方文档中HttpProxyMiddleware对应的模块
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware


class IPPOOLS(HttpProxyMiddleware):
    # 初始化方法
    def __init__(self, ip=''):
        self.ip = ip

    # process_request()方法，主要进行请求处理
    def process_request(self, request, spider):
        # 先随机选择一个IP
        thisip = random.choice(IPPOOL)
        # 输出当前选择的IP，便于调试观察
        print("当前使用的IP是：" + thisip["ipaddr"])
        # 将对应的IP实际添加为具体的代理，用该IP进行爬取
        request.meta["proxy"] = "http://" + thisip["ipaddr"]


# (4)
DOWNLOADER_MIDDLEWARES = {
    # 'myfirstpjt.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 123,
    'myfirstpjt.middlewares.IPPOOLS': 125
}

# (5)
# 用户代理（user-agent）池设置
UAPOOL = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5"
]

# (6)
# uamid下载中间件
import random
from myfirstpjt.settings import UAPOOL
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


class Uamid(UserAgentMiddleware):
    def __init__(self, ua=''):
        self.ua = ua

    def process_request(self, request, spider):
        thisua = random.choice(UAPOOL)
        print("当前使用的user-agent是：" + thisua)
        request.headers.setdefault('User-Agent', thisua)


# (7)
# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'myfirstpjt.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 2,
    'myfirstpjt.uamid.Uamid': 1
}


#第19章千图网图片爬虫项目
#
#（1）
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QtpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#建立picurl存储图片的网址
    picurl=scrapy.Field()
#建立picid存储图片网址中的图片名，以方便构造本地文件名
    picid=scrapy.Field()

#（2）
# -*- coding: utf-8 -*-
import urllib.request
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QtpjtPipeline(object):
    def process_item(self, item, spider):
#一个图片列表页中有多张图片，通过for循环依次将图片存储到本地
        for i in range(0,len(item["picurl"])):
            thispic=item["picurl"][i]
#根据上面总结的规律构造出原图片的URL地址
            trueurl=thispic+"_1024.jpg"
#构造出图片在本地存储的地址
            localpath = "D:/Python35/myweb/part19/pic/" + item["picid"][i] + ".jpg"
#通过urllib.request.urlretrieve()将原图片下载到本地
            urllib.request.urlretrieve(trueurl, filename=localpath)
        return item

#（3）
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'qtpjt.pipelines.QtpjtPipeline': 300,
}


#（4）
# -*- coding: utf-8 -*-
import scrapy
import re
from qtpjt.items import QtpjtItem
from scrapy.http import Request

class QtspdSpider(scrapy.Spider):
    name = "qtspd"
    allowed_domains = ["58pic.com"]
    start_urls = (
        'http://www.58pic.com/tb/',
    )

    def parse(self, response):
        item=QtpjtItem()
#构建提取缩略图网址的正则表达式
        paturl="(http://pic.qiantucdn.com/58pic/.*?).jpg"
        #提取对应图片网址
item["picurl"]=re.compile(paturl).findall(str(response.body))
#构造出提取图片名的正则表达式，以方便构造出本地的文件名
        patlocal = "http://pic.qiantucdn.com/58pic/.*?/.*?/.*?/(.*?).jpg"
#提取互联网中的图片名
        item["picid"] = re.compile(patlocal).findall(str(response.body))
        yield item
#通过for循环依次遍历1到200页图片列表页
        for i in range(1,201):
#构造出下一页图片列表页的网址
            nexturl="http://www.58pic.com/tb/id-"+str(i)+".html"
            yield Request(nexturl, callback=self.parse)




#第16章CrawlSpider
#16.1 初识CrawSpider
#（1）
D:\Python35\myweb\part16>scrapy startproject mycwpjt
New Scrapy project 'mycwpjt', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part16\mycwpjt
You can start your first spider with:
    cd mycwpjt
    scrapy genspider example example.com

#（2）
D:\Python35\myweb\part16\mycwpjt>scrapy genspider -t crawl weisuen sohu.com
Created spider 'weisuen' using template 'crawl' in module:
  Mycwpjt.spiders.weisuen

#16.2 链接提取器
#（1）
rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

#（2）
 rules = (
        Rule(LinkExtractor(allow=('.shtml')), callback='parse_item', follow=True),
    )

#（3）
rules = (
        Rule(LinkExtractor(allow=('.shtml'),allow_domains=(sohu.com)), callback='parse_item', follow=True),
    )

#16.3 实战CrawSpider实例
#（1）
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MycwpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    link=scrapy.Field()

#（2）
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MycwpjtPipeline(object):
    def process_item(self, item, spider):
        print(item["name"])
        print(item["link"])
        print("-------------------")
        return item

#（3）
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'mycwpjt.pipelines.MycwpjtPipeline': 300,
}

#（4）
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mycwpjt.items import MycwpjtItem


class WeisuenSpider(CrawlSpider):
    name = 'weisuen'
    allowed_domains = ['sohu.com']
    start_urls = ['http://news.sohu.com/']

    rules = (
#新闻网页的url地址类似于：
#“http://news.sohu.com/20160926/n469167364.shtml”
#所以可以得到提取的正则表达式为'.*?/n.*?shtml’
        Rule(LinkExtractor(allow=('.*?/n.*?shtml'),allow_domains=('sohu.com')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = MycwpjtItem()
#根据Xpath表达式提取新闻网页中的标题
        i["name"]=response.xpath("/html/head/title/text()").extract()
#根据Xpath表达式提取当前新闻网页的链接
        i["link"]=response.xpath("//link[@rel='canonical']/@href").extract()
        return i

#（5）
 rules = (
        Rule(LinkExtractor(allow=('.*?/n.*?shtml'),allow_domains=('sohu.com')), callback='parse_item', follow=False),
    )





#第17章Scrapy高级应用
#17.1 Python3如何操作数据库
#(1)
D:\Python35\myweb\part16\mycwpjt>pip install pymysql3
Collecting pymysql3
  Downloading PyMySQL3-0.5.tar.gz
running egg_info
……
  Stored in directory: C:\Users\Administrator.USER-20160828PN\AppData\Local\pip\Cache\wheels\bf\84\b3\c2cb0d3d8e99f408976e112f65ba4780cbfb446a606dd620db
Successfully built pymysql3
Installing collected packages: pymysql3
Successfully installed pymysql3-0.5

#(2)
>>> cs=conn1.cursor()
>>> cs.execute("select * from mytb")
1
>>> for i in cs:
	print("当前是第"+str(cs.rownumber)+"行")
	print("标题是："+i[0])
	print("关键词是："+i[1])

#17.2 爬取内容写进MySQL
#(1)
D:\Python35\myweb\part17>scrapy startproject mysqlpjt
New Scrapy project 'mysqlpjt', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part17\mysqlpjt
You can start your first spider with:
    cd mysqlpjt
    scrapy genspider example example.com

#(2)
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MysqlpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #建立name存储网页标题
    name=scrapy.Field()
    #建立keywd存储网页关键词
    keywd=scrapy.Field()

#(3)
# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MysqlpjtPipeline(object):
    def __init__(self):
        #刚开始时连接对应数据库
        self.conn=pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="mypydb")
    def process_item(self, item, spider):
        #将获取到的name和keywd分别赋给变量name和变量key
        name=item["name"][0]
        key=item["keywd"][0]
        #构造对应的sql语句
        sql="insert into mytb(title,keywd) VALUES('"+name+"','"+key+"')"
        #通过query实现执行对应的sql语句
        self.conn.query(sql)
        return item
    def close_spider(self,spider):
        self.conn.close()

#(4)
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'mysqlpjt.pipelines.MysqlpjtPipeline': 300,
}

#(5)
D:\Python35\myweb\part17\mysqlpjt>scrapy genspider -t crawl weiwei sina.com.cn
Created spider 'weiwei' using template 'crawl' in module:
  Mysqlpjt.spiders.weiwei

#(6)
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mysqlpjt.items import MysqlpjtItem


class WeiweiSpider(CrawlSpider):
    name = 'weiwei'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/']

    rules = (
        Rule(LinkExtractor(allow=('.*?/[0-9]{4}.[0-9]{2}.[0-9]{2}.doc-.*?shtml'),allow_domains=('sina.com.cn')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = MysqlpjtItem()
        #通过xpath表达式提取网页标题
        i["name"]=response.xpath("/html/head/title/text()").extract()
        #通过xpath表达式提取网页的关键词
        i["keywd"]=response.xpath("/html/head/meta[@name='keywords']/@content").extract()
        return i

#(7)
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#(8
   def __init__(self, host="localhost", user=None, passwd="",
                 db=None, port=3306, unix_socket=None,
                 charset='utf8', sql_mode=None,
                 read_default_file=None, conv=decoders, use_unicode=None,
                 client_flag=0, cursorclass=Cursor, init_command=None,
                 connect_timeout=None, ssl=None, read_default_group=None,
                 compress=None, named_pipe=None):







)


# 第14章Scrapy中文输出与存储
# 14.1 Scrapy的中文输出
# (1)
# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class MypjtItem(scrapy.Item):
    # define the fields for your item here like:
    # 定义title，用来存储网页标题信息
    title = scrapy.Field()


# (2)
# -*- coding: utf-8 -*-
import scrapy
# 导入items文件中的MypjtItem
from mypjt.items import MypjtItem


class MyspdSpider(scrapy.Spider):
    name = "myspd"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
        # 定义要抓取的起始网址为新浪首页
        'http://www.sina.com.cn/',
    )

    def parse(self, response):
        # 初始化item
        item = MypjtItem()
        # 通过Xpath表达式提取该网页中的标题信息
        item["title"] = response.xpath("/html/head/title").extract()
        # 输出提取到的标题信息
        print
        item["title"]


# (3)
# -*- coding: utf-8 -*-
import scrapy
from mypjt.items import MypjtItem


class MyspdSpider(scrapy.Spider):
    name = "myspd"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
        'http://www.sina.com.cn/',
    )

    def parse(self, response):
        item = MypjtItem()
        item["title"] = response.xpath("/html/head/title").extract()
        # print item["title"]
        # item["title"]是一个列表，所以我们可以通过for循环遍历出该列表中的元素
        for i in item["title"]:
            # 对遍历出来的标题信息进行encode("gbk")编码
            print
            i.encode("gbk")


# (4)
D:\Python35\myweb\part13 > scrapy
startproject
mypjt
New
Scrapy
project
'mypjt', using
template
directory
'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
D:\Python35\myweb\part13\mypjt

You
can
start
your
first
spider
with:
    cd
    mypjt
    scrapy
    genspider
    example
    example.com

# (5)
# -*- coding: utf-8 -*-
import scrapy


class MypjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()


# (6)
# -*- coding: utf-8 -*-
import scrapy
from mypjt.items import MypjtItem


class WeisuenSpider(scrapy.Spider):
    name = "weisuen"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
        # 设置起始网址为新浪新闻下的某个新闻网页
        'http://tech.sina.com.cn/d/s/2016-09-17/doc-ifxvyqwa3324638.shtml',
    )

    def parse(self, response):
        item = MypjtItem()
        # 通过Xpath表达式提取网页中的标题信息
        item["title"] = response.xpath("/html/head/title/text()")
        # 直接输出，在Python3.X中，虽然包含中文信息，但直接输出即可
        print(item["title"])


# 14.2 Scrapy的中文存储
# (1)
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 本项目中在pipelines文件里面的类是MypjtPipeline，接下来会具体看到
    'mypjt.pipelines.MypjtPipeline': 300,
}

# (2)
# -*- coding: utf-8 -*-
# 导入codecs模块，使用codecs直接进行解码
import codecs


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 定义了pipelines里面的类，类名需要与刚才settings.py里面设置的类名对应起来
class MypjtPipeline(object):
    # __init__()为类的初始化方法，开始的时候调用
    def __init__(self):
        # 首先以写入的方式创建或打开一个普通文件用于存储抓取到的数据
        self.file = codecs.open("D:/python35/myweb/part13/mydata1.txt", "wb", encoding="utf-8")

    # process_item()为pipelines中的主要处理方法，默认会自动调用
    def process_item(self, item, spider):
        # 设置每行要写的内容
        l = str(item) + '\n'
        # 此处通过print()输出，方便程序的调试
        print(l)
        # 将对应信息写入文件中
        self.file.write(l)
        return item

    # close_spider()方法一般在关闭蜘蛛时调用
    def close_spider(self, spider):
        # 关闭文件，有始有终
        self.file.close()


# 14.3 输出中文到json文件
# (1)
# -*- coding: utf-8 -*-
import codecs
# 因为要进行JSON文件的处理，所以导入json模块
import json


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
class MypjtPipeline(object):
    def __init__(self):
        # 以写入的方式创建或打开一个json格式（后缀名为.json）的文件
        self.file = codecs.open("D:/python35/myweb/part13/mydata1.json", "wb", encoding="utf-8")

    def process_item(self, item, spider):
        # 通过dict(item)将item转化成一个字典
        # 然后通过json模块下的dumps()处理字典数据
        i = json.dumps(dict(item))
        # 得到的数据后加上”\n”换行符形成要写入的一行数据
        line = i + '\n'
        # 在此进行直接输出，方便调试，实际的时候输出这一行可以去掉
        print(line)
        # 写入数据到json文件中
        self.file.write(line)
        return item

    def close_spider(self, spider):
        # 关闭文件，有始有终
        self.file.close()


# (2)
# -*- coding: utf-8 -*-
import codecs
import json


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MypjtPipeline(object):
    def __init__(self):
        self.file = codecs.open("D:/python35/myweb/part13/mydata1.json", "wb", encoding="utf-8")

    def process_item(self, item, spider):
        # 通过json模块下的dumps()处理的时候
        # 第二个参数将ensure_ascii设置为False
        i = json.dumps(dict(item), ensure_ascii=False)
        line = i + '\n'
        print(line)
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

    # (3)


start_urls = (
    'http://tech.sina.com.cn/d/s/2016-09-17/doc-ifxvyqwa3324638.shtml',
    "http://sina.com.cn",
)

# (4)
item["title"] = response.xpath("/html/head/title/text()").extract()
item["key"] = response.xpath("//meta[@name='keywords']/@content").extract()


#第15章编写自动爬取网页的爬虫
#15.1 实战items编写
#（1）
D:\Python35\myweb\part15>scrapy startproject autopjt
New Scrapy project 'autopjt', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part15\autopjt
You can start your first spider with:
    cd autopjt
    scrapy genspider example example.com

#(2)
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutopjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#定义好name用来存储商品名
    name=scrapy.Field()
#定义好price用来存储商品价格
    price=scrapy.Field()
#定义好link用来存储商品链接
    link=scrapy.Field()
#定义好comnum用来存储商品评论数
    comnum=scrapy.Field()


#15.2 实战pipelines编写
#(1)
# -*- coding: utf-8 -*-
import codecs
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutopjtPipeline(object):
    def __init__(self):
#打开mydata.json文件
        self.file = codecs.open("D:/python35/myweb/part15/mydata.json", "wb", encoding="utf-8")
    def process_item(self, item, spider):
        i=json.dumps(dict(item), ensure_ascii=False)
#每条数据后加上换行
        line = i + '\n'
#写入数据到mydata.json文件中
        self.file.write(line)
        return item
    def close_spider(self,spider):
#关闭mydata.json文件
        self.file.close()

#(2)
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'autopjt.pipelines.AutopjtPipeline': 300,
}

#(3)
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

#15.4 自动爬虫编写实战
#(1)
D:\Python35\myweb\part15>cd .\autopjt\
D:\Python35\myweb\part15\autopjt>scrapy genspider -t basic autospd dangdang.com
Created spider 'autospd' using template 'basic' in module:
  Autopjt.spiders.autospd

#(2)
# -*- coding: utf-8 -*-
import scrapy
from autopjt.items import AutopjtItem
from scrapy.http import Request

class AutospdSpider(scrapy.Spider):
    name = "autospd"
    allowed_domains = ["dangdang.com"]
    start_urls = (
        'http://category.dangdang.com/pg1-cid4002203.html',
    )

    def parse(self, response):
        item=AutopjtItem()
#通过各Xpath表达式分别提取商品的名称、价格、链接、评论数等信息
        item["name"]=response.xpath("//a[@class='pic']/@title").extract()
        item["price"]=response.xpath("//span[@class='price_n']/text()").extract()
        item["link"]=response.xpath("//a[@class='pic']/@href").extract()
        item["comnum"]=response.xpath("//a[@name='P_pl']/text()").extract()
#提取完后返回item
        yield item
#接下来很关键，通过循环自动爬取75页的数据
        for i in range(1,76):
#通过上面总结的网址格式构造要爬取的网址
            url="http://category.dangdang.com/pg"+str(i)+"-cid4002203.html"
#通过yield返回Request，并指定要爬取的网址和回调函数
#实现自动爬取
            yield Request(url, callback=self.parse)

#15.5 调试与运行
#（1）
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#（2）
# -*- coding: utf-8 -*-
import codecs
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutopjtPipeline(object):
    def __init__(self):
#此时存储到的文件是mydata2.json，不与之前存储的文件mydata.json冲突
        self.file = codecs.open("D:/python35/myweb/part15/mydata2.json", "wb", encoding="utf-8")
    def process_item(self, item, spider):
        #item=dict(item)
        #print(len(item["name"]))
#每一页中包含多个商品信息，所以可以通过循环，每一次处理一个商品
#其中len(item["name"])为当前页中商品的总数，依次遍历
        for j in range(0,len(item["name"])):
#将当前页的第j个商品的名称赋值给变量name
            name=item["name"][j]
            price=item["price"][j]
            comnum=item["comnum"][j]
            link=item["link"][j]
#将当前页下第j个商品的name、price、comnum、link等信息处理一下
#重新组合成一个字典
            goods={"name":name,"price":price,"comnum":comnum,"link":link}
            #将组合后的当前页中第j个商品的数据写入json文件
i=json.dumps(dict(goods), ensure_ascii=False)
            line = i + '\n'
            self.file.write(line)
#返回item
        return item
    def close_spider(self,spider):
        self.file.close()


#第四章
#4.2  快速使用Urllib扒取网页
#(1)
>>> import urllib.request

#(2)
>>> file=urllib.request.urlopen("http://www.baidu.com")

#(3)
>>> data=file.read()
>>> dataline=file.readline()

#(4)
>>> print(dataline)

#(5)
>>> print(data)

#(6)
>>> fhandle=open("D:/Python35/myweb/part4/1.html","wb")
>>> fhandle.write(data)
99437
>>> fhandle.close()

#(7)
>>>filename=urllib.request.urlretrieve("http://edu.51cto.com",filename="D:/Python35/myweb/part4/2.html")

#(8)
>>> urllib.request.urlcleanup()

#(9)
>>> file.info()
<http.client.HTTPMessage object at 0x0000000003623D68>

#(10)
>>> file.getcode()
200

#(11)
>>> file.geturl()
'http://www.baidu.com'

#(12)
>>> urllib.request.quote("http://www.sina.com.cn")
'http%3A//www.sina.com.cn'

#(13)
>>> urllib.request.unquote("http%3A//www.sina.com.cn")
'http://www.sina.com.cn'

#4.3  浏览器的完全模拟--Headers属性
#(1)
>>> import urllib.request
>>> url= "http://blog.csdn.net/weiwei_pig/article/details/51178226"
>>> file=urllib.request.urlopen(url)

#(2)
mport urllib.request
url= "http://blog.csdn.net/weiwei_pig/article/details/51178226"
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
data=opener.open(url).read()

#(3)
>>> fhandle=open("D:/Python35/myweb/part4/3.html","wb")
>>> fhandle.write(data)
47630
>>> fhandle.close()

#(4)
import urllib.request
url= "http://blog.csdn.net/weiwei_pig/article/details/51178226"
req=urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
data=urllib.request.urlopen(req).read()

#4.4  超时设置
#(1)
import urllib.request
for i in range(1,100):
    try:
        file=urllib.request.urlopen("http://yum.iqianyue.com",timeout=1)
        data=file.read()
        print(len(data))
    except Exception as e:
        print("出现异常-->"+str(e))
#(2)
import urllib.request
for i in range(1,100):
    try:
        file=urllib.request.urlopen("http://yum.iqianyue.com",timeout=30)
        data=file.read()
        print(len(data))
    except Exception as e:
        print("出现异常-->"+str(e))

#4.5  HTTP协议请求实战
#(1)
mport urllib.request
keywd="hello"
url="http://www.baidu.com/s?wd="+keywd
req=urllib.request.Request(url)
data=urllib.request.urlopen(req).read()
fhandle=open("D:/Python35/myweb/part4/4.html","wb")
fhandle.write(data)
fhandle.close()

#(2)
import urllib.request
url="http://www.baidu.com/s?wd="
key="韦玮老师"
key_code=urllib.request.quote(key)
url_all=url+key_code
req=urllib.request.Request(url_all)
data=urllib.request.urlopen(req).read()
fh=open("D:/Python35/myweb/part4/5.html","wb")
fh.write(data)
fh.close()

#(3)
import urllib.request
import urllib.parse
url = "http://www.iqianyue.com/mypost/"
postdata =urllib.parse.urlencode({
"name":"ceo@iqianyue.com",
"pass":"aA123456"
}).encode('utf-8') #将数据使用urlencode编码处理后，使用encode()设置为utf-8编码
req = urllib.request.Request(url,postdata)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
data=urllib.request.urlopen(req).read()
fhandle=open("D:/Python35/myweb/part4/6.html","wb")
fhandle.write(data)
fhandle.close()

#4.6  瞒天过海之代理服务器的设置
#(1)
def use_proxy(proxy_addr,url):
    import urllib.request
    proxy= urllib.request.ProxyHandler({'http':proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    return data
proxy_addr="202.75.210.45:7777"
data=use_proxy(proxy_addr,"http://www.baidu.com")
print(len(data))

#4.7  DebugLog实战
#(1)
import urllib.request
httphd=urllib.request.HTTPHandler(debuglevel=1)
httpshd=urllib.request.HTTPSHandler(debuglevel=1)
opener=urllib.request.build_opener(httphd,httpshd)
urllib.request.install_opener(opener)
data=urllib.request.urlopen("http://edu.51cto.com")

#4.8  异常处理神器--URLError实战
#(1)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.URLError as e:
    print(e.code)
    print(e.reason)

#(2)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)

#(3)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.baidusss.net")
except urllib.error.HTTPError as e:
    print(e.reason)

#(4)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.baidusss.net")
except urllib.error.URLError as e:
    print(e.reason)

#(5)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.baidusss.net")
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)
except urllib.error.URLError as e:
    print(e.reason)

#(6)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://www.baidussssss.net")
except urllib.error.URLError as e:
    print(e.code)
    print(e.reason)

#(7)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.URLError as e:
    if hasattr(e,"code"):
        print(e.code)
    if hasattr(e,"reason"):
        print(e.reason)
