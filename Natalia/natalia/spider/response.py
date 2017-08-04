#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# response.py
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

import urlparse
from natalia.utils.url import base_url

__version__ = '0.0.1'
__author__ = 'sxt'

class Response(object):
    def __init__(self,url,status_code,content,request,cookies=None,headers=None):
        self.url = url
        self.status_code = status_code
        self.content = content or ''
        self.request = request
        self.cookies = cookies or {}
        self.headers = headers or {}
        self.base_url = base_url(url)
        self.meta = getattr(request,'meta',None)

    def splicing_url(self,url):
        return urlparse.urljoin(self.base_url,url)

    @property
    #装饰content_to_unicode方法为属性函数
    def content_to_unicode(self):
        return self.content.decode('utf-8')

    def __repr__(self):
        #内建函数，返回一个可以用来表示对象的可打印字符串
        return '<Response status={} url="{}" content="{}">'.format(self.status_code,self.url,self.content[:60])


if __name__=='__main__':
    pass
