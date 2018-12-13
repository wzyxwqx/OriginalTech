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
        self.crawledurlfile = codecs.open("/root/originaltech/crawler/sina_crawler/sina_crawler/spiders/crawled_urls", "a+", "utf-8")
        self.conn = pymysql.connect(host = "localhost", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        res = dict(item)
        self.crawledurlfile.write(res["url"] + "\n")
        time = res['time'].replace('年', '-').replace('月', '-').replace('日', '')
        insert_sql = "insert into news (title, url, content, time, source, keywords, topic, website) value('" + item['title'] + "', '" + item['url'] + "', '" + item['content'] + "', '" + time + "', '" + item['source'] + "', '" + item['keywords'] + "', '" + item['topic'] + "', '新浪财经')"
        self.cursor.execute(insert_sql)
        self.conn.commit()
        return item
