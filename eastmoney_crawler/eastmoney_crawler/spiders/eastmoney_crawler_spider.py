#!encoding:utf-8
import scrapy
import os
import pymysql
from datetime import datetime
from eastmoney_crawler.items import EastmoneyCrawlerItem
from scrapy.selector import Selector

class EastmoneyCrawlerSpider(scrapy.Spider):
    name = "eastmoney_crawler"
    allowed_domains = ["eastmoney.com"]
    start_urls = ["http://www.eastmoney.com/"]
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
        f = open("/root/originaltech/crawler/eastmoney_crawler/eastmoney_crawler/spiders/crawled_urls", "r")
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
        item = EastmoneyCrawlerItem()
        item['title'] = selector.xpath('//div[@class="newsContent"]/h1/text()').extract_first()
        item['time'] = selector.xpath('//div[@class="time-source"]/div[@class="time"]/text()').extract_first()
        item['source'] = selector.xpath('//div[@class="source data-source"]/text()').extract()
        item['url'] = response.url
        content_list = selector.xpath('//div[@id="ContentBody"]/p/text()').extract()
        item['content'] = " ".join(content_list).replace('\u3000', '').replace('\r\n', ' ')
        item['abstract'] = selector.xpath('//div[@class="b-review"]/text()').extract_first()
        if item['title'] != None:
            #f = open("./crawled_urls", "a+")
            #f.write(str(response.url) + "\n")
            #f.close()
            if item['time'] != None:
                item['time'] = item['time'].replace('年', '-').replace('月', '-').replace('日', '')
            if len(item['source']) > 1:
                item['source'] = item['source'][1].strip('\r\n').strip(' ')
            elif len(item['source']) == 1:
                item['source'] = item['source'][0].strip('\r\n').strip(' ')
            self.crawled_urls.add(response.url)
            #insert_sql = "insert into cnstock_news (title, url, time, content, source) values ('" + item['title'][0] + "', '" + str(response.url) + "', '" + item['time'][0] + "', '" + item['content'] + "', '" + item['source'][0].strip("来源：") + "')"
            #self.cursor.execute(insert_sql)
            #self.conn.commit()
            yield item
        for sel in selector.xpath('//a'):
            #title = sel.xpath("text()").extract_first()
            link = sel.xpath("@href").extract_first()
            if link != None and not link.endswith("pdf") and not link.endswith("exe") and not link.endswith("zip"):
                url = link
                if not link.lower().startswith("http"):
                    url = os.path.split(response.url)[0] + '/' + link
                url = self.processUrl(url)
                if url != None and url.find("eastmoney.com") != -1:
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

