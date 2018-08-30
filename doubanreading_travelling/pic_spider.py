# -×- coding:utf-8 -*-


import re #解析不合适
import urllib.request
import requests
from lxml import etree  #解析不合适
from bs4 import BeautifulSoup
import time




def call_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080'}

    res = requests.get(url,headers=headers)
    if res.status_code == 200:
        return res.text
    return None
# //a/@title
#解析时尝试bs4把一块数据弄下来，然后再用re遍历切割！
def parse_page(html):
#想办法把两个Beautifulsoup分别取下来后，再拼接为一个新的字符串形式，再用正则进行匹配
    # 把图片链接和名称打包在一起  #提出空格和提出特殊字符纠结在一起  直接上正则即可！
    patt = re.compile('<img class="" src="(.*?)"' + '.*?title="(.*?)"',re.S)
    items = re.findall(patt,html)
    for item in items:
        # item[0]是图片链接， item[1]是书名
        link = item[0]
        title = item[1]
        # 针对斜杠的书名游标转义一下  用‘’字符串话，这样才比较好用原始字符串 还是思考作为一个一次处理
        # urllib.request.urlretrieve(link,'/home/karson/pics/%s'% (r'%s'%title))
        try:
            urllib.request.urlretrieve(link,'/home/karson/pics/%s'% (r'%s'%title))
        except FileNotFoundError :
            pass

        print('下载完成了')







if __name__ == '__main__':
    for offset in range(0,1000,20):
        url = 'https://book.douban.com/tag/%E6%97%85%E8%A1%8C?start='+str(offset)+'&type=T'
        content = call_page(url)
        parse_page(content)
        print(offset)
        time.sleep(2)





