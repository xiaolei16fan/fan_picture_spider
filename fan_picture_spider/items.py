# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FanPictureSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AttractionItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    pic_url = scrapy.Field()
    group_id = scrapy.Field()
    updated_pic_url = scrapy.Field()
    pic_width = scrapy.Field()
    pic_height = scrapy.Field()
    pic_size = scrapy.Field()
    time = scrapy.Field()

class RestrantItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    pic_url = scrapy.Field()
    group_id = scrapy.Field()
    updated_pic_url = scrapy.Field()
    pic_width = scrapy.Field()
    pic_height = scrapy.Field()
    pic_size = scrapy.Field()
    time = scrapy.Field()

class ShoppingItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    pic_url = scrapy.Field()
    group_id = scrapy.Field()
    updated_pic_url = scrapy.Field()
    pic_width = scrapy.Field()
    pic_height = scrapy.Field()
    pic_size = scrapy.Field()
    time = scrapy.Field()
