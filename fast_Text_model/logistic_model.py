#!encoding:utf-8
import pymysql
import tushare as ts
import numpy as np
import pandas as pd
import pickle as pk
from sklearn.linear_model import LogisticRegression
from datetime import datetime
from datetime import timedelta
from tushare_copy import get_stock_data

'''logistic.model.py

The data used for analysis is all from databases in server.
The good & bad label data comes from senti_stat which is 
updated by news_stock_count.py

'''
# Database 1 - crawled_news : store crawled news.
db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()
# Database 2 - stock_data   : store stock related data.
db2 = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "stock_data", charset = "utf8")
cursor2 = db2.cursor()

if __name__ == "__main__":


    # Collect stock data from SQL in server.
    print("collecting stock data ...")
    check_sql = "select stockcode, stockname from stock"
    cursor2.execute(check_sql)
    stock_data = dict()
    for line in cursor2:
        stock_data[line[0]] = line[1]
    cursor2.close()


    # Collect stat_table from senti_stat in database 1.
    # senti_stat get updated by news_stock_count.py
    print("constructing data set ...")
    now = datetime.now() + timedelta(hours = 8)
    check_sql = "select time, stockcode, total, good, bad from senti_stat"
    cursor.execute(check_sql)
    data = pd.DataFrame(columns = ['pchange', 'total', 'good', 'bad', 'vol'])
    count = 0
    stat_table = cursor.fetchall()


    # Use stored tushare data to organize stock_data.
    # Find more information about specific stock.
    for line in stat_table:
        if line[1] == '':
            continue
        stock_data = get_stock_data(line[1], line[0].strftime("%Y-%m-%d"))
        if stock_data is None:
            continue
        pchange = 0
        if stock_data[6] > 0:
            pchange = 1
        stock_data = get_stock_data(line[1], (line[0] + timedelta(days = -1)).strftime("%Y-%m-%d"))
        i = 1
        while stock_data is None:
            i += 1
            stock_data = get_stock_data(line[1], (line[0] + timedelta(days = -i)).strftime("%Y-%m-%d"))
            if i > 10:
                break
        if i > 10:
            continue
        volume = stock_data[4]
        v_ma5 = stock_data[10]
        vol = volume * 1.0 / v_ma5
        data.append(pd.DataFrame([[pchange, line[2], line[3], line[4], vol]], columns = ['pchange', 'total', 'good', 'bad', 'vol']), ignore_index = True)
        count += 1
        # Print every 1000 stocks.
        if count % 1000 == 0:
            print(count)
    # Store data
    print("saving data ...")
    data.to_csv("log_data.csv")


    # Logistic regression training.
    data = pd.read_csv("data.csv")
    print("preparing for logistic regression ...")
    Y_train = np.array(data[['pchange']])
    X_train = np.array(data[['total', 'good', 'bad', 'vol']])
    cls = LogisticRegression(multi_class = 'multinomial',solver = 'lbfgs')
    cls.fit(X_train, Y_train)
    output = open("new_logistic_model.pkl", "wb")
    s = pk.dump(cls, output)
    output.close()

    print("finish trainning!")

