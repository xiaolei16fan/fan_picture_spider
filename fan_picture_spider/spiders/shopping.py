# -*- coding: utf-8 -*-
import scrapy
import time
import re

from selenium import webdriver
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from fan_picture_spider.items import ShoppingItem

class Shopping(scrapy.Spider):
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

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 获取购物景点列表
    def parse(self, response):
        self.shopping += 1
        list_ = response.xpath('//div[@id="FILTERED_LIST"]')
        url_list = list_.css('div.listing_commerce a');
        for url in url_list: # [:]
            yield response.follow(url, callback=self.parse_item_picture)
        
        # 获取下一页链接
        if self.shopping < self.settings.get('SHOPPING_COUNT'): # 50
            for next_page in response.css('div.pagination a.next'):
                yield response.follow(next_page, callback=self.parse)

    # 获取原图链接
    def parse_item_picture(self, response):
        pictures = response.selector.css('div[data-bigurl]::attr(data-bigurl)')
        shopping_url = response.request.url
        picture_count = self.settings.get('PICTURE_COUNT')

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
                self.logger.info('attraction loader, url: {}, except: {}'
                                    .format(attraction_url, repr(e)))
            
            yield loader.load_item()