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

db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()

db2 = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "stock_data", charset = "utf8")
cursor2 = db2.cursor()

def ts_get(stockcode, time):
    stock_data = ts.get_hist_data(stockcode, start = (time + timedelta(days = -10)).strftime("%Y-%m-%d"), end = time.strftime("%Y-%m-%d"),retry_count=5, pause=0.1)
    i = 0
    '''
    while stock_data is None or stock_data.empty:
        stock_data = ts.get_hist_data(stockcode, start = (time + timedelta(days = -i)).strftime("%Y-%m-%d"), end = (time + timedelta(days = -i)).strftime("%Y-%m-%d"),retry_count=5, pause=0.1)
        i += 1
        if i > 10:
            break
    if i > 10:
        return 0
    '''
    #print(stock_data)
    stack = list()
    vol = list()
    for row in stock_data.iterrows():
        volume = row[1][4]
        v_ma5 = row[1][10]
        stack.append(volume/v_ma5)
    while len(stack) > 0:
        vol.append(stack.pop())
        i += 1
        if i >= 3:
            break
    return vol

def tsc_get(stockcode, time):
    count = 0
    vol = list()
    for i in range(0,10):
        stock_data = get_stock_data(stockcode, (time + timedelta(days = -i)).strftime("%Y-%m-%d"))
        if stock_data is None:
            continue
        volume = stock_data[4]
        v_ma5 = stock_data[10]
        vol.append(volume/v_ma5)
        count += 1
        if count >= 3:
            break
    return vol

if __name__ == "__main__":
    print("collecting stock data ...")
    check_sql = "select stockcode, stockname from stock"
    cursor2.execute(check_sql)
    stock_data = dict()
    for line in cursor2:
        stock_data[line[0]] = line[1]
    cursor2.close()

    print("constructing data set ...")
    now = datetime.now() + timedelta(hours = 8)
    #pre_time = now + timedelta(days = -3)
    check_sql = "select time, stockcode, total, good, bad from senti_stat"
    cursor.execute(check_sql) 
    data = pd.DataFrame(columns = ['pchange', 'total', 'good', 'bad', 'total1', 'good1', 'bad1', 'total2', 'good2', 'bad2', 'vol', 'vol1', 'vol2'])
    count = 0
    stat_table = cursor.fetchall()
    check_sql = "select total, good, bad, stockcode, time from senti_stat"
    cursor.execute(check_sql)
    res = cursor.fetchall()
    senti = pd.DataFrame(list(res))
    for line in stat_table:
        #stock_data = ts.get_hist_data(line[1], start = line[0].strftime("%Y-%m-%d"), end = line[0].strftime("%Y-%m-%d"),retry_count=5, pause=0.1)
        #pchange = 0
        #if stock_data is None or stock_data.empty:
        #    continue
        #for row in stock_data.iterrows():
        #    if row[1][6] > 0:
        #        pchange = 1
        stock_data = get_stock_data(line[1], line[0].strftime("%Y-%m-%d"))
        if stock_data is None:
            continue
        if stock_data[6] > 0:
            pchange = 1
        else:
            pchange = 0
        #check_sql = "select total, good, bad from senti_stat where stockcode = '" + line[1] + "' and time < '" + line[0].strftime("%Y-%m-%d") + " 00:00:00' and time > '" + (line[0] +timedelta(days = -1)).strftime("%Y-%m-%d") + " 00:00:00'"
        #cursor.execute(check_sql)
        #line1 = [0,0,0]
        #for row in cursor:
        #    line1[0] = row[0]
        #    line1[1] = row[1]
        #    line1[2] = row[2]
        line1 = [0,0,0]
        for row in senti[(senti[3] == line[1]) & (senti[4] < line[0].strftime("%Y-%m-%d")) & (senti[4] > (line[0] + timedelta(days = -1)).strftime("%Y-%m-%d"))].iterrows():
            line1[0] = row[1][0]
            line1[1] = row[1][1]
            line1[2] = row[1][2]
        #check_sql = "select total, good, bad from senti_stat where stockcode = '" + line[1] + "' and time < '" + (line[0] +timedelta(days = -1)).strftime("%Y-%m-%d") + " 00:00:00' and time > '" + (line[0] +timedelta(days = -2)).strftime("%Y-%m-%d") + " 00:00:00'"
        #cursor.execute(check_sql)
        #line2 = [0,0,0]
        #for row in cursor:
        #    line2[0] = row[0]
        #    line2[1] = row[1]
        #    line2[2] = row[2]
        line2 = [0,0,0]
        for row in senti[(senti[3] == line[1]) & (senti[4] < (line[0] + timedelta(days = -1)).strftime("%Y-%m-%d")) & (senti[4] > (line[0] + timedelta(days = -2)).strftime("%Y-%m-%d"))].iterrows():
            line2[0] = row[1][0]
            line2[1] = row[1][1]
            line2[2] = row[1][2]
        vol = tsc_get(line[1], line[0] + timedelta(days = -1))
        if len(vol) <= 2:
            continue
        data = data.append(pd.DataFrame([[pchange, line[2], line[3], line[4], line1[0], line1[1], line1[2], line2[0], line2[1], line2[2], vol[0], vol[1], vol[2]]], columns = ['pchange', 'total', 'good', 'bad', 'total1', 'good1', 'bad1', 'total2', 'good2', 'bad2', 'vol', 'vol1', 'vol2']), ignore_index = True)
        count += 1
        if count % 1000 == 0:
            print(count)
    print("saving data ...")
    data.to_csv("new_log_data.csv")

    data = pd.read_csv("new_log_data.csv")
    print("preparing for logistic regression ...")
    Y_train = np.array(data[['pchange']])
    X_train = np.array(data[['total', 'good', 'bad', 'total1', 'good1', 'bad1', 'total2', 'good2', 'bad2', 'vol', 'vol1', 'vol2']])
    cls = LogisticRegression(multi_class = 'multinomial',solver = 'lbfgs')
    cls.fit(X_train, Y_train.astype('int'))
    output = open("new_logistic_model.pkl", "wb")
    s = pk.dump(cls, output)
    output.close()

    print("finish trainning!")

