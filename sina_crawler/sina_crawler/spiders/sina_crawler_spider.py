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
        f = open("/root/originaltech/crawler/sina_crawler/sina_crawler/spiders/crawled_urls", "r")
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
        lower_url = response.url.lower()
        selector = Selector(response)
        #html = response.body
        #f = open("test.html","w",encoding="utf-8")
        #f.write(str(html))
        #f.close
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
                self.crawled_urls.add(response.url)
                if item['time'] == None:
                    item['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if item['source'] == None:
                    item['source'] = ''
                if item['keywords'] == None:
                    item['keywords'] = ''
                if item['topic'] == None:
                    item['topic'] = ''
                yield item
            '''
            f = open("./crawled_urls", "a+")
            f.write(str(response.url) + "\n")
            f.close()
            self.crawled_urls.add(response.url)
            insert_sql = "insert into sina_news (title, url"
            if len(item['time']) != 0:
                insert_sql += ", time"
            if len(item['content']) != 0:
                insert_sql += ", content"
            if len(item['source']) != 0:
                insert_sql += ", source"
            if len(item['keywords']) != 0:
                insert_sql += ", keywords"
            if len(item['topic']) != 0:
                insert_sql += ", topic"
            insert_sql += ") values ('"
            insert_sql += item['title'][0] + "', '" + item['url'] + "'"
            if len(item['time']) != 0:
                insert_sql += ", '" + item['time'][0].replace("年", "-").replace("月", "-").replace("日", "") + "'"
            if len(item['content']) != 0:
                insert_sql += ", '" + item['content'] + "'"
            if len(item['source']) != 0:
                insert_sql += ", '" + item['source'][0] + "'"
            if len(item['keywords']) != 0:
                insert_sql += ", '" + ",".join(item['keywords']) + "'"
            if len(item['topic']) != 0:
                insert_sql += ", '" + item['topic'][0] + "'"
            insert_sql += ")"
            self.cursor.execute(insert_sql)
            self.conn.commit()
            yield item
            '''
        for sel in selector.xpath('//a'):
            #title = sel.xpath("text()").extract_first()
            link = sel.xpath("@href").extract_first()
            if link != None and not link.endswith("pdf"):
                url = link
                if not link.startswith("http"):
                    url = os.path.split(response.url)[0] + '/' + link
                url = self.processUrl(url)
                if url != None and url.find("finance.sina.com") != -1:
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

