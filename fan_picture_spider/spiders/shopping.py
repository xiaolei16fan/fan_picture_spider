# -*- coding: utf-8 -*-
import scrapy
import time
import re

from selenium import webdriver
from scrapy.http import TextResponse

class Shopping(scrapy.Spider):
    name = 'shopping'
    page = 0

    start_urls = [
        'https://www.tripadvisor.cn/Restaurants-g294197-c26-Seoul.html'
    ]

    # 获取餐厅列表
    def parse(self, response):
        self.page += 1
        list_ = response.xpath('//div[@id="EATERY_LIST_CONTENTS"]')
        url_list = list_.css('a.property_title');
        for url in url_list[:1]:
            yield response.follow(url, callback=self.parse_item_picture)
        
        # 获取下一页链接
        if self.page < 2:
            for next_page in response.css('div.pagination a.next'):
                yield response.follow(next_page, callback=self.parse)

    # 获取原图链接
    def parse_item_picture(self, response):
        pictures = response.selector.css('div[data-bigurl]::attr(data-bigurl)')
        attraction_url = response.request.url
        for picture in pictures[:10]:
            yield {
                'pic_url': picture.extract(),
                'attraction_id': re.findall(r'-*d(\d+)-', attraction_url)[0],
                'group_id':re.findall(r'-*g(\d+)-', attraction_url)[0],
                'url': attraction_url,
            }
