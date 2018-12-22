import pymysql
import datetime
import jieba.analyse
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import pandas as pd
import tushare as ts


# Fetching data
print('===========================================')
print('    start Fetching')
db = pymysql.connect(host = '165.227.30.65', user = 'mlf', passwd = 'mashiro120', db = 'crawled_news', charset = 'utf8')
cursor = db.cursor()

now_date = datetime.datetime.now() + datetime.timedelta(hours=8)
print('now:',now_date)
start_date = now_date + datetime.timedelta(days=-7)
print('start:',start_date)
check_sql = "select title, content, keystock, time from news where keystock != ''  and time between "\
        + "'%s'"%(start_date.strftime('%Y-%m-%d')) + " and " + "'%s'"%(now_date.strftime('%Y-%m-%d %H:%M:%S')) +" order by time desc";
print(check_sql)
cursor.execute(check_sql)
result = cursor.fetchall()

title_info = []
content_info = []
keystock_info = []
date_info = []
for line in result:
    title_info.append(line[0])
    content_info.append(line[1])
    keystock_info.append(line[2])
    date_info.append(line[3])
news_size = len(title_info)
print('size of data:', news_size)
print('    end Fetching')

# jieba cut
print('===========================================')
print('   start jieba cut')
def jieba_keywords(news):
    keywords = jieba.analyse.extract_tags(news, topK=20)
    return keywords


content_df = pd.DataFrame(content_info, columns=['content'])
jieba.analyse.set_stop_words("stopwords2")
jieba_content = content_df.content.apply(jieba_keywords)

content_S = []
for line in jieba_content:
    content_S.append(' '.join(line))

print('    end jieba cut')


# TFIDF
print('===========================================')
print('   Loading TFIDF Vectorizer')
vectorizer = joblib.load("Tfidf_vec.pkl")
print('   Loading Complete')



# naive bayes
print('===========================================')
print('   Loading Bayes Model')
classifier = joblib.load("Naive_bayes.pkl")
print('   Loading Complete')

# organize results
predict_res = classifier.predict_proba(vectorizer.transform(content_S))
stock_predict = {}

for line in range(news_size):
    stocklist = keystock_info[line].split()
    for stock in stocklist:
        if stock in stock_predict:
            stock_predict[stock] += predict_res[line][0] - predict_res[line][1]
        else:
            stock_predict[stock] = predict_res[line][0] - predict_res[line][1]


# sort
stock_predict_items = stock_predict.items()
back_items = [[v[1], v[0]] for v in stock_predict_items]
back_items.sort(reverse=True)
ranking = [[v[1], v[0]] for v in back_items]
print(ranking[0:10])
