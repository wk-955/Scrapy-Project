# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import shutil
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem
import os
from .settings import IMAGES_STORE, KEYWORD


class ImagesPipelinse(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['img_urls']:
            yield scrapy.Request(img_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        img_path = '%s%s' % (IMAGES_STORE, KEYWORD)
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        for i in image_paths:
            shutil.move(IMAGES_STORE + i, img_path + i.replace('full/', '/'))
        return item
