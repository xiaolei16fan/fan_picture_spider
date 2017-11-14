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
service_args = []
service_args.append('--load-images=no')
service_args.append('--disk-cache=yes')
service_args.append('--ignore-ssl-errors=true')
driver = webdriver.PhantomJS(service_args=service_args)
driver.implicitly_wait(10) # 超时时间为10s
driver.set_page_load_timeout(10)


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

        try:
            click_element = '//div[@class="entry_cta_wrap"]'
            driver.find_element_by_xpath(click_element).click()
            sleep(3)
        except:
            spider.logger.debug('cannot open the click element refere page.')

        body = driver.page_source
       
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8',
                            request=request)
