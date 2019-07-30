# coding:utf-8

from gensim.models import Word2Vec
import pickle
import random

def genRandomList(size):
    v = []
    for i in range(size):
        v.append(random.random())
    return v

genRandomList(5)


def trainW2V():
    f1 = open("./正样本","r")
    f2 = open("./负样本","r")
    words = set()
    sentence1 = f1.readlines()
    sentence2 = f2.readlines()
    sentences  =sentence1+sentence2
    # print(sentences)
    # sentences = ["今天 天气 怎么"]
    model = Word2Vec(sentences,size = 30,window = 1,min_count = 0,sg = 1)
    for sent in sentences:
        a = sent.split()
        for word in a:
            words.add(word)

    print(len(words))
    dictW2v  = dict()
    i = 0
    m = 0
    for word in words:
        try:
            dictW2v[word] = model.wv[word]
            i+=1
        except:
            dictW2v[word] = genRandomList(30)       
    print(i)
    # print(m)
    print(len(dictW2v))
    f3 = open("./w2v",'wb')
    pickle.dump(dictW2v,f3)
    f3.close()


    


trainW2V()
