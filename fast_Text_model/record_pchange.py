#!encoding:utf-8
import pymysql
import tushare as ts
import pandas as pd
from datetime import datetime
from datetime import timedelta
from tushare_copy import get_stock_data

class record:
    def __init__(self):
        self.db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
        self.cursor = self.db.cursor()

    def load_list(self):
        print("load list ...")
        now = datetime.now() + timedelta(hours = 8)
        check_sql = "select id, time, stockcode from recomand_stock where pchange_1 is NULL"
        self.cursor.execute(check_sql)
        table = self.cursor.fetchall()
        return table

    def get_pchange(self, stockcode, time):
        time1 = time.strftime("%Y-%m-%d")
        time2 = (time + timedelta(days = 20)).strftime("%Y-%m-%d")
        data = ts.get_hist_data(stockcode, start = time1, end = time2, retry_count=5, pause=0.1)
        if data is None or data.empty:
            return None
        count = 0
        res = dict()
        for row in data.iterrows():
            count += 1
            pchange = row[1][6]
            res[str(count)] = pchange
            if count == 2:
                return res
        return None

    def update(self, stock_id, time, stockcode):
        pchange = self.get_pchange(stockcode, time)
        if pchange is not None:
            update_sql = "update recomand_stock set pchange_1 = '%f', pchange_2 = '%f' where id = '%d'"
            self.cursor.execute(update_sql % (pchange['1'], pchange['2'], stock_id))
            self.db.commit()

    def pchange_record(self):
        update_list = self.load_list()
        for row in update_list:
            print("update pchange for " + row[2] + " ...")
            self.update(row[0], row[1], row[2])

if __name__ == "__main__":
    record().pchange_record()
    print("finish!")
