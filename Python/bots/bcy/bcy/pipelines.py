# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem  
from os import system

class DuplicatesPipeline(object):  
  
    def __init__(self):  
        self.ids_seen = set()  

    def process_item(self, item, spider):  
        if item['url'] in self.ids_seen:  
            raise DropItem("Duplicate item found: %s" % item['title'])  
        else:  
            self.ids_seen.add(item['url'])  
            return item

class BcyPipeline(object):
    def process_item(self, item, spider):
        if item['title'] == '':
            item['title'] = "%s_%s" % (item['cp_id'], item['rp_id'])
        item['author'] = item['author'].encode('utf-8', 'ignore')
        item['title'] = item['title'].encode('utf-8', 'ignore')

        path = 'output/%s/%s' % (item['author'], item['title'])
        # path = path.encode('utf-8', 'ignore')
        system("mkdir -p '%s'" % path)
        ofilename = '%s/../%s_%s.list' % (path, item['cp_id'].encode('utf-8', 'ignore'), item['rp_id'])
        ofs = open(ofilename, 'w')

        for picurl in item['pics']:
            system("wget -c -P '%s' '%s'" % (path, picurl.encode('utf-8')))
            ofs.write("%s\n" % picurl.encode('utf-8'))
        
        ofs.close()
        return item['title'] + ' complete'
