# coding:utf-8

from sklearn.externals import joblib
import pickle
import numpy as np

def loaddict():
    input_f = open('/home/liu/新论文/classify_W/skip-gram-nopos/wordembeddings','rb') # 打开之前训练词向量的词典，词->数字
    word2vec= pickle.load(input_f)
    input_f.close()
    f_r = open('../../../01对话系统文字部分/tplt/dict_intent','rb')
    dict_intent = pickle.load(f_r)
    f_r.close()

    return word2vec,dict_intent

def sent2vec(sentList,word2vec,dict_intent,embedding_size,maxLength):
    embed_list = []
    data_list = []

    padding_random = np.random.rand(embedding_size)
    padding_0 = [0]*embedding_size

    for i in range(maxLength):
        if i<len(sentList):
            if sentList[i] in word2vec:
                embed_list.extend(word2vec[sentList[i]])
            else:
                embed_list.extend(padding_random)
        else:
            embed_list.extend(padding_0)
            
    return [embed_list]
    
def reverseIntentDict(dict_intent):
    return dict((v,k) for k,v in dict_intent.items())



# sentList = ['王恒升','老师','办公室','在','哪']
def genIntent(sentList):

    word2vec,dict_intent = loaddict()
    embedList = sent2vec(sentList,word2vec,dict_intent,embedding_size=30,maxLength=25)
    num2intent = reverseIntentDict(dict_intent)

    clf = joblib.load("../../../01对话系统文字部分/tplt/svm_model.m")
    intent = clf.predict(embedList)[0]
    return num2intent[intent]

