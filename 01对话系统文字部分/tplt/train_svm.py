# coding:utf-8
import numpy as np 
from sklearn import svm
import data
from sklearn.externals import joblib

from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

X_train,Y_train = data.build_data('/home/liu/新论文/语料/整理中/初步完成/用于评价',embedding_size=30,max_len=25)
# X_test,Y_test = data.build_dev('/Users/liutong/新论文/语料/整理中/初步完成/test_set',embedding_size=30,max_len=25)

def f1(p,r):
    return 2*p*r/(p+r)


# 通过调参数改变拟合的情况


#--------------------------------------SVM-----------------------------------------
clf = svm.SVC(C=31)
clf.fit(X_train,Y_train)
joblib.dump(clf, "svm_model.m")  # 保存模型
y_pred_svm = clf.predict(X_train)
# print (len(y_pred))
# print(classification_report(y_pred_svm,Y_test))
p_svm = precision_score(Y_train,y_pred_svm,average='macro')
r_svm = recall_score(Y_train,y_pred_svm,average='macro')
print('SVM-P: ',p_svm)
print('SVM-R: ',r_svm)
print('SVM-F1: ',f1(p_svm,r_svm))


#----------------------------------------------------------------------------------
