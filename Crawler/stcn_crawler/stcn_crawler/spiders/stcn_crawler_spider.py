#!encoding:utf-8
import scrapy
import os
import pymysql
from datetime import datetime
from stcn_crawler.items import StcnCrawlerItem
from scrapy.selector import Selector

class StcnCrawlerSpider(scrapy.Spider):
    name = "stcn_crawler"
    allowed_domains = ["stcn.com"]
    start_urls = ["http://www.stcn.com/"]
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
        f = open("/root/originaltech/crawler/stcn_crawler/stcn_crawler/spiders/crawled_urls", "r")
        line = f.readline()
        while line != "":
            line = line.strip("\n")
            self.crawled_urls.add(line)
            #self.visited_urls.add(line)
            line = f.readline()
        f.close()
        print("crawled " + str(len(self.crawled_urls)) + " websites")
        #self.conn = pymysql.connect(host = "localhost", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
        #self.cursor = self.conn.cursor()

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback = self.parse, headers = self.headers, cookies = self.cookies, meta = self.meta)

    def parse(self, response):
        if response.url in self.visited_urls:
            return
        print("parsing " + str(response.url))
        self.visited_urls.add(response.url)
        selector = Selector(response)
        item = StcnCrawlerItem()
        item['title'] = selector.xpath('//div[@class="intal_tit"]/h2/text()').extract_first()
        item['time'] = selector.xpath('//div[@class="info"]/text()').extract_first()
        item['url'] = response.url
        item['source'] = selector.xpath('//div[@class="info"]/span/text()').extract_first()
        content_list = selector.xpath('//div[@class="txt_con"]/p/text()').extract()
        item['content'] = " ".join(content_list).replace('\u3000', '')
        if item['title'] != None:
            #f = open("./crawled_urls", "a+")
            #f.write(str(response.url) + "\n")
            #f.close()
            self.crawled_urls.add(response.url)
            #insert_sql = "insert into stcn_news (title, url, time, content, source) values ('" + item['title'][0] + "', '" + item['url'] + "', '" + item['time'] + "', '" + item['content'] + "', '" + item['source'][0].strip("来源：") + "')"
            #self.cursor.execute(insert_sql)
            #self.conn.commit()
            yield item
        for sel in selector.xpath('//a'):
            #title = sel.xpath("text()").extract_first()
            link = sel.xpath("@href").extract_first()
            if link != None and not link.endswith("pdf"):
                url = link
                if not link.startswith("http"):
                    url = os.path.split(response.url)[0] + '/' + link
                url = self.processUrl(url)
                if url != None and url.find("stcn.com") != -1:
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


