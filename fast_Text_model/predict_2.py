import pickle as pk
import pymysql
import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime
from datetime import timedelta
from tushare_copy import get_stock_data

db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()

if __name__ == "__main__":
    now = datetime.now() + timedelta(hours = 8)
    model_path = open("logistic_model.pkl", "rb")
    cls = pk.load(model_path)
    check_sql = "select time, stockcode, total, good, bad from senti_stat where time > '" + now.strftime("%Y-%m-%d") + " 00:00:00'"
    f = open("listed_fin_co", "r", encoding = "utf-8")
    lines = f.readlines()
    fin_co = [line.strip() for line in lines]
    cursor.execute(check_sql)
    news_list = cursor.fetchall()
    #cursor.close()
    print("calculating recommand stock ...")
    recomand = dict()
    pchange = dict()
    count = 0
    yesterday = now + timedelta(days = -1)
    for line in news_list:
        '''
        stock_data = ts.get_hist_data(line[1], start = (now + timedelta(days = -1)).strftime("%Y-%m-%d"), end = (now + timedelta(days = -1)).strftime("%Y-%m-%d"))
        i = 1
        while stock_data is None or stock_data.empty:
            stock_data = ts.get_hist_data(line[1], start = (now + timedelta(days = -i)).strftime("%Y-%m-%d"), end = (now + timedelta(days = -i)).strftime("%Y-%m-%d"))
            i += 1
            if i > 10:
                break
        if i > 10:
            continue
        '''
        '''
        if stock_data is None or stock_data.empty:
            continue
        '''
        '''
        for row in stock_data.iterrows():
            volume = row[1][4]
            v_ma5 = row[1][10]
        '''
        if line[1] == '':
            continue
        stock_data = get_stock_data(line[1], yesterday.strftime("%Y-%m-%d"))
        i = 1
        while stock_data is None:
            stock_data = get_stock_data(line[1], (yesterday + timedelta(days = - i)).strftime("%Y-%m-%d"))
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
            res = cls.predict(x_array)
        except:
            res = 0
            print("fail to predict " + line[1] + " in " + now.strftime("%Y-%m-%d"))
        if res == 1:
            #print(line[1])
            '''
            change_data = ts.get_hist_data(line[1], start = '2018-12-12', end = '2018-12-12')
            for row in change_data.iterrows():
                change = row[1][6]
                pchange[line[1]] = change
            if change > 0:
                count += 1
            '''
            recomand[str(line[1])] = line[3]
            
    print("finish!")
    print(len(recomand))
    #print(count / len(recomand))
    print("the recomanded stocks are:")
    count = 0
    for row in sorted(recomand.items(), key = lambda asd:asd[1], reverse = True):
        if row[0] in fin_co:
            continue
        print(row[0] + " " + str(row[1]))# + " " + str(pchange[row[0]]))
        insert_sql = "insert into recomand_stock (time, stockcode) values ('" + now.strftime("%Y-%m-%d %H:%M:%S") + "', '" + row[0] + "')"
        cursor.execute(insert_sql)
        db.commit()
        count += 1
        if count == 10:
            break
