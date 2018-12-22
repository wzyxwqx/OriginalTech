import pymysql
import datetime
import jieba.analyse
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import pandas as pd
import tushare as ts
from tushare_copy import get_stock_data

# Fetching data
print('===========================================')
print('    start Fetching')
db = pymysql.connect(host = '165.227.30.65', user = 'mlf', passwd = 'mashiro120', db = 'crawled_news', charset = 'utf8')
cursor = db.cursor()

now_date = datetime.datetime.now()
print('now:',now_date)
start_date = now_date + datetime.timedelta(days=-20)
print('start:',start_date)
end_date = now_date + datetime.timedelta(days=-7)
print('end:',end_date)
check_sql = "select title, content, keystock, time from news where keystock != ''  and time between "\
            + "'%s'"%(start_date.strftime('%Y-%m-%d')) + " and " + "'%s'"%(end_date.strftime('%Y-%m-%d')) +" order by time desc";
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


# label data
def get_p_change(stock, date):
    ts_df = get_stock_data(stock, date)
    if ts_df is None:
        return(0)
    now_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    error_count = 0
    while ts_df.empty and error_count < 6:
        error_count += 1
        now_date = now_date + datetime.timedelta(days=1)
        new_date = now_date.strftime('%Y-%m-%d')
        ts_df = get_stock_data(stock, new_date)
    if ts_df.empty:
        ans = 0
    else:
        ans = ts_df.p_change
        if ans > 0.5:
            ans = 1
        else:
            ans = -1
    return(ans)


print('===========================================')
print('    start labeling')
y_train = []
count = 0
for line in range(news_size):
    count += 1
    print('labeling:', count, '/', news_size)
    stocklist = keystock_info[line].split()
    total_p_change = 0
    for stock in stocklist:
        total_p_change = total_p_change + get_p_change(stock, date_info[line].strftime('%Y-%m-%d'))
    if total_p_change > 0:
        y_train.append(1)
    else:
        y_train.append(0)

print('    end labeling')


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
print('   start TFIDF')
vectorizer = TfidfVectorizer()
vectorizer.fit(content_S)
X = vectorizer.transform(content_S)
print('TFIDF matrix shape:', X.shape)
print('    end TFIDF')



# naive bayes
print('===========================================')
print('   start Training')
classifier = MultinomialNB()
classifier.fit(vectorizer.transform(content_S), y_train)

joblib.dump(classifier, 'Naive_bayes.pkl')
joblib.dump(vectorizer, 'Tfidf_vec.pkl')
print('   end Training')

