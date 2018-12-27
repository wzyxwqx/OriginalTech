#!encoding:utf-8
import pymysql
import tushare as ts
import numpy as np
import pandas as pd
import pickle as pk
from sklearn.linear_model import LogisticRegression
from datetime import datetime
from datetime import timedelta

db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()

db2 = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "stock_data", charset = "utf8")
cursor2 = db2.cursor()

if __name__ == "__main__":
    print("collecting stock data ...")
    check_sql = "select stockcode, stockname from stock"
    cursor2.execute(check_sql)
    stock_data = dict()
    for line in cursor2:
        stock_data[line[0]] = line[1]
    cursor2.close()

    print("constructing data set ...")
    now = datetime.now() #+ timedelta(hours = 16)
    #pre_time = now + timedelta(days = -3)
    check_sql = "select time, stockcode, total, good, bad from senti_stat"
    cursor.execute(check_sql)
    
    data = pd.DataFrame(columns = ['pchange', 'total', 'good', 'bad', 'vol'])
    count = 0
    for line in cursor:
        stock_data = ts.get_hist_data(line[1], start = line[0].strftime("%Y-%m-%d"), end = line[0].strftime("%Y-%m-%d"))
        pchange = 0
        if stock_data is None:
            continue
        elif stock_data.empty:
            continue
        for row in stock_data.iterrows():
            if row[1][6] > 0:
                pchange = 1
        stock_data = ts.get_hist_data(line[1], start = (line[0] + timedelta(days = -1)).strftime("%Y-%m-%d"), end = (line[0] + timedelta(days = -1)).strftime("%Y-%m-%d"))
        i = 1
        while stock_data is None or stock_data.empty and i < 10:
            stock_data = ts.get_hist_data(line[1], start = (line[0] + timedelta(days = -i)).strftime("%Y-%m-%d"), end = (line[0] + timedelta(days = -i)).strftime("%Y-%m-%d"))
            i += 1
        if i==10:
            continue
        for row in stock_data.iterrows():
            volume = row[1][4]
            v_ma5 = row[1][10]
        vol = volume * 1.0 / v_ma5
        data = data.append(pd.DataFrame([[pchange, line[2], line[3], line[4], vol]], columns = ['pchange', 'total', 'good', 'bad', 'vol']), ignore_index = True)
        count += 1
        if count % 100 == 0:
            print(count)
    print("saving data ...")
    data.to_csv("data.csv")
    print("preparing for logistic regression ...")
    Y_train = np.array(data['pchange'])
    X_train = np.array(data['total', 'good', 'bad', 'vol'])
    cls = LogisticRegression(multi_class = 'multinomial',solver = 'lbfgs')
    cls.fit(X_train, Y_train)
    output = open("logistic_model.pkl", "wb")
    s = pk.dump(cls, output)
    output.close()

    print("finish trainning!")

