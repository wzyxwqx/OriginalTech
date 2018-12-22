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


# organize data
print('===========================================')
print('  stock data processing..')
stock_dict = {}
for line in range(news_size):
    stocklist = keystock_info[line].split()
    for stock in stocklist:
        if stock in stock_dict:
            stock_dict[stock] += content_info[line]
        else:
            stock_dict[stock] = content_info[line]
stock_code = list(stock_dict.keys())
stock_news = list(stock_dict.values())
print('   done.')

# jieba cut
print('===========================================')
print('   start jieba cut')
def jieba_keywords(news):
    keywords = jieba.analyse.extract_tags(news, topK=20)
#    keywords_cp = keywords[:]
#    for word in keywords_cp:
#        if word.isdigit():
#            keywords.remove(word)
    return keywords


content_df = pd.DataFrame(stock_news, columns=['content'])
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
stock_proba = [x[0] for x in predict_res]
stock_predict = list(zip(stock_code, stock_proba, content_S))

# sort
stock_predict.sort(key=lambda x : x[1], reverse=True)
for line in range(10):
    print('Rank :',line,' / 10:')
    print('Code :',stock_predict[line][0])
    print('Proba:',stock_predict[line][1])
    print('Related keywords:',jieba_content[line])

print('feature:', vectorizer.get_feature_names()[0:100])
print('feature:', vectorizer.get_feature_names()[-100:-1])
