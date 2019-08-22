# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductInfo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    shop = scrapy.Field()
    parameter = scrapy.Field()
    commentCount = scrapy.Field()
    goodCount = scrapy.Field()
    generalCount = scrapy.Field()
    poorCount = scrapy.Field()