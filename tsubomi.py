from pyquery import PyQuery as pq
import requests
import os
import os.path
import time

def downloadpic(keyword):
    if not os.path.exists(keyword):
        os.makedirs(keyword)
    pagenum = 1
    while True:
        url = 'https://avmo.pw/cn/star/{}/page/{}'.format(keyword,str(pagenum))
        page = requests.get(url)
        if page.status_code == requests.codes.ok:    
            d = pq(page.text)
            img_url = []
            title_list = []
            for url in d('.movie-box .photo-frame img'):
                img_url.append(d(url).attr('src').replace('s.jpg', 'l.jpg'))
            for title in d('.movie-box .photo-info date:eq(0)'):
                title_list.append(d(title).text())
            for pos,name in enumerate(title_list):
                with open(r'./' + keyword + '/' + name + '.jpg','wb') as f:
                    print('download {} {}...'.format(name, img_url[pos]))
                    f.write(requests.get(img_url[pos]).content)
        else:
            print('Ok, all down.................')
            break
        pagenum += 1

def main():
    starttime = time.time()
    # keyword=9oz  e.g "https://avmo.pw/cn/star/9oz" 
    keyword = '9qp'
    downloadpic(keyword)
    endtime = time.time()
    print('耗时{:.2f}秒'.format(endtime-starttime))

if __name__ == '__main__':
    main()
