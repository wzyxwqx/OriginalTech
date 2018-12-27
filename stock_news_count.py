#!encoding:utf-8
import pymysql
from NewsPredict import predict
from datetime import datetime
from datetime import timedelta

db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()

if __name__ == "__main__":
    print("select recent news from database ...")
    now = datetime.now() + timedelta(hours = 8)
    for i in range(1, 2):
        pre_time = now + timedelta(days = -i)
        cur_time = pre_time + timedelta(days = 1)
        print("select news before " + cur_time.strftime("%Y-%m-%d") + " 09:10:00")
        check_sql = "select title, time, keystock from news where time > '" + pre_time.strftime("%Y-%m-%d") + " 09:10:00' and time < '" + cur_time.strftime("%Y-%m-%d") + " 09:10:00' and keystock != ''"
        cursor.execute(check_sql)
        news = cursor.fetchall()
        stock_good = dict()
        stock_bad = dict()
        stock_total = dict()
        for line in news:
            senti = predict(line[0])[0][0]
            keystocks = line[2].split(" ")
            for stock in keystocks:
                if stock in stock_total:
                    stock_total[stock] += 1
                    if senti == "__label__1":
                        stock_good[stock] += 1
                    elif senti == "__label__2":
                        stock_bad[stock] += 1
                else:
                    stock_total[stock] = 1
                    if senti == "__label__1":
                        stock_good[stock] = 1
                        stock_bad[stock] = 0
                    elif senti == "__label__2":
                        stock_bad[stock] = 1
                        stock_good[stock] = 0
                    else:
                        stock_good[stock] = 0
                        stock_bad[stock] = 0
    
        for key, value in stock_total.items():
            good = stock_good[key]
            bad = stock_bad[key]
            insert_sql = "insert into senti_stat (time, stockcode, total, good, bad) values ('%s', '%s', '%d', '%d', '%d')"
            cursor.execute(insert_sql % ((cur_time.strftime("%Y-%m-%d") + " 09:10:00"), key, value, good, bad))
            db.commit()
    print("finish!")


