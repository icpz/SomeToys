# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from PIL import Image
import io
import binascii

class CoreCourse(CrawlSpider):
    name = 'CoreCourse'
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
            return

        print 'login success'
        yield scrapy.Request(url = 'http://electsys.sjtu.edu.cn/edu/student/CoreCourses.aspx',
                             meta = response.meta,
                             callback = self.process_course)

    def process_course(self, response):
        n = -1 + len(response.xpath('//body/form//*[@id="dgSet"]/tr'))
        xpath_fmt = '//body/form//*[@id="dgSet"]/tr[%d]/td[%d]/font/text()'
        
        sumscore = 0
        summark = 0.0

        def process_score(score):
	    scoremap = {
		    'A+' : 95,
		    'A' : 90,
		    'A-' : 85,
		    'B+' : 80,
		    'B' : 75,
		    'B-' : 70
		}
	    result = 0
	    try:
		result = int(score)
	    except ValueError:
		result = scoremap[score.split()[0]]
	    return result
        
        for i in range(1, n + 1):
            score = response.xpath(xpath_fmt % (i + 1, 8)).extract()[0]
            score = process_score(score)
            mark = float(response.xpath(xpath_fmt % (i + 1, 9)).extract()[0])
            sumscore += mark * score
            summark += mark
        
        print sumscore / summark


