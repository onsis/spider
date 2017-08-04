#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# crawler.py
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
from natalia.core.engine import CrawlerEngine

__version__ ='0.0.1'
__author__ = 'sxt'

class CrawlerProcess(object):
    def __init__(self,settings=None,log_level='DEGUB'):
        """

        :param settings: 配置文件
        :param log_level: 默认日志级别是'logging.DEBUG'
        """
        self.logger = logging.getLogger(__name__)
        self.engine = CrawlerEngine(**(settings or {}))
        self.log_level = log_level
        self.config_logger()

    def crawl(self, spider_cls, *args, **kwargs):
        self.engine.submit(spider_cls, *args, **kwargs)

    def start(self):
        self.engine.start()

    def config_logger(self):
        logging.basicConfig(format='[%(asctime)s][%(module)s.%(lineno)d][%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=getattr(logging, self.log_level, logging.DEBUG))
