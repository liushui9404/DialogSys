# coding:utf-8

import random
import pickle

from sklearn import svm
from sklearn.externals import joblib

from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


def genZeroList(size):
    v = []
    for i in range(size):
        v.append(0)
    return v

def buildLabel(trainSize1,trainSize2):
    # train1为正样本  2为负样本
    y = []
    for i in range(trainSize1):
        y.append(0)  # 正样本
    for i in range(trainSize2):
        y.append(1)  # 负样本
    return y
        



def buildTrainData():
    f0 = open("./w2v",'rb')
    w2v = pickle.load(f0)
    f0.close()
    f1 = open("./正样本","r")
    sentences1 = f1.readlines()
    sentenceList1 = []
    for sentence in sentences1:
        temp = []
        sent = sentence.split()
        lenSent = len(sent)
        for i in range(10):  # 一句话最多10个词
            if i<lenSent:
                temp.extend(list(w2v[sent[i]]))
            else:
                temp.extend(genZeroList(30))
        sentenceList1.append(temp)
    trainSize1 = len(sentenceList1)
    f1.close()  

    f2 = open("./负样本","r")
    sentences2 = f2.readlines()
    sentenceList2 = []
    for sentence in sentences2:
        temp = []
        sent = sentence.split()
        lenSent = len(sent)
        for i in range(10):  # 一句话最多10个词
            if i<lenSent:
                temp.extend(list(w2v[sent[i]]))
            else:
                temp.extend(genZeroList(30))
        sentenceList2.append(temp)
    f2.close()

    trainSize2 = len(sentenceList2) 
    x = sentenceList1+sentenceList2
    y = buildLabel(trainSize1,trainSize2)
    return x,y


X_train,Y_train = buildTrainData()
# -------------------------------------SVM-----------------------------------------
clf = svm.SVC(C=1)
clf.fit(X_train,Y_train)
joblib.dump(clf, "./filterModel.m")  # 保存模型
y_pred_svm = clf.predict(X_train)
# print (len(y_pred))
# print(classification_report(y_pred_svm,Y_test))
p_svm = precision_score(Y_train,y_pred_svm,average='macro')
r_svm = recall_score(Y_train,y_pred_svm,average='macro')
print('SVM-P: ',p_svm)
print('SVM-R: ',r_svm)