from pyquery import PyQuery as pq
import requests
import os
import os.path
import time
from multiprocessing.dummy import Pool as ThreadPool

def get_urls():
    pagenum = 1
    urls = []
    while True:
        url = 'https://avmo.pw/cn/star/{}/page/{}'.format(keyword,str(pagenum))
        page = requests.get(url)
        if page.status_code == requests.codes.ok:
            pagenum += 1
            urls.append(url)
        else:
            break
    return urls

def get_imginfo(url):
    page = requests.get(url).text
    d = pq(page)
    img_url = []
    title_list = []
    for url in d('.movie-box .photo-frame img'):
        img_url.append(d(url).attr('src').replace('s.jpg', 'l.jpg'))
    for title in d('.movie-box .photo-info date:eq(0)'):
        title_list.append(d(title).text())
    return [[img_url[pos], title_list[pos]] for pos in range(len(img_url))]
    
def write_img(writelist):
    for url,title in writelist:
        with open(r'./' + keyword + '/' + title + '.jpg','wb') as f:
            print('download {} {}...'.format(title, url))
            f.write(requests.get(url).content)

def main():
    starttime = time.time()
    # keyword=9oz  e.g "https://avmo.pw/cn/star/9oz" 
    global keyword
    keyword = '9qp'
    if not os.path.exists(keyword):
        os.makedirs(keyword)

    urls = get_urls()
    poolnum = 8

    pool = ThreadPool(poolnum)
    writelist = pool.map(get_imginfo, urls)
    # writelist = map(get_imginfo, urls)

    pool2 = ThreadPool(poolnum)
    pool2.map(write_img, writelist)

    pool2.close()
    pool2.join()

    endtime = time.time()
    print('Ok, all down.................')
    print('耗时{:.2f}秒'.format(endtime-starttime))

if __name__ == '__main__':
    main()
