# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
#import MySQLdb
import pymysql

class SinaCrawlerPipeline(object):
    def __init__(self):
        self.crawled_urls_file = codecs.open("/root/originaltech/crawler/sina_crawler/sina_crawler/spiders/crawled_urls", "a+", "utf-8")
        self.conn = pymysql.connect(host = "localhost", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        '''
        res = dict(item)
        self.crawled_urls_file.write(res["url"] + "\n")
        url = res['url']
        title = res['title'][0]
        content = res['content'][0]
        time = res['time'][0].replace('年', '-').replace('月', '-').replace('日', '')
        source = res['source'][0]
        keywords = ",".join(res['keywords'])
        topic = res['topic'][0]
        '''
        return item
