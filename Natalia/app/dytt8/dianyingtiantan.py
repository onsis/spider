from natalia.core.crawler import  CrawlerProcess

from natalia.spider.spider import  BaseSpider
from natalia.spider.request import  Request

import json
from lxml.html import  fromstring

class DyttDownload(BaseSpider):
    name = 'dytt_spider'
    urls = ['http://www.ygdy8.net/']
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'
    }

    def start_spider(self):
        self.file = open('dytt.txt', 'w')

    def stop_spider(self):
        self.file.close()

    def spider_idle(self):
        pass

    def make_request_from_url(self, url):
        return Request(url, headers=self.default_headers)

    def parse(self, response):
        root = fromstring(response.content, base_url=response.base_url)
        for element in root.xpath('//ul/a'):
            #text = self.extract_first(element,'//p/text()')
            #print text
            link = self.extract_first(element,'@href')
            print link

    def process_item(self, item):
        print item
        print json.dumps(item, ensure_ascii=False)

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
        'concurrent_requests': 100,
        'queue_size': 1024
    }
    crawler = CrawlerProcess(settings, 'DEBUG')
    crawler.crawl(DyttDownload)
    crawler.start()
    #resp = requests.get(request.url, **kw_params)


if __name__ == '__main__':
    main()