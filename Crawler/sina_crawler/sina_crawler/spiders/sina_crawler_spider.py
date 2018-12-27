#!encoding:utf-8
import scrapy
import re
import os
import json
import pymysql
from datetime import datetime
from sina_crawler.items import SinaCrawlerItem
from scrapy.selector import Selector



class SinaCrawlerSpider(scrapy.Spider):
    '''Spider: crawling financial news starting from sina
    

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
    name = "sina_crawler"
    allowed_domains = ["finance.sina.com.cn"]
    start_urls = ["https://finance.sina.com.cn/"]
    crawled_urls = set()
    visited_urls = set()
    custom_settings = {
        'DEPTH_PRIORITY' : 1,
        'DEPTH_LIMIT' : 4,
        'CLOSESPIDER_TIMEOUT' : 420,
    }
    cookies = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    meta = {'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]}
    
    def __init__(self):
        '''Initiate to get crawled_urls for later use.'''
        f = open("/root/originaltech/crawler/sina_crawler/sina_crawler/spiders/crawled_urls", "r")
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
        '''The function processing callback informatino in scrapy.Request'''
        if response.url in self.visited_urls:
            return
        print("parsing " + str(response.url))
        self.visited_urls.add(response.url)
        lower_url = response.url.lower()
        selector = Selector(response)
        if lower_url.endswith("htm") or lower_url.endswith("html"):
            item = SinaCrawlerItem()
            item['title'] = selector.xpath('//h1[@class="main-title"]/text()').extract_first()
            item['time'] = selector.xpath('//span[@class="date"]/text()').extract_first()
            content_list = selector.xpath('//*[@id="artibody"]/p/text()').extract()
            item['content'] = " ".join(content_list).replace('\u3000', '')
            item['source'] = selector.xpath('//div[@class="date-source"]/a/text()').extract_first()
            item['url'] = response.url
            keyword_list = selector.xpath('//div[@class="keywords"]/a/text()').extract()
            item['keywords'] = ",".join(keyword_list)
            item['topic'] = selector.xpath('//div[@data-sudaclick="content_relativetopics_p"]/a/text()').extract_first()
            if item['title'] != None:
                # Got right url:
                self.crawled_urls.add(response.url)
                # Process errors.
                if item['time'] == None:
                    item['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if item['source'] == None:
                    item['source'] = ''
                if item['keywords'] == None:
                    item['keywords'] = ''
                if item['topic'] == None:
                    item['topic'] = ''
                yield item

        for sel in selector.xpath('//a'):
            # Crawl further in the links available.
            link = sel.xpath("@href").extract_first()
            if link != None and not link.endswith("pdf"):
                url = link
                if not link.startswith("http"):
                    url = os.path.split(response.url)[0] + '/' + link
                url = self.processUrl(url)
                if url != None and url.find("finance.sina.com") != -1:
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

