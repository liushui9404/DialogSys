# coding:utf-8

from sklearn.externals import joblib
import pickle

class sentenceFilter(object):
    def __init__(self):
        self.on = True  # 将过滤器打开
        self.state = True  # 表示过滤器并没有将该句话过滤掉，说明这句话是任务相关
        self.clf = joblib.load("/home/liu/00毕业课题/developing/01对话系统文字部分/filter/filterModel.m")  # 加载之前的SVM模型
        self.w2v = self.loadW2V()  # 加载词向量字典
        
    def loadW2V(self):
        f = open("/home/liu/00毕业课题/developing/01对话系统文字部分/filter/w2v",'rb')
        w2v = pickle.load(f)
        f.close()
        return w2v

    def toString(self,cutedSentence):  # 去掉开头与结尾BOS EOS
        sentence = cutedSentence[0]
        sentList = sentence.split()
        return sentList[1:-1]

    def genZeroList(self,size):
        v = []
        for i in range(size):
            v.append(0)
        return v

    
    def buildInput(self,cutedSentence):
        sent = self.toString(cutedSentence)
        print("sent",sent)
        temp = []
        lenSent = len(sent)
        for i in range(10):  # 一句话最多10个词
            if i<lenSent:
                temp.extend(list(self.w2v[sent[i]]))
            else:
                temp.extend(self.genZeroList(30))
        return [temp]

    def filtSent(self,cutedSentence):
        inputSent = self.buildInput(cutedSentence)
        # print("inputSent",inputSent)
        res = self.clf.predict(inputSent)[0]
        print("res",res)

        if res == 0:
            self.state = True  #　是任务相关
        else:
            self.state = False  # 闲聊


def test():
    cutedSentence = ['BOS 王 老师 的 办公室 在 哪 EOS']    
    sentFilter = sentenceFilter()
    # print(sentFilter.buildInput(cutedSentence))
    sentFilter.filtSent(cutedSentence)
    


# test()
    