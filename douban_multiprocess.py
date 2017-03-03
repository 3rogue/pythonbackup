# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
import xlwings as xw
from time import time
from multiprocessing.dummy import Pool as ThreadPool
# 导出我的豆瓣电影列表多线程版本
# 缺点：顺序不是按照观看的先后顺序导出的，当然作为数据库的话其实不重要，如果要求按顺序查找的话应该是去的网页版吧
# 优点：节省成吨的时间(不包括写入excel的时间)，之前单线程115秒，多线程的话只需要12秒
userid = '38278418'
url = 'https://movie.douban.com/people/{}/collect'.format(userid)
page = requests.get(url)
d = pq(page.text)
pagenum = int(d('.paginator>a:last').text())
url_list = [url + '?start={}&sort=time&rating=all&filter=all&mode=grid'.format(num*15) for num in range(pagenum)]
res = []

def parse(url):
    global res
    page = requests.get(url)
    d = pq(page.text) 
    for each in d('.grid-view .item').items():
        detail = [each('.title a').text(), each('.title a').attr('href'), each('.intro+li span:eq(0)').attr('class')[6], each('.tags').text()[4:], each('.comment').text()]
        res.append(detail)

start = time()

pool = ThreadPool(10)
result = pool.map(parse,url_list)
pool.close()
pool.join()
print('准备写入excel，请耐心等待......')
wb = xw.Book()
xw.Range('A1').value = ['片名', '评分', '标签', '短评']
length = len(res)
for i in range(length):
    xw.Range('A{}'.format(i+2)).add_hyperlink(res[i][1], text_to_display = res[i][0])
xw.Range('B2:D{}'.format(length+1)).value = [i[2:] for i in res]
wb.save('movie.xlsx')

end = time()
print('耗时{}'.format(end-start))
