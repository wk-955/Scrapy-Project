# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem

from JDSpider import settings



class JDPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        db = clinet[settings.MONGODB_DBNAME]
        self.Products = db[settings.KEYWORDS]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing {0}!'.format(data))
        if valid:
            self.Products.insert(dict(item))
            return item


