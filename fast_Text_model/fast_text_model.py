#!encoding:utf-8
import jieba
import pymysql
import fastText

db = pymysql.connect(host = "165.227.30.65", user = "mlf", passwd = "mashiro120", database = "crawled_news", charset = "utf8")
cursor = db.cursor()

if __name__ == "__main__":
    print("reading stop words ...")
    f = open("Chinese_Stop_Words.txt", "r", encoding = 'utf-8')
    lines = f.readlines()
    stop_words = [line.strip() for line in lines]
    f.close()
    print("finish reading stop words!")
    jieba.load_userdict("finance_dict_new")
    print("reading & processing news from mysql ...")
    for count in range(1,50):
        check_sql = "select title, senti1 from news where keystock != '' and senti1 != '' and id > " + str((count-1) * 20000) + " and id < " + str(count * 20000)
        cursor.execute(check_sql)
        news_list = cursor.fetchall()
        f_out = open("training_data_title", "a+", encoding = 'utf-8')
        for line in news_list:
            out_line = "__label__" + str(line[1]) + " "
            seg_title = jieba.cut(line[0].replace("\t", " ").replace("\n", " "))
            #seg_content = jieba.cut(line[1].replace("\t", " ").replace("\n", " "))
            seg_title = filter(lambda x : x not in stop_words, seg_title)
            #seg_content = filter(lambda x : x not in stop_words, seg_content)
            out_line += " ".join(seg_title)# + " " + " ".join(seg_content)
            #out_line = " ".join(seg_title) + " " + " ".join(seg_content) + "\t__label__" + str(line[2])
            #out_line += "\t__label__" + str(line[2]) + "\n"
            f_out.write(out_line + "\n")
        print(count)
    f_out.close()
    print("finish processing data!")
    print("fasttext training ...")
    classifier = fastText.train_supervised(input = 'training_data_title', epoch=50, lr=0.05, wordNgrams=5, minCount=1)
    print("finish training!")
    classifier.save_model('fast_model_V2.bin')
