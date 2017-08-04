#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# engine.py
# Copyright (C) 2017 onsis <sxtttian@163.com>
#
# Natalia is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-foobar is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import threading
import eventlet
eventlet.monkey_patch()
import time
import Queue
import random

import pybloom
import requests
from requests.exceptions import  ConnectTimeout,ConnectionError,ReadTimeout

import pybloomfilter

from natalia.spider.request import  Request
from natalia.spider.response import Response
from natalia.utils.url import url_fingerprint



__version__ = '0.0.1'
__author__ = 'sxt'

#通过设置logging.CRITICAL来起到关闭requests 库的日志打印作用
logging.getLogger('requests').setLevel(logging.CRITICAL)

class CrawlerEngine(object):
    def __init__(self,concurrent_requests=100,download_delay=0,download_timeout=5,
                 retry_on_timeout=False,queue_size=1024):
        """
        爬虫的核心引擎，负责调度并完成URL请求和调用解析方法
        :param concurrent_requests: 并发请求数
        :param download_delay: 每批次之间的下载延迟（单位为秒），默认为0
        :param download_time: 下载等待延迟，默认为6秒
        :param retry_on_time: 即当下载超时后，对应的请求是否应该重试
        :param queue_size: 请求队列和响应队列大小，当队列已满时，会阻塞后续操作
        """
        self.logger = logging.getLogger(__name__)
        self.status = False
        self.concurrent_requests = concurrent_requests
        self.download_delay = download_delay
        self.engine_idle_timeout = 1.5 * download_timeout
        self.download_timeout = download_timeout
        self.retry_on_download_timeout = retry_on_timeout
        self.requests_queue = Queue.Queue(queue_size)
        self.responses_queue = Queue.Queue(queue_size)
        self.spiders = {}

        #调用pybloom库进行URL去重操作
        self.distinct = pybloom.ScalableBloomFilter()

    def start(self):
        #启动引擎
        self.start_engine()
        self.status = True
        #初始化种子请求
        self.init_seed_requests()

        #启动一个后台线程池，负责下载由调度器提供给它的所有 URL（Request），并将响应（Response）结果存放到队列中
        #threading.Thread(target=self.scheduler_download).setDaemon(True).start()
        t = threading.Thread(target=self.scheduler_download)
        t.setDaemon(True)
        t.start()

        #前台解析线程会不断消费处理队列中的响应（Response），并调用相应 Spider 的解析函数处理这些相应；
        self.process_responses_from_queue()

    def close(self):
        #关闭引擎
        self.status = False
        self.close_engine()

    def submit(self, spider_cls, *args, **kwargs):
        """
        提交一个新的Spider到工作队列中
        :param spider_cls: 一个Spider类
        :param args:
        :param kwargs:
        :return: None
        """

        spider = spider_cls(*args, crawler=self, **kwargs)
        # 确保爬虫名字是唯一的

        self.logger.info(spider.name)
        if spider.name in self.spiders:
            raise Exception('爬虫 {} 退出, 如果你需要继续运行该爬虫，请更改爬虫名字.'.format(spider.name))
        self.spiders[spider.name] = spider

    def crawl(self, request, spider):
        """
        爬取下一个请求
        :param request: 一个"Request"对象
        :param spider: 爬虫句柄
        :return:
        """
        #self.logger.debug(request)
        #self.logger.debug(spider)
        self.enqueue_request(request, spider)

    def engine_idle(self):
        """
        当队列中没有request时，将会调用这个方法，给引擎添加新的请求
        :return:None
        """
        self.logger.debug('爬虫引擎处于idle 模式')
        self.call_func_in_spiders('spider_idle')


    def start_engine(self):
        self.logger.info('启动爬虫引擎')
        #回调方法，调用所有爬虫的start_spider方法
        self.call_func_in_spiders('start_spider')

    def close_engine(self):
        """
        关闭爬虫引擎
        :return: None
        """
        self.logger.info('关闭爬虫引擎')
        self.call_func_in_spiders('stop_spider')

    def init_seed_requests(self):
        for spider in self.spiders.values():
            try:
                [self.crawl(request, spider) for request in self.call_func_in_spider(spider, 'get_requests')]
            except Exception as err:
                self.logger.error(err, exc_info=True)

    def process_request(self, request, spider):
        """
        为这个spider处理一个新的请求
        :param request: 一个"Request"对象
        :param spider: 爬虫句柄
        :return: None
        """
        self.logger.debug('[{}][{}] 正在处理请求: {}'.format(spider.name, self.requests_queue.qsize(), request))
        self.call_func_in_spider(spider, 'process_request', request)

    def enqueue_request(self,request, spider):
        if request:
            if not request.dont_filter and self.request_distinct(request):
                self.logger.debug('[{}] 忽略重复的请求 {}'.format(spider.name,
                                                                     request))
                return
        self.requests_queue.put((request, spider))


    def process_response(self,response,spider):
        """
        为这个spider处理一个新的响应
        :param request: 一个"Request"对象
        :param spider: 爬虫句柄
        :return: None
        """
        self.logger.debug(
            '[{}][{}] 正在处理响应: {}'.format(spider.name, self.responses_queue.qsize(), response))
        self.call_func_in_spider(spider, 'process_response', response)

        try:
            #获取指定的回调方法，没有指定使用默认方法
            parse = getattr(response.request, 'callback', None) or getattr(spider, 'parse')
            result = parse(response)
            if result is None:
                return
            for r in parse(response):
                if r is None:
                    continue
                if isinstance(r,dict):
                    self.process_item(r,spider)
                elif isinstance(r,Request):
                    # 一个新的请求将会放到队列
                    self.crawl(r,spider)
                else:
                    self.logger.error('Expected types are `dict`, `Request` and `None`')
        except Exception as err:
            self.logger.error(self,exc_info=True)


    def process_item(self,item,spider):
        """

        :param item:
        :param spider:
        :return:
        """
        self.logger.debug('[{}] Scraped item: '.format(spider.name))
        self.call_func_in_spider(spider, 'process_item', item)




    def process_responses_from_queue(self):
        while self.status:
            try:
                response, spider = self.responses_queue.get(timeout=self.engine_idle_timeout)
                self.process_response(response, spider)
            except Exception as err:
                self.close()
            time.sleep(0.05)

    def download(self,request,spider):
        def retry():
            if self.retry_on_download_timeout:
                self.logger.debug('下载超时，从新下载{}'.format(request))
                self.crawl(request,spider)


        try:
            self.process_request(request,spider)
            self.logger.debug(request.url)
            if request is None:
                return

            method = request.method.upper()

            resp = None
            kw_params ={
                'timeout': self.download_timeout,
                'cookies': request.cookies,
                'headers': request.headers,
                'proxies': {
                    'http': request.proxy,
                    'https': request.proxy
                }
            }
            self.logger.debug('[{}]<{} {}>'.format(spider.name, method, request.url))

            if method == 'GET':
                resp = requests.get(request.url, **kw_params)
            elif method == 'POST':
                resp = requests.post(request.url, request.data, **kw_params)

            self.responses_queue.put((Response(resp.url, resp.status_code, resp.content, request,
                                            resp.cookies), spider))
        except (ConnectionError,ConnectTimeout,ReadTimeout):#有待改进
            retry()
        except Exception as err:
            self.logger.error(err, exc_info=True)
        return 'end download'


    def scheduler_download(self):
        pool = eventlet.GreenPool(self.concurrent_requests)
        while self.status:
            #futures = [pool.imap(self.download,req,spider) for req,spider in self.next_requests_batch()]
            futures = [pool.spawn(self.download, req,spider) for req ,spider in self.next_requests_batch()]

            time.sleep(self.download_delay*random.randint(1,5))

        self.logger.debug('停止下载')







    def next_requests_batch(self):
        for i in range(self.concurrent_requests):
            try:
                yield self.requests_queue.get(timeout=1)
            except Exception as err:
                self.engine_idle()


    def call_func_in_spider(self,spider, name, *args, **kwargs):
        try:
            if hasattr(spider, name):
                return getattr(spider, name)(*args, **kwargs)
        except Exception as err:
            self.logger.error(err, exc_info=True)

    def call_func_in_spiders(self,name,*args,**kwargs):
        for s in self.spiders.values():
            self.call_func_in_spider(s, name, *args, **kwargs)

    def request_distinct(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.distinct:
            return True
        self.distinct.add(fp)


    @staticmethod
    def request_fingerprint(request):
        return url_fingerprint(request.url)



def main():
    pass

if __name__=='__main__':
    main()