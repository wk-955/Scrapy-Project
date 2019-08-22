# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from PicSpiders.items import PicspidersItem


class ShutterSpider(scrapy.Spider):
    name = 'shuttershock'
    allowed_domains = ['shuttershock.com']
    base_url = 'https://www.shutterstock.com/zh/search/{keyword}?page={page}'

    def start_requests(self):
        for page in range(self.settings.get('MAX_PAGE') + 1):
            keyword = self.settings.get('KEYWORD')
            if ' ' in keyword:
                keyword = keyword.replace(' ', '+')
            url = self.base_url.format(keyword=keyword, page=page)
            yield Request(url, callback=self.img_parse)

    def img_parse(self, response):
        item = PicspidersItem()

        img_urls = response.xpath('//img[@class="z_g_h"]//@src').extract()

        item['img_urls'] = img_urls

        yield item