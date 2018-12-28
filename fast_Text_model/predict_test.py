# encoding=utf-8
import pickle as pk
import pymysql
import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime
from datetime import timedelta
from tushare_copy import get_stock_data


class predict:
    def __init__(self):
        self.now = datetime.now() + timedelta(hours = 8)
        self.yesterday = self.now + timedelta(days = -1)
        self.recommand = None
        self.cursor = None
        self.recomand = dict()
        self.news_list = []
    def conn(self):
        db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
        self.cursor = db.cursor()
        check_sql = "select time, stockcode, total, good, bad from senti_stat where time > '" + self.now.strftime("%Y-%m-%d") + " 00:00:00' "
        self.cursor.execute(check_sql)
        self.news_list = self.cursor.fetchall()
                
    def get_logistic(self):
        model_path = open("logistic_model.pkl", "rb")
        self.cls = pk.load(model_path)


    def get_fin_co(self):
        f = open("listed_fin_co", "r", encoding = "utf-8")
        lines = f.readlines()
        self.fin_co = [line.strip() for line in lines]
        
    def predict_data(self):
        print("calculating recommand stock ...")
        recomand = dict()
        pchange = dict()
        count = 0
        for line in self.news_list:
            if line[1] == '':
                continue

            stock_data = get_stock_data(line[1], self.yesterday.strftime("%Y-%m-%d"))
            i = 1
            while stock_data is None:
                stock_data = get_stock_data(line[1], (self.yesterday + timedelta(days = - i)).strftime("%Y-%m-%d"))
                i += 1
                if i > 10:
                    break
            if i > 10:
                continue
            volume = stock_data[4]
            v_ma5 = stock_data[10]
            vol = volume * 1.0 / v_ma5
            
            x_test = pd.DataFrame([[line[2], line[3], line[4], vol]], columns = ['total', 'good', 'bad', 'vol'])
            x_array = np.array(x_test)
            try:
                res = self.cls.predict(x_array)
            except:
                res = 0
                print("fail to predict " + line[1] + " in " + self.now.strftime("%Y-%m-%d"))
            if res == 1:
                recomand[str(line[1])] = line[3]
        print(len(recomand))
        self.recomand = recomand
    
        print("the recomanded stocks are:")
        
    def store_recomand(self):
        self.count = 0
        for row in sorted(self.recomand.items(), key = lambda asd:asd[1], reverse = True):
            if row[0] in self.fin_co:
                continue
            print(row[0] + " " + str(row[1]))
            #insert_sql = "insert into recomand_stock (time, stockcode) values ('" + now.strftime("%Y-%m-%d %H:%M:%S") + "', '" + row[0] + "')"
            #cursor.execute(insert_sql)
            #db.commit()
            self.count += 1
            if self.count == 10:
                break


if __name__ == '__main__':
    a = predict()
    a.conn()
    a.get_logistic()
    a.get_fin_co()
    a.predict_data()
    a.store_recomand()
