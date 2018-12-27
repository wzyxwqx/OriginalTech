# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import pymysql

class CsCrawlerPipeline(object):
    def __init__(self):
        self.crawledurlfile = codecs.open("/root/originaltech/crawler/cs_crawler/cs_crawler/spiders/crawled_urls", "a+")
        self.conn = pymysql.connect(host = "localhost", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        res = dict(item)
        self.crawledurlfile.write(res['url'] + "\n")
        insert_sql = "insert into news (title, url, content, source, time, website) values ('" + res['title'] + "', '" + res['url'] + "', '" + res['content'] + "', '" + res['source'].strip("来源：") + "', '" + res['time'] + "', '中证网')"
        self.cursor.execute(insert_sql)
        self.conn.commit()
        return item
