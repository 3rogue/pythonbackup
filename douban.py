# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
import xlwings as xw

userid = '38278418'
url = 'https://movie.douban.com/people/{}/collect'.format(userid)

page = requests.get(url)
d = pq(page.text)
pagenum = int(d('.paginator>a:last').text())
res = []
for num in range(pagenum):
    newurl = url + '?start={}&sort=time&rating=all&filter=all&mode=grid'.format(num*15)
    page = requests.get(newurl)
    d = pq(page.text)
    for each in d('.grid-view .item').items():
        detail = [each('.title a').text(), each('.title a').attr('href'), each('.intro+li span:eq(0)').attr('class')[6], each('.tags').text()[4:], each('.comment').text()]
        res.append(detail)
    # if num == 1:
    #     break
# print(res)
print('准备写入excel，请耐心等待......')
wb = xw.Book()
xw.Range('A1').value = ['片名', '评分', '标签', '短评']
length = len(res)
for i in range(length):
    xw.Range('A{}'.format(i+2)).add_hyperlink(res[i][1], text_to_display = res[i][0])
xw.Range('B2:D{}'.format(length+1)).value = [i[2:] for i in res]

wb.save('movie.xlsx')
