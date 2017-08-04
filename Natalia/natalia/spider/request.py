#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# request.py
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

from natalia.utils.url import safe_url

__version__ = '0.0.1'
__author__ = 'sxt'

class Request(object):
    def __init__(self,url,method='GET',data=None,cookies=None,headers=None,meta=None,proxy=None,
                 callback=None,dont_filter=False):
        self.url = safe_url(url)
        self.method = method
        self.data = data
        self.cookies = cookies
        self.headers = headers
        self.meta = meta
        self.proxy = proxy
        self.callback = callback
        self.dont_filter = dont_filter

    def __repr__(self):
        return '<Request url="{url}">'.format(**self.__dict__)

if __name__ =='__main__':
    pass