# -*- coding: utf-8 -*-
import scrapy
import time
import re

from selenium import webdriver
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from fan_picture_spider.items import RestrantItem

class Restrant(scrapy.Spider):
    name = 'restrant'
    restrant = 0

    start_urls = [
        'https://www.tripadvisor.cn/Restaurants-g294197-Seoul.html', #首尔
        'https://www.tripadvisor.cn/Restaurants-g297884-Busan.html', #釜山
        'https://www.tripadvisor.cn/Restaurants-g983296-Jeju_Island.html', #济州岛
        'https://www.tripadvisor.cn/Restaurants-g297889-Incheon.html', #仁川
        'https://www.tripadvisor.cn/Restaurants-g608520-Chuncheon_Gangwon_do.html', #春川市
        'https://www.tripadvisor.cn/Restaurants-g1074139-Samcheok_Gangwon_do.html', #三陟市
        'https://www.tripadvisor.cn/Restaurants-g317126-Gangneung_Gangwon_do.html', #江陵市
        'https://www.tripadvisor.cn/Restaurants-g317129-Sokcho_Gangwon_do.html', #束草市
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 获取餐厅列表
    def parse(self, response):
        list_ = response.xpath('//div[@id="EATERY_LIST_CONTENTS"]')
        url_list = list_.css('a.property_title');
        for url in url_list: # [:]
            self.restrant += 1
            yield response.follow(url, callback=self.parse_item_picture)
        
        # 获取下一页链接
        if self.restrant < self.settings.get('RESTRANT_COUNT'): # 200
            for next_page in response.css('div.pagination a.next'):
                yield response.follow(next_page, callback=self.parse)

    # 获取原图链接
    def parse_item_picture(self, response):
        pictures = response.selector.css('div[data-bigurl]::attr(data-bigurl)')
        restrant_url = response.request.url
        picture_count = self.settings.get('PICTURE_COUNT')

        for picture in pictures[:picture_count]:
            loader = ItemLoader(item=RestrantItem(), response=response)
            loader.add_value('id', re.findall(r'-*d(\d+)-', restrant_url)[0])
            loader.add_value('group_id', re.findall(r'-*g(\d+)-',
                            restrant_url)[0])
            loader.add_value('url', restrant_url)

            try:
                loader.add_value('pic_url', picture.extract())
            except Exception as e:
                loader.add_value('pic_url', None)
                self.logger.info('attraction loader, url: {}, except: {}'
                                    .format(attraction_url, repr(e)))
            
            yield loader.load_item()
