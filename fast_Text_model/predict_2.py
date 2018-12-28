# encoding=utf-8
import pickle as pk
import pymysql
import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime
from datetime import timedelta
from tushare_copy import get_stock_data

# 连接数据库
db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()

if __name__ == "__main__":
    # 获取当前时间(服务器时间比中国迟8小时)
    now = datetime.now() + timedelta(hours = 8)
    
    # 载入logistic模型
    model_path = open("logistic_model.pkl", "rb")
    cls = pk.load(model_path)
    
    # 获取今日新闻的时间、相关股票、利好利空新闻数 
    check_sql = "select time, stockcode, total, good, bad from senti_stat where time > '" + now.strftime("%Y-%m-%d") + " 00:00:00'"
    
    # 载入金融机构名单
    f = open("listed_fin_co", "r", encoding = "utf-8")
    lines = f.readlines()
    fin_co = [line.strip() for line in lines]
    cursor.execute(check_sql)
    
    news_list = cursor.fetchall()
    #cursor.close()
    
    # 获取相关股票前一天的成交量、平均成交量等信息
    print("calculating recommand stock ...")
    recomand = dict()
    pchange = dict()
    count = 0
    yesterday = now + timedelta(days = -1)
    for line in news_list:
        # 去除空数据
        if line[1] == '':
            continue
            
        # 获取十天内最近的有效相关数据，十天内均无有效数据则忽视本新闻
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
        
        # 将数据转为pd形式
        x_test = pd.DataFrame([[line[2], line[3], line[4], vol]], columns = ['total', 'good', 'bad', 'vol'])
        x_array = np.array(x_test)
        try:
            # 预测股票未来涨跌的可能性
            res = cls.predict(x_array)
        except:
            res = 0
            print("fail to predict " + line[1] + " in " + now.strftime("%Y-%m-%d"))
        if res == 1:
            recomand[str(line[1])] = line[3]
            
    print("finish!")
    print(len(recomand))
    #print(count / len(recomand))
    print("the recomanded stocks are:")
    count = 0
    # 将最有可能涨的股票存在数据库中
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
