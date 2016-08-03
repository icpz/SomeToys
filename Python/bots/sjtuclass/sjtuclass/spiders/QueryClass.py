# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from PIL import Image
import io
import binascii

class QueryclassSpider(CrawlSpider):
    name = 'QueryClass'
    allowed_domains = ['sjtu.edu.cn']
    start_urls = ['http://www.sjtu.edu.cn/']
    cookiejar = None

    username = None
    password = None

    def start_requests(self):
        with open('cfg/user.ini', 'r') as ifs:
            self.username = ifs.readline()[:-1]
            self.password = ifs.readline()[:-1]

        url = 'http://electsys.sjtu.edu.cn/edu/login.aspx'
        yield scrapy.Request(url, callback = self.get_captcha, meta = { 'cookiejar' : 1 })

    def get_captcha(self, response):
        self.cookiejar = response.meta['cookiejar']
        captcha_url = 'https://jaccount.sjtu.edu.cn/jaccount/captcha'
        meta = { 'cookiejar' : self.cookiejar }
        for i in range(1, 5):
            meta.update({ response.xpath('//*[@id="login-form"]/form/input[%d]/@name' % i).extract()[0]
                        : response.xpath('//*[@id="login-form"]/form/input[%d]/@value' % i).extract()[0] })

        yield scrapy.Request(captcha_url, callback = self.login_proc, meta = meta)

    def login_proc(self, response):
        captchaImg = Image.open(io.BytesIO(response.body))
        captchaImg.show()
        captcha = raw_input('Please input captcha: ')
        form = {key : response.meta[key] for key in ['sid', 'returl', 'se', 'v']}
        form.update({'user' : self.username})
        form.update({'pass' : self.password})
        form.update({'captcha' : captcha})
        print form
        
        yield scrapy.FormRequest(url = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin',
                                 formdata = form,
                                 meta = { 'cookiejar' : self.cookiejar },
                                 dont_filter = True,
                                 callback = self.requare_class)

    def requare_class(self, response):
        if response.url.find('sdtMain') == -1:
            print response.url
            print 'login fail'
            self.start_requests()
            return

        print 'login success'
