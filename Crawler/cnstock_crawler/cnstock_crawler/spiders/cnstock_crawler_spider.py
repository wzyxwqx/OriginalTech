#!encoding:utf-8
import scrapy
import os
import pymysql
from datetime import datetime
from cnstock_crawler.items import CnstockCrawlerItem
from scrapy.selector import Selector


class CnstockCrawlerSpider(scrapy.Spider):
    '''Spider: crawling financial news starting from CNSTOCK
        

    The SinaCrawlerSpider class starts from finance.sina.com.cn and proceeds crawling
    following a depth-first algorithm, tests the validity of returned content of news
    and stores the content into the database of server.


    Attributes:
        name: The name of crawler.
        allowed_domains: List of allowed domains for crawler.
        start_urls: List of url which the spider starts at.
        crawled_urls: Set of urls which have been crawled.
        visited_urls: Set of urls visited for the depth-first algorithm.
        custom_settings:
            DEPTH_PRIORITY: set 1 as default.
            DEPTH_LIMIT: set 4 as default.
            CLOSESPIRDER_TIMEOUT: set 420 as default, 7 mins timed out.
        cookies: Dict of cookies. Refer to scrapy for details.
        headers: Dict of user-agent string. Refer to scrapy for details.
        meta: Dict of some attributes. Refer to scrapy for details.
    '''
    name = "cnstock_crawler"
    allowed_domains = ["cnstock.com"]
    start_urls = ["http://www.cnstock.com/"]
    custom_settings = {
        'DEPTH_PRIORITY' : 1,
        'DEPTH_LIMIT' : 4,
        'CLOSESPIDER_TIMEOUT' : 420,
    }
    crawled_urls = set()
    visited_urls = set()
    cookies = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    meta = {'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]}
    def __init__(self):
        '''Initiate to get crawled_urls for later use.'''
        f = open("/root/originaltech/crawler/cnstock_crawler/cnstock_crawler/spiders/crawled_urls", "r")
        line = f.readline()
        while line != "":
            line = line.strip("\n")
            self.crawled_urls.add(line)
            line = f.readline()
        f.close()
        print("crawled " + str(len(self.crawled_urls)) + " websites")

    def start_requests(self):
        '''The main function calls Request from scrapy.'''
        yield scrapy.Request(self.start_urls[0], callback = self.parse, headers = self.headers, cookies = self.cookies, meta = self.meta)

    def parse(self, response):
        '''The function processing callback information in scrapy.Request'''
        if response.url in self.visited_urls:
            return
        print("parsing " + str(response.url))
        self.visited_urls.add(response.url)
        selector = Selector(response)
        item = CnstockCrawlerItem()
        item['title'] = selector.xpath('//div[@class="main-content text-large"]/h1[@class="title"]/text()').extract_first()
        item['time'] = selector.xpath('//span[@class="timer"]/text()').extract_first()
        item['source'] = selector.xpath('//span[@class="source"]/text()').extract_first()
        item['url'] = response.url
        content_list = selector.xpath('//div[@id="qmt_content_div"]/p/text()').extract()
        item['content'] = " ".join(content_list).replace('\u3000', '')
        if item['title'] != None:
            self.crawled_urls.add(response.url)
            yield item
        for sel in selector.xpath('//a'):
            # Crawl further in the links available
            link = sel.xpath("@href").extract_first()
            if link != None and not link.endswith("pdf"):
                url = link
                if not link.lower().startswith("http"):
                    url = os.path.split(response.url)[0] + '/' + link
                url = self.processUrl(url)
                if url != None and url.find("cnstock.com") != -1:
                    yield scrapy.Request(url, callback = self.parse, headers = self.headers, cookies = self.cookies, meta = self.meta)

    def processUrl(self, url):
        '''Process urls in the right form for scrapy.Request.'''
        items = url.split("/")
        ss = list()
        for s in items:
            if s == ".":
                continue
            elif s == "..":
                ss.pop()
            else:
                ss.append(s)
        u = "/".join(ss)
        if u.endswith("pdf") or u.endswith("zip"):
            return None
        return u

