# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from time import sleep

import re

global driver
# service_args = []
# service_args.append('--load-images=no')
# service_args.append('--disk-cache=yes')
# service_args.append('--ignore-ssl-errors=true')
# service_args=service_args
driver = webdriver.Firefox()
#driver.implicitly_wait(15) # 超时时间为10s
#driver.set_page_load_timeout(15)


class FanPictureSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class JavaScriptMiddleware(object):

    def process_request(self, request, spider):
        if not re.match(r'^.*?Reviews.*?$', request.url):
            return None

        global driver
        driver.get(request.url)
        sleep(2)

        try:
            click_element = '//div[@class="entry_cta_wrap"]'
            driver.find_element_by_xpath(click_element).click()
            sleep(1)
        except:
            spider.logger.info('cannot open the click element refere page. url: {}'
                                .format(request.url))
            body = None
        else:
            body = driver.page_source
       
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8',
                            request=request)

class SaveErrorsMiddleware(object):
    def __init__(self, crawler):
        crawler.signals.connect(self.close_spider, signals.spider_closed)
        crawler.signals.connect(self.open_spider, signals.spider_opened)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        self.output_file = open('crawler_error.log', 'a+b')

    def close_spider(self, spider):
        self.output_file.close()

    def process_spider_exception(self, response, exception, spider):
        self.output_file.write(response.url + '\n')

