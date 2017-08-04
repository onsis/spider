from natalia.core.crawler import  CrawlerProcess

from natalia.spider.spider import  BaseSpider
from natalia.spider.request import  Request

import json
from lxml.html import  fromstring

class BaiduNewsSpider(BaseSpider):
    name = 'baidu_news_spider'
    urls = ['http://news.baidu.com/']
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'
    }

    def start_spider(self):
        self.file = open('baidu_news.txt','w')

    def stop_spider(self):
        self.file.close()

    def spider_idle(self):
        pass

    def make_request_from_url(self,url):
        return Request(url, headers=self.default_headers)

    def parse(self,response):
        root = fromstring(response.content, base_url=response.base_url)
        for element in root.xpath('//a[@target="_blank"]'):
            title = self.extract_first(element, 'text()')
            link = self.extract_first(element, '@href').strip()
            if title:
                if link.startswith('http://') or link.startswith('https://'):
                    yield {'title': title, 'link': link}
                    yield Request(link, headers=self.default_headers, callback=self.parse_news,meta={'title': title})

    def parse_news(self, response):
        pass

    def process_item(self,item):
        print item
        print json.dumps(item,ensure_ascii=False)

    @staticmethod
    def extract_first(element, exp, default=''):
        r = element.xpath(exp)
        if len(r):
            return r[0]

        return default


def main():
    settings = {
        'download_delay': 1,
        'download_timeout': 6,
        'retry_on_timeout': True,
        'concurrent_requests': 48,
        'queue_size': 1024
    }
    crawler = CrawlerProcess(settings,'DEBUG')
    crawler.crawl(BaiduNewsSpider)
    crawler.start()

if __name__=='__main__':
    main()