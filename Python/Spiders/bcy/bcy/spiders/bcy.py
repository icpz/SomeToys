# -*- coding: utf-8 -*-

import scrapy

class BcySpider(scrapy.Spider): 
    name = 'bcy'
    allowed_domains = ["bcy.net"]
    start_urls = [
            'http://bcy.net/coser'
            ]
    
    def parse(self, response):
        for a in response.xpath("//div[@class='l-grid__item newThumbnail newThumbnail--118x220 js-img-error']/a"):
            for t in a.xpath('@title'): print t.extract()
            for u in a.xpath('@href'): print u.extract()
            # for author in a.xpath('@
