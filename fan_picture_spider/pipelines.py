# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from qiniu import Auth
from qiniu import BucketManager
from scrapy import signals
from scrapy.exporters import CsvItemExporter

import uuid
import json
import requests
import time

class FanPictureSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class UploadPicturePipeline(object):

    def __init__(self, access_key, secret_key, bucket_domain, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_domain = bucket_domain
        self.bucket_name = bucket_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            access_key = crawler.settings.get('QINIU_ACCESS_KEY'),
            secret_key = crawler.settings.get('QINIU_SECRET_KEY'),
            bucket_domain = crawler.settings.get('BUCKET_DOMAIN'),
            bucket_name = crawler.settings.get('BUCKET_NAME'),
        )

    def open_spider(self, spider):
        q = Auth(self.access_key, self.secret_key)
        self.bucket = BucketManager(q)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        url = item.get('pic_url')[0]
        group_id = item.get('group_id')[0]
        id_ = item.get('id')[0]
        
        # 增加时间戳
        item['time'] = int(time.time())

        key = 'zuobiao/g' + group_id + '/a' + id_ \
                + '/' + str(uuid.uuid4()) + '.jpg'

        try:
            ret, info = self.bucket.fetch(url, self.bucket_name, key)
        except Exception as e:
            spider.logger.info('[图片上传失败]，链接：{}，异常：{}'.format(
                                url, repr(e)))
        else:
            if key == ret['key']:
                item['updated_pic_url'] = ret['key']
        try:
            image_info = requests.get(self.bucket_domain + key, 'imageInfo').json()
        except Exception as e:
            spider.logger.info('[图片尺寸获取失败]，链接：{}，异常：{}'
                            .format(key, repr(e)))
        else:
            item['pic_width'] = image_info.get('width')
            item['pic_height'] = image_info.get('height')
            item['pic_size'] = image_info.get('size')

        return item

class CsvItemExporterPipline(object):

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('%s_items.csv' % spider.name, 'a+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
