#encoding = utf-8
from pymongo import MongoClient
import os,jieba,fastText

Conn = MongoClient("localhost", 27017)
db = Conn["Sina_Stock"]
STWPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/news_analysis_model/Chinese_Stop_Words'
FNDPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/news_analysis_model/finance_dict_new'
collection = db.get_collection("sina_news_company")
article = collection.find_one({'RelevantStock': '600066 '})['Article']
stopwords = [line.strip() for line in open(STWPath, 'r').readlines()]
#finance_dict = [line.strip() for line in open(FNDPath, 'r').readlines()]
jieba.load_userdict(FNDPath)
segs=jieba.lcut(article)    #利用结巴分词进行中文分词
#segs=filter(lambda x:len(x)>1,segs)    #去掉长度小于1的词
segs=filter(lambda x:x not in stopwords,segs)    #去掉停用词
sentences = ("__lable__1"+" "+" ".join(segs))
#with open( "test",'w') as t:
#    t.write(sentences)
classifier = fastText.train_supervised('test', lr=0.1, dim=100, ws=5, epoch=5, minCount=1, minCountLabel=0, minn=0, maxn=0, neg=5, wordNgrams=1, loss='softmax', bucket=2000000, thread=12, lrUpdateRate=100, t=0.0001, label='__label__', verbose=2, pretrainedVectors='')
result = classifier.test('test')
print(result)    #准确率
