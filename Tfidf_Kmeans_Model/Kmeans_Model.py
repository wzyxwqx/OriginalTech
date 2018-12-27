# coding=utf-8
import numpy as np
import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import tushare as ts
import datetime


def get_news_data(filename):
    # 获取数据，重命名columns，分词，再存储
    csv_data = pd.read_csv(filename, error_bad_lines=False, encoding='utf-8')
    csv_data.columns = ['time', 'title', 'content', 'keystock', 'source']
    #csv_data.drop(['id'], axis=1, inplace=True)
    #csv_data.content[pd.isnull(csv_data.content)]
    csv_data.content = csv_data.content.fillna('999')
    nalist = csv_data[(csv_data.content=='999')].index.tolist()
    csv_data = csv_data.drop(nalist)
    csv_data['cut_content'] = ''
    news = jieba_cut(csv_data)
    #news.to_csv('cut_news.csv', index=False)
    return news


def get_stop_words(STWPath):
    stopwords = [line.strip() for line in open(STWPath, 'r', encoding='utf-8').readlines()]
    return stopwords


def jieba_cut(news_data):
    stopwords = get_stop_words('Chinese_Stop_Words')
    jieba.load_userdict('finance_dict_new')
    data_tmp = news_data.copy()
    for index, row in data_tmp.iterrows():
        outstr = []
        sentence_seged = list(jieba.cut(row.content))
        for word in sentence_seged:
            if word not in stopwords and len(word) > 1:
                outstr.append(word)
        data_tmp['cut_content'][index] = ' '.join(outstr)
    return data_tmp


def get_content(news_data):
    data = []
    for index, row in news_data.iterrows():
        data.append(row.cut_content)
    return data


def label_content(time, stockid):
    '''
    :param time:str 日期 y-m-d
    :param stockid: str 股票代码 6位
    :return: 股票涨跌幅度与涨跌标识
    '''
    start_time = datetime.datetime.strptime(time, '%Y-%m-%d')
    delta = datetime.timedelta(days=7)
    next_time = start_time + delta
    start_day = time
    next_day = next_time.strftime('%Y-%m-%d')
    hist_data = ts.get_hist_data(stockid, start=start_day, end=next_day)
    #hist_data = pro.daily(ts_code=stockid, start_date=start_day, end_date=next_day)
    if hist_data is None:
        pchange = 0
        ans = -1
    elif (hist_data.empty):
        pchange = 0
        ans = -1
    else:
        pchange = hist_data.p_change[0]
        if pchange > 0:
            ans = 1
        else:
            ans = 0
    return [pchange, ans]


def train_tfidf_kmeans(news):
    # 随机抽取6000数据用于tfidf模型和kmeans模型计算
    train_data = news.sample(frac=0.3)
    data = get_content(train_data)

    # 训练tfidf计算模型
    vectorizer = TfidfVectorizer(max_features=8000)
    tfidf = vectorizer.fit_transform(data)

    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()

    # 50类聚类
    clf = KMeans(n_clusters=50)
    s = clf.fit(tfidf)

    # 存储
    joblib.dump(vectorizer, 'Tf_idf.pkl')
    joblib.dump(s, 'Km_50.pkl')


def label_kmeans_type(news):
    '''
    :param news:
    :return:使用kmeans分辨该cut_content属于哪一类
    '''
    #加载tfidf与kmeans模型
    vectorizer = joblib.load('Tfidf.pkl')
    km_50 = joblib.load('km_50.pkl')

    news['type'] = -1
    for index, row in news.iterrows():
        print(index)
        tfidf = vectorizer.transform([news.cut_content[index]])
        news['type'][index] = km_50.predict(tfidf)[0]


def count_stock_related_news(news):
    '''
    分析每支股票每天的涨跌以及其相关的新闻种类、数目
    :param news: dataframe
    :return: stock_count:dataframe
    '''
    stock_count = pd.DataFrame(columns=['stock_id', 'date', 'p_change', 'label',
                                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                        '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                                        '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                                        '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
                                        '40', '41', '42', '43', '44', '45', '46', '47', '48', '49'])
    for index, row in news.iterrows():
        date = row.time[0:10]
        stocks = row.keystock.split()
        for stock_id in stocks:
            df1 = stock_count[stock_count['date'].isin([date])]
            df2 = df1[df1['stock_id'].isin([stock_id])]
            if df2.empty:
                stock_count = stock_count.append({
                    'stock_id': stock_id, 'date': date, 'p_change': 0.0, 'label': -1,
                    '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0,
                    '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0,
                    '20': 0, '21': 0, '22': 0, '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0,
                    '30': 0, '31': 0, '32': 0, '33': 0, '34': 0, '35': 0, '36': 0, '37': 0, '38': 0, '39': 0,
                    '40': 0, '41': 0, '42': 0, '43': 0, '44': 0, '45': 0, '46': 0, '47': 0, '48': 0, '49': 0
                }, ignore_index=True)
                ty = str(row.type)
                inx = len(stock_count)-1
                stock_count[ty][inx] = stock_count[ty][inx] + 1
            else:
                inx = df2.index[0]
                tmp = stock_count[str(row.type)][inx]
                stock_count[str(row.type)][inx] = tmp + 1
    return stock_count


if __name__ == '__main__':
    #读取分词后的数据
    news = pd.read_csv('count_df.csv', error_bad_lines=False, encoding='utf-8')
    '''
    stop = True
    for index, row in news.iterrows():
        if 8001 > index >1999:
            print(index)
            stockid = str(row.stock_id).zfill(6)
            ans = label_content(row.date, stockid)
            news['p_change'][index] = ans[0]
            news['label'][index] = ans[1]
    news.to_csv('count_df.csv', index=False)
    '''

    X_train, X_test, y_train, y_test = train_test_split(news.iloc[:, 4:54], news.iloc[:, 3],
                                                        test_size=0.5)
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    p = np.mean(y_pred == y_test)
