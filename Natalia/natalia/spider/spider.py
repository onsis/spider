#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# spider.py
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
from natalia.spider.request import Request



__version__ = '0.0.1'
__author__ = 'sxt'

class BaseSpider(object):
    name = ''
    urls = []

    def __init__(self,*args,**kwargs):
        self.crawler = kwargs.get('crawler',None)
        self.logger = logging.getLogger(__name__)

    def start_spider(self):
        pass

    def spider_idle(self):
        pass

    def stop_spider(self):
        pass

    def get_requests(self):
        print self.urls
        for url in self.urls:
            yield self.make_request_from_url(url)

    def make_request_from_url(self,url):
        return Request(url,headers=getattr(self,'default_headers',None),
                       callback=self.parse)

    def parse(self,response):
        raise NotImplementedError

    def process_request(self,request):
        pass

    def process_response(self,response):
        pass

    def process_item(self,item):
        raise  NotImplementedError

    def __repr__(self):
        return '<{} name="{}">'.format(self.__class__.__name__,self.name)





if __name__=='__main__':
    pass
