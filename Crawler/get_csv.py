import pymysql
import pandas as pd

db = pymysql.connect(host = "localhost", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()

check_sql = "select time, title, content, keystock, source from news where keystock != '' order by time desc limit 2000"
cursor.execute(check_sql)
data = cursor.fetchall()
frame = pd.DataFrame(list(data))
frame.to_csv("news_12_13.csv", index=False)
print("finish")
