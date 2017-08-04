#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# url.py
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

from hashlib import sha1
#from urlparse import urlparse
#from urlparse import urlunsplit
#from urllib import urlencode

import urlparse
import urllib

__version__ = '0.0.1'
__author__ = 'sxt'


def url_fingerprint(url):
    h = sha1()
    h.update(url.encode('utf-8'))
    return h.hexdigest()

def safe_url(url,remove_empty_query=True):
    """
    此方法的作用是返回一个合法的URL
    :param url:传入的网址，如：https://github.com/onsis/
    :param remove_empty_query:设为True时，当URL的查询字段query为空时，就把这个字段移除
    :return:返回一个合法的URL
    """
    try:
        """
         urlparse模块主要是把url拆分为6部分,返回一个元祖 (scheme, netloc, path, parameters, query, fragment)，（协议、位置、路径、可选参数、查询、片段）
         urlunsplit模块主要是把(scheme, netloc, path, query, fragment)组合成一个完整的url,注意不能有parameters这个参数
        """
        parseresult = urlparse.urlparse(url)
        print parseresult

        if not url.query:
            return url.rstrip('/')#把末尾的'/'删除
        #for i in parseresult.query:
            #print i


    except:
        return url.rstrip('/')

def base_url(url):
    """
    从一个完整的url地址中获取基地址
    :param url: 从一个完整的url地址，https://github.com/onsis/
    :return: 返回基地址，https://github.com
    """
    parseresult = urlparse.urlparse(url)
    print parseresult
    return '://'.join((parseresult.scheme , parseresult.netloc))

def main():
    url = 'http://httpbin.org/get?key1=value1&key2=value2&key2=value3'
    result = safe_url(url)
    print result

if __name__ =='__main__':
    main()


