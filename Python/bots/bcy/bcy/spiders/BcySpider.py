# -*- coding: utf-8 -*-

import scrapy
import json
from bcy.items import BcyItem
import sys

class BcySpider(scrapy.Spider): 
    name = 'bcy'
    allowed_domains = ["bcy.net"]
    start_urls = [
            'http://bcy.net/coser'
            ]
    login_url = 'http://bcy.net/public/dologin'
    cookiejar = None

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept':'text/html;q=0.9,*/*;q=0.8',
                        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding':'gzip',
                        'Connection':'close',
                        'Referer':None
                        }

    begin = '0'
    ltime = '1470035248'
    ctime = '0'
    username = ""
    password = ""

    def start_requests(self):
        with open('cfg/ltime.ini', 'r') as ifs:
            self.ltime = ifs.readline()[:-1]
        
        with open('cfg/user.ini', 'r') as ifs:
            self.username = ifs.readline()[:-1]
            self.password = ifs.readline()[:-1]

        yield scrapy.FormRequest(
                url = self.login_url,
                headers = self.headers,
                formdata = { 
                         'email': self.username,
                         'password': self.password,
                         'remember': '1'
                    },
                meta = { 'cookiejar': 1 },
                callback = self.parseLoadPage
            )
    
    def getTimeLineRequest(self, since):
        return scrapy.FormRequest(
                url = 'http://bcy.net/home/timeline/load',
                headers = self.headers,
                formdata = {
                        'since': since
                    },
                meta = { 'cookiejar': self.cookiejar },
                callback = self.parseTimeLine
            )

    def parseLoadPage(self, response):
        self.cookiejar = response.meta['cookiejar']
        yield self.getTimeLineRequest(self.begin)

    def parseTimeLine(self, response):
        publics = json.loads(response.body)['data']
        for pub in publics:
            if pub['otype'] != 'coser': continue
            if pub['ctime'] == self.ctime: continue
            if self.ctime == '0':
                open('ltime.ini', 'w').write(pub['ctime'] + '\n')
            self.ctime = pub['ctime']
            if int(self.ctime) <= int(self.ltime): raise StopIteration

            item = BcyItem()
            item['author'] = pub['uname'] if 'uname' in pub.keys() else pub['ouname']
            detail = pub['detail']
            item['title'] = detail['title']
            item['url'] = 'http://bcy.net/coser/detail/%s/%s' % (detail['cp_id'], detail['rp_id'])
            item['rp_id'] = detail['rp_id']
            item['cp_id'] = detail['cp_id']

            yield scrapy.Request(url = item['url'], headers = self.headers,
                                 meta = { 'item': item, 'cookiejar': self.cookiejar }, callback = self.parseItem)

        ctime = publics[-1]['ctime']
        if int(self.ltime) < int(self.ctime):
            yield self.getTimeLineRequest(str(self.ctime))

    def parseItem(self, response):
        item = response.meta['item']
        item['pics'] = ['http://bcy.net/image/full?type=coser&id=%s&url=%s' % (item['rp_id'], pic.extract()[:-5])
                        for pic in response.xpath("//img[@class='detail_std detail_clickable']/@src")]
        yield item
















