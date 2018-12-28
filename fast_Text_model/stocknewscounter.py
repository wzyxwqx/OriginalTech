#!encoding:utf-8
import pymysql
from NewsPredict import predict
from datetime import datetime
from datetime import timedelta
from mysqlconnector import MysqlConnector

'''stock_news_count.py

Prepare data for logistic model training.
Update senti_stat from crawled_news database.
If the data is missing for several days, revise
the days in range.

'''
class StockNewsCounter:
    def __init__(self):
        # Database from server: crawled news.
        self.conn = MysqlConnector()
        self.news = []
        self.stock_good = dict()
        self.stock_bad = dict()
        self.stock_total = dict()

    def fetch(self, days):
        if not isinstance(days, int):
            raise ValueError('wrong days!')
        if days < 1:
            raise ValueError('wrong days!')
        # Collect recent news.
        print("select recent news from database ...")
        # The time in server is GMT, it should add 8 hours
        # to get CST.
        now = datetime.now() + timedelta(hours=8)
        # Last 24*days hours.
        for i in range(1,1+days):
            pre_time = now + timedelta(days=-i)
            cur_time = pre_time + timedelta(days=1)
            print("select news before " + cur_time.strftime("%Y-%m-%d") + " 09:10:00")
            check_sql = "select title, time, keystock from news where time > '" + pre_time.strftime(
                "%Y-%m-%d") + " 09:10:00' and time < '" + cur_time.strftime(
                "%Y-%m-%d") + " 09:10:00' and keystock != ''"
            self.news = self.conn.fetchdata(check_sql)

    def count(self):
        # Good & bad & total news count.
        for line in self.news:
            # Use fast_text model to predict good or bad.
            senti = predict(line[0])[0][0]
            keystocks = line[2].split(" ")
            for stock in keystocks:
                if stock in self.stock_total:
                    self.stock_total[stock] += 1
                    if senti == "__label__1":
                        self.stock_good[stock] += 1
                    elif senti == "__label__2":
                        self.stock_bad[stock] += 1
                else:
                    self.stock_total[stock] = 1
                    if senti == "__label__1":
                        self.stock_good[stock] = 1
                        self.stock_bad[stock] = 0
                    elif senti == "__label__2":
                        self.stock_bad[stock] = 1
                        self.stock_good[stock] = 0
                    else:
                        self.stock_good[stock] = 0
                        self.stock_bad[stock] = 0

    def insert(self):
        # Insert information into the senti_stat from database of crawled_news.
        if len(stock_total) == 0:
            raise Exception("No data to commit!")
        for key, value in self.stock_total.items():
            good = self.stock_good[key]
            bad = self.stock_bad[key]
            insert_sql = "insert into senti_stat (time, stockcode, total, good, bad) values ('%s', '%s', '%d', '%d', '%d')"
            self.conn.insertdata(insert_sql % ((cur_time.strftime("%Y-%m-%d") + " 09:10:00"), key, value, good, bad))


if __name__ == "__main__":
    snc = StockNewsCounter()
    snc.fetch(1)
    snc.count()
    snc.insert()
    print("finish!")


