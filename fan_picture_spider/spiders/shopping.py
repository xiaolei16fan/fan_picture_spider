# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from fan_picture_spider.items import ShoppingItem
from scrapy_redis.spiders import RedisSpider
from scrapy.exceptions import IgnoreRequest
from scrapy.exceptions import CloseSpider

class Shopping(RedisSpider):
    name = 'shopping'
    shopping = 0

    start_urls = [
        'https://www.tripadvisor.cn/Attractions-g294197-Activities-c26-Seoul.html', #首尔
        'https://www.tripadvisor.cn/Attractions-g297884-Activities-c26-Busan.html', #釜山
        'https://www.tripadvisor.cn/Attractions-g983296-Activities-c26-Jeju_Island.html', #济州岛
        'https://www.tripadvisor.cn/Attractions-g297889-Activities-c26-Incheon.html', #仁川
        'https://www.tripadvisor.cn/Attractions-g608520-Activities-c26-Chuncheon_Gangwon_do.html', #春川市
        'https://www.tripadvisor.cn/Attractions-g1074139-Activities-c26-Samcheok_Gangwon_do.html', #三陟市
        'https://www.tripadvisor.cn/Attractions-g317126-Activities-c26-Gangneung_Gangwon_do.html', #江陵市
        'https://www.tripadvisor.cn/Attractions-g317129-Activities-c26-Sokcho_Gangwon_do.html', #束草市
    ]

    # g317129 = 0
    # g317126 = 0
    # g1074139 = 0
    # g608520 = 0
    def __init__(self, *a, **kw):
        super(Shopping, self).__init__(*a, **kw)
        for url in self.start_urls:
            region_name = re.findall(r'.*-(g\d+)-.*', url)[0]
            self.region_name = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 获取景点列表
    def parse(self, response):
        region_name = re.findall(r'.*-(g\d+)-.*', response.url)[0]
        list_ = response.xpath('//div[@id="FILTERED_LIST"]')
        url_list = list_.css('div.listing_commerce a');
        for url in url_list:
            self.shopping += 1 # 增加一个总抓取量
            self.region_name += 1 # 增加一个地区抓取量
            a = url.css('a::attr(href)').extract_first()
            self.logger.info('[当前坐标]: {} [地区]: {}'
                        .format(a, response.url))

            yield response.follow(url, callback=self.parse_item_picture)

        # 检查单个坐标
        region_count = self.settings.get('SHOPPING_REGION_COUNT')
        if self.region_name >= region_count:
            raise IgnoreRequest('单个地区 {} 坐标抓取数已达到 {} 个。'
                .format(region_name, self.region_name))

        # 检查抓取总数
        if self.shopping >= self.settings.get('SHOPPING_COUNT'):
            raise CloseSpider('总共抓取了 {} 个坐标'.format(self.shopping))

        self.logger.info('[开始进入下一页...] [当前抓取坐标数]: %d' % self.shopping)

        for next_page in response.css('div.pagination a.next'):

            yield response.follow(next_page, callback=self.parse)

    # 获取原图链接
    def parse_item_picture(self, response):
        shopping_url = response.request.url
        pictures = response.selector.css('div[data-bigurl]::attr(data-bigurl)')
        if pictures is None:
            raise IgnoreRequest('[坐标没有图片]: %s' % shopping_url)
        picture_count = self.settings.get('PICTURE_COUNT')
        self.logger.info('[总图片数]: {} [从属坐标]: {}'
                    .format(len(pictures), shopping_url))
 
        for picture in pictures[:picture_count]:
            loader = ItemLoader(item=ShoppingItem(), response=response)
            loader.add_value('id', re.findall(r'-*d(\d+)-', shopping_url)[0])
            loader.add_value('group_id', re.findall(r'-*g(\d+)-',
                            shopping_url)[0])
            loader.add_value('url', shopping_url)
            
            try:
                loader.add_value('pic_url', picture.extract())
            except Exception as e:
                loader.add_value('pic_url', None)
                self.logger.warning('shopping loader, url: {}, except: {}'
                                    .format(shopping_url, repr(e)))

            self.logger.info('[抓取的图片]: {} [从属坐标]: {}'
                        .format(picture.extract(), shopping_url))
            
            yield loader.load_item()