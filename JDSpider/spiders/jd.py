# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import requests
from JDSpider import items


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']

    base_url = 'https://search.jd.com/Search?keyword={keyword}&enc=utf-8&wq={wq}&page={page}'
    price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{skuID}'
    commentSummaries_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={skuID}'

    def start_requests(self):
        keyword = self.settings.get('KEYWORDS')
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            url = self.base_url.format(keyword=keyword, wq=keyword, page=page)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        goods_urls = re.compile('href="(//item\.jd\.com/\d{5,20}\.html)"').findall(response.text)
        for url in goods_urls:
            url = 'https:' + url
            yield Request(url, callback=self.parse_product)

    def parse_product(self, response):
        ProductInfo = items.ProductInfo()

        # 商品名称
        name = response.xpath('/html/body/div[6]/div/div[2]/div[1]/text()').extract()[0].strip()
        # 商品链接
        url = response.xpath('/html/head/link[1]/@href').extract()[0]
        # 商品价格
        skuID = re.compile('skuid: (\d{5,25})').search(response.text).group(1)
        r = requests.get(self.price_url.format(skuID=skuID))
        price = re.compile('"op":"(.*?)"').search(r.text).group(1)
        # 商家名称
        shop = response.xpath('//*[@id="popbox"]/div/div[1]/h3/a/text()').extract()
        if shop:
            shop = shop[0]
        else:
            shop = '京东自营'
        # 评论数量
        r = requests.get(self.commentSummaries_url.format(skuID=skuID))
        commentCount = r.json()['CommentsCount'][0]['CommentCountStr']
        goodCount = r.json()['CommentsCount'][0]['GoodCountStr']
        generalCount = r.json()['CommentsCount'][0]['GeneralCountStr']
        poorCount = r.json()['CommentsCount'][0]['PoorCountStr']
        # 商品参数
        parameter = ''.join(response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]//text()').extract()). \
            replace('\n', '，').replace('>>', '').replace(' ', '').replace('更多参数', '').replace('，', ' ').strip()

        ProductInfo['name'] = name
        ProductInfo['url'] = url
        ProductInfo['price'] = price
        ProductInfo['shop'] = shop
        ProductInfo['commentCount'] = commentCount
        ProductInfo['goodCount'] = goodCount
        ProductInfo['generalCount'] = generalCount
        ProductInfo['poorCount'] = poorCount
        ProductInfo['parameter'] = parameter

        yield ProductInfo
