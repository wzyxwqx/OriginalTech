import pickle as pk
import pymysql
import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime
from datetime import timedelta

db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()

if __name__ == "__main__":
    now = datetime.now() + timedelta(hours = 16)
    model_path = open("logistic_model.pkl", "rb")
    cls = pk.load(model_path)
    check_sql = "select time, stockcode, total, good, bad from senti_stat where time > '2018-12-06 00:00:00' and time < '2018-12-07 00:00:00'"# + now.strftime("%Y-%m-%d") + " 00:00:00'"
    cursor.execute(check_sql)
    news_list = cursor.fetchall()
    cursor.close()
    print("calculating recommand stock ...")
    recomand = dict()
    for line in news_list:
        stock_data = ts.get_hist_data(line[1], start = (now + timedelta(days = -1)).strftime("%Y-%m-%d"), end = (now + timedelta(days = -1)).strftime("%Y-%m-%d"))
        i = 1
        while stock_data is None or stock_data.empty:
            stock_data = ts.get_hist_data(line[1], start = (now + timedelta(days = -i)).strftime("%Y-%m-%d"), end = (now + timedelta(days = -i)).strftime("%Y-%m-%d"))
            i += 1
            if i > 10:
                break
        if i > 10:
            continue
        for row in stock_data.iterrows():
            volume = row[1][4]
            v_ma5 = row[1][10]
        vol = volume * 1.0 / v_ma5
        x_test = pd.DataFrame([[line[2], line[3], line[4], vol]], columns = ['total', 'good', 'bad', 'vol'])
        x_array = np.array(x_test)
        res = cls.predict(x_array)
        if res == 1:
            print(line[1])
            recomand[str(line[1])] = line[3]
    print("finish!")
    print(len(recomand))
    print("the recomanded stocks are:")
    count = 0
    for key, value in sorted(recomand.items(), key = lambda asd:asd[0], reverse = False).items():
        print(key + " " + str(good))
        count += 1
        if count == 3:
            break
