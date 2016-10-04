#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
from lxml import html
import json
import time
import re

def make_sure_output_path(nickname):
    if not os.path.exists('./output'):
        os.mkdir('output')

    prefix = './output/%s' % nickname
    if not os.path.exists(prefix):
        os.mkdir('output/%s' % nickname)
    return prefix.encode('utf-8')

def get_userid_and_worknum(uid):
    url = 'http://changba.com/u/%s' % uid
    r = requests.get(url)
    r.encoding = 'utf-8'
    key = 'userid = \''
    start_pos = r.text.find(key)
    end_pos = r.text.find('\';', start_pos)
    userid = r.text[start_pos + len(key) : end_pos]
    key = 'worknum = '
    start_pos = r.text.find(key, start_pos)
    end_pos = r.text.find(';', start_pos)
    worknum = r.text[start_pos + len(key) : end_pos]
    nickname = html.fromstring(r.text).xpath('//title/text()')[0]
    return userid, worknum, nickname[:nickname.find(u'个人主页')]

def get_work_list(userid, worknum):
    worknum = int(worknum)
    page_sum = worknum / 20;
    if worknum % 20 != 0:
        page_sum += 1

    work_list = []

    for i in range(page_sum):
        url = 'http://changba.com/member/personcenter/loadmore.php?ver=1&pageNum=%d&type=0&userid=%s&curuserid=-1' % (i, userid)
        r = requests.get(url)
        work_list += json.loads(r.text)

    return work_list

def parse_song_address(enworkid):
    url = 'http://changba.com/s/%s' % enworkid
    r = requests.get(url)
    a = re.findall(r'var a="(http[s]*://[^/]+/[\w\/]+.mp3)"', r.text.encode('utf-8'))[0]
    c = re.findall(r'userwork/([abc])(\d+)/(\w+)/(\w+).mp3', a)
    if c:
        c = c[0]
        d = c[0]
        e = int(c[1], 8)
        f = int(c[2], 16) / e / e
        g = int(c[3], 16) / e / e
        if d == 'a' and g % 0x1e3 == f:
            a = 'http://a%dmp3.changba.com/userdata/userwork/%d/%d.mp3' % (e, f, g)
        elif d == 'c':
            a = 'http://aliuwmp3.changba.com/userdata/userwork/%d.mp3' % g
    return a

def download_list(work_list, prefix):
    for song in work_list:
        filename = '%s_%s' % (song['songname'], song['workid'])
        filename = filename.encode('utf-8')
        try:
            address = parse_song_address(song['enworkid'])
        except IndexError:
            time.sleep(2)
            address = parse_song_address(song['enworkid'])
        os.system('wget %s -O %s/%s.mp3' % (address, prefix, filename))

def main():
    with open('./cfg/config.ini', 'r') as ifs:
        uid = ifs.readline().strip('\n')
    userid, worknum, nick_name = get_userid_and_worknum(uid)
    work_list = get_work_list(userid, worknum)
    prefix = make_sure_output_path(nick_name)
    download_list(work_list, prefix)

if __name__ == '__main__':
    main()


