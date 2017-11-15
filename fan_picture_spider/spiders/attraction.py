# -*- coding: utf-8 -*-
import scrapy
import time
import re

from selenium import webdriver
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from fan_picture_spider.items import AttractionItem

class Attraction(scrapy.Spider):
    name = 'attraction'
    attraction = 0

    start_urls = [
        'https://www.tripadvisor.cn/Attractions-g294197-Activities-Seoul.html'
    ]

    # 获取景点列表
    def parse(self, response):
        list_ = response.xpath('//div[@id="FILTERED_LIST"]')
        url_list = list_.css('div.listing_commerce a');
        for url in url_list[:1]: # [:]
            self.attraction += 1
            yield response.follow(url, callback=self.parse_item_picture)

        # 获取下一页链接
        if self.attraction < self.settings.get('ATTRACTION_COUNT'): # 50
            for next_page in response.css('div.pagination a.next'):
                yield response.follow(next_page, callback=self.parse)

    # 获取原图链接
    def parse_item_picture(self, response):
        pictures = response.selector.css('div[data-bigurl]::attr(data-bigurl)')
        attraction_url = response.request.url
        picture_count = self.settings.get('PICTURE_COUNT')
 
        for picture in pictures[:picture_count]:
            loader = ItemLoader(item=AttractionItem(), response=response)
            loader.add_value('id', re.findall(r'-*d(\d+)-', attraction_url)[0])
            loader.add_value('group_id', re.findall(r'-*g(\d+)-',
                            attraction_url)[0])
            loader.add_value('url', attraction_url)
            loader.add_value('pic_url', picture.extract())
            yield loader.load_item()
