# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FanPictureSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    picture_url = scrapy.Field()
    attraction_id = scrapy.Field()
    group_id = scrapy.Field()
    attraction_url = scrapy.Field()

class AttractionItem(scrapy.Item):
    url = scrapy.Field()
    picture_url = scrapy.Field()
    group_id = scrapy.Field()
    id = scrapy.Field()
    updated_pic_url = scrapy.Field()

class RestrantItem(scrapy.Item):
    url = scrapy.Field()
    picture_url = scrapy.Field()
    group_id = scrapy.Field()
    id = scrapy.Field()
    updated_pic_url = scrapy.Field()

class ShoppingItem(scrapy.Item):
    url = scrapy.Field()
    picture_url = scrapy.Field()
    group_id = scrapy.Field()
    id = scrapy.Field()
    updated_pic_url = scrapy.Field()
