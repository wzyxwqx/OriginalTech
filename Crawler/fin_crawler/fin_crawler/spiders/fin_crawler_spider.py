#!encoding:utf-8
import scrapy
import os
from datetime import datetime
from fin_crawler.items import FinCrawlerItem
from scrapy.selector import Selector

class FinCrawlerSpider(scrapy.Spider):
    name = "fin_crawler"
    allowed_domains = ["financialnews.com.cn"]
    custom_settings = {
        'DEPTH_PRIORITY' : 1,
        'DEPTH_LIMIT' : 4,
        'CLOSESPIDER_TIMEOUT' : 420,
    }
    start_urls = ["http://www.financialnews.com.cn/"]
    crawled_urls = set()
    visited_urls = set()
    cookies = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    meta = {'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]}

    def __init__(self):
        f = open("/root/originaltech/crawler/fin_crawler/fin_crawler/spiders/crawled_urls", "r")
        line = f.readline()
        while line != "":
            line = line.strip("\n")
            self.crawled_urls.add(line)
            line = f.readline()
        f.close()
        print("crawled " + str(len(self.crawled_urls)) + " websites")

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback = self.parse, headers = self.headers, cookies = self.cookies, meta = self.meta)

    def parse(self, response):
        if response.url in self.visited_urls:
            return
        print("parsing " + str(response.url))
        self.visited_urls.add(response.url)
        lower_url = response.url.lower()
        selector = Selector(response)
        if lower_url.endswith("htm") or lower_url.endswith("html"):
            item = FinCrawlerItem()
            item['title'] = selector.xpath('//div[@class="content_title"]/text()').extract_first()
            item['url'] = response.url
            if item['title'] != None:
                content_list = selector.xpath('//div[@class="content_body"]/div[@class="TRS_Editor"]/div[@class="Custom_UnionStyle"]/p/text()').extract()
                item['content'] = " ".join(content_list).replace('\u3000', '').replace('\xa0', '')
                item['source'] = selector.xpath('//div[@class="content_info"]/span[1]/text()').extract_first()
                if item['source'] != None:
                    item['source'] = item['source'].strip('来源：')
                item['time'] = selector.xpath('//div[@class="content_info"]/span[3]/text()').extract_first()
                if item['time'] != None:
                    item['time'] = item['time'].strip('发布日期：')
                self.crawled_urls.add(response.url)
                yield item
        for sel in selector.xpath('//a'):
            link = sel.xpath("@href").extract_first()
            if link != None and not link.endswith("pdf"):
                url = link
                if not url.lower().startswith("http"):
                    url = os.path.split(response.url)[0] + '/' + link
                url = self.processUrl(url)
                if url != None and url.lower().find("financialnews.com.cn") != -1:
                    yield scrapy.Request(url, callback = self.parse, headers = self.headers, cookies = self.cookies, meta = self.meta)

    def processUrl(self, url):
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

