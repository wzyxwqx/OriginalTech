# encoding:utf-8
import pymysql
from datetime import datetime
from datetime import timedelta

if __name__ == '__main__':
    now = datetime.now() + timedelta(hours = 8)
    db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
    cursor = db.cursor()
    if cursor != None:
        print('Connect to mysql successfully')
    else:
        print('Failed to connect to mysql')
    check_sql = "select time, stockcode, total, good, bad from senti_stat where time > '" + now.strftime("%Y-%m-%d") + " 00:00:00'"
    cursor.execute(check_sql)
    news_list = cursor.fetchall()
    if len(news_list) > 0:
        print('Crawler got news successfully!')
        print('Got ' + str(len(news_list)) + ' news')
    else:
        print('Crawler failed to get news!')
