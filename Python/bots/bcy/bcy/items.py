# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BcyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    cp_id = scrapy.Field()
    rp_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    # timeId = scrapy.Field()
    pics = scrapy.Field()
