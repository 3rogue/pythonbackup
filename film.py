# -*- coding: utf-8 -*-
import requests
import json
from email.mime.text import MIMEText
from email.header import Header
import smtplib

# r = requests.get('https://movie.douban.com/j/chart/top_list?type=23&interval_id=100%3A90&action=0&start=0&limit=149')
# film = {}
# for i in r.json():
#     film[str(i['rank'])+' '+i['title']] = i['url']

# with open('film.txt','w',encoding = 'utf-8') as f:
#     f.write(json.dumps(film, ensure_ascii = False))

with open(r'F:\pythonwork\film.txt','r+',encoding = 'utf-8') as f:
    film = json.load(f)
    if not film:
        first = '看光了去重新获取列表吧'
        link = 'https://movie.douban.com/typerank?type_name=%E7%9F%AD%E7%89%87&type=23&interval_id=100:90&action='
    else:
        first = list(film.keys())[0]
        link = film[first]
    # 发送邮件
    from_addr = '发件邮箱'
    password = '密码'
    to_addr = 'me@wunderlist.com'
    smtp_server = 'smtp.126.com' #smtp服务器地址
    
    msg = MIMEText(link,'plain','utf-8')

    msg['From'] = Header('<{}>'.format(from_addr))
    msg['To'] = Header('<{}>'.format(to_addr))
    msg['Subject'] = Header('今天'+first, 'utf-8')

    server = smtplib.SMTP_SSL(smtp_server, 465) 
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    del film[first]
    f.seek(0)
    f.write(json.dumps(film, ensure_ascii = False))
    f.truncate()
