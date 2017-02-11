# -*- coding: utf-8 -*-
import requests
import os
import re
# 163 api https://github.com/yanunon/NeteaseCloudMusic/wiki/%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90API%E5%88%86%E6%9E%90

def downloadlyric(songname):
    songname = re.search(r'.*\\(.*).mp3',songname)
    songname = songname.group(1)
    headers = {'referer':'http://music.163.com', 'appver':'2.0.2'}

    r = requests.post('http://music.163.com/api/search/get/', data = {'s':songname,'limit':10, 'type':1, 'offset':0}, headers = headers)

    searchbox = []
    if r.status_code == requests.codes.ok:
        for i in r.json()['result']['songs']:
            item = {'id':i['id'], 'name':i['name'], 'artistname':i['artists'][0]['name'], 'albumname':i['album']['name'], 'time':'{}:{}'.format(i['duration']//1000//60, i['duration']//1000%60)}
            searchbox.append(item)
    if searchbox[0]['artistname'] + ' - ' + searchbox[0]['name'] == songname and searchbox[1]['artistname'] + ' - ' + searchbox[1]['name'] != songname:
        id = 0
        print('完全匹配到了，静默下载...')
    else:
        for i,detail in enumerate(searchbox):
            print('{}: {}{}{}\t{}\n'.format(i, detail['name'], detail['artistname'].center(20), detail['albumname'], detail['time']))
        id = input('在0-9选择要下载的序号：')
    songdetail = searchbox[int(id)]
    id = songdetail['id']
    r = requests.get('http://music.163.com/api/song/lyric?lv=-1&tv=-1&id={}'.format(id))

    lyric = r.json()['lrc']['lyric']
    if r.json()['tlyric']['version']:
        lyric += r.json()['tlyric']['lyric']

    with open(os.path.join(r'F:\CloudMusic\Lrc', songname+'.lrc'), 'w', encoding='utf-8') as f:
        f.write(lyric)
        print('All down.............')

def main():
    while True:
        songname = input('将歌曲拖曳至命令行(输入q退出)：')
        if songname == 'q':
            break
        downloadlyric(songname)

if __name__ == '__main__':
    main()
