#!encoding=utf-8
import jieba
import fastText

def predict(line):
    model_path = "/root/originaltech/fastText_model/fast_model_title_upload.bin"
    classifier = fastText.load_model(model_path)
    try:
        data = ' '.join(jieba.cut(line.strip().replace('\t', ' ').replace('\n', ' '), cut_all = False))
        res = classifier.predict(data)
        return res
    except:
        print("fail to predict senti")
