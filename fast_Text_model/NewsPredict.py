#!encoding=utf-8
import jieba
import fastText

def predict(line):
    # load fast_text model
    model_path = "/root/originaltech/fastText_model/fast_model_V2.bin"
    classifier = fastText.load_model(model_path)
    try:
        # jieba_cut data
        data = ' '.join(jieba.cut(line.strip().replace('\t', ' ').replace('\n', ' '), cut_all = False))
        
        # predict data type
        res = classifier.predict(data)
        return res
    except:
        print("fail to predict senti")
