#!encoding:utf-8
import scrapy
import os
from hexun_crawler.items import HexunCrawlerItem
from scrapy.selector import Selector

class HexunCrawlerSpider(scrapy.Spider):
    name = "hexun_crawler"
    allowed_domains = ["hexun.com"]
    custom_settings = {
        'DEPTH_PRIORITY' : 1,
        'DEPTH_LIMIT' : 4,
        'CLOSESPIDER_TIMEOUT' : 420,
    }
    start_urls = ["http://www.hexun.com/"]
    crawled_urls = set()
    visited_urls = set()
    cookies = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    meta = {'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]}

    def __init__(self):
        f = open("/root/originaltech/crawler/hexun_crawler/hexun_crawler/spiders/crawled_urls", "r")
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
            item = HexunCrawlerItem()
            item['title'] = selector.xpath('//div[@class="layout mg articleName"]/h1/text()').extract_first()
            item['url'] = response.url
            content_list = selector.xpath('//div[@class="art_contextBox"]/p/text()').extract()
            item['content'] = " ".join(content_list).replace('\u3000', '')
            if item['title'] != None:
                item['time'] = selector.xpath('//div[@class="clearfix"]/div[@class="tip fl"]/span[@class="pr20"]/text()').extract_first()
                item['source'] = selector.xpath('//div[@class="clearfix"]/div[@class="tip fl"]/a/text()').extract_first()
                self.crawled_urls.add(response.url)
                yield item
        for sel in selector.xpath('//a'):
            link = sel.xpath("@href").extract_first()
            if link != None and not link.endswith("pdf"):
                url = link
                if not url.lower().startswith("http"):
                    url = os.path.split(response.url)[0] + '/' + link
                url = self.processUrl(url)
                if url != None and url.lower().find("hexun.com") != -1:
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

