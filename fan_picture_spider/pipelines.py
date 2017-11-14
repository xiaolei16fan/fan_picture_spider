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

class FanPictureSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class UploadPicturePipeline(object):

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            access_key = crawler.settings.get('QINIU_ACCESS_KEY'),
            secret_key = crawler.settings.get('QINIU_SECRET_KEY')
        )

    def open_spider(self, spider):
        q = Auth(self.access_key, self.secret_key)
        self.bucket = BucketManager(q)
        self.bucket_name = 'static'

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        url = item.get('picture_url')[0]
        group_id = item.get('group_id')[0]
        id_ = item.get('id')[0]

        key = 'zuobiao/g' + group_id + '/a' + id_ \
                + '/' + str(uuid.uuid4()) + '.jpg'

        try:
            ret, info = self.bucket.fetch(url, self.bucket_name, key)
        except ConnectionError as e:
            spider.logger.info('[图片上传失败] 失败链接：{}'.format(url))
        else:
            item['updated_pic_url'] = ret['key']

        return item

class CsvItemExporterPipline(object):

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('%s_items.csv' % spider.name, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
