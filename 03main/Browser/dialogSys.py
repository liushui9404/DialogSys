#!/usr/bin/python3.5
# -*- coding:utf-8 -*-

#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用(Web Server Gateway Interface)
from flask import Flask
import tensorflow as tf
from sklearn.externals import joblib
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
#导入前台请求的request模块
from flask import request   
import traceback  
import sys
import time
sys.path.append('../Server')
# 导入各个模块
from wordSegmentation import wordSegment  # 分词器
from sentenceFilter import sentenceFilter  # 过滤器
from NLU import NLU   # 对话理解器
from manage import Manage  # 对话管理器
from interactWithKB import InteractWithKB  # 知识交互器
from answerGenerator import AnswerGenerator  # 回答产生器


#------------------------------------------------------------------

class dialogServer(object):

    def __init__(self):
        self.wordSegmentor = wordSegment()        # 生成 分词器
        self.sentFilter = sentenceFilter()        # 生成 过滤器
        self.NLUModel = NLU()                     # 生成 对话理解器
        self.dialogueManager = Manage()           # 生成 对话管理器
        self.Interactor = InteractWithKB()        # 生成 知识交互器
        self.answerGenerator = AnswerGenerator()  # 生成 回答产生器

        self.isFirst = True  # 是一轮对话的开始
        self.isShow = "0"  # 0表示不显示图,1表示显示图
        
    
    def setIsShow(self,intent):
        if intent=="query_location":
            self.isShow = "1"
        else:
            self.isShow = "0"
        


    def dialogComplete(self):
        pass
        # 这里是 对话完成后,将一些状态置0
    
    def processSentecne(self,input_x):
        sentCuted = self.wordSegmentor.cut_sentence(input_x) # 分词

        self.sentFilter.filtSent(sentCuted)    # 过滤器处理句子

        if self.wordSegmentor.hasSentence == True:  # 保证有内容
            # 过滤器先放上吧
            # if self.sentFilter.state == True:
            if True == True:
                # 说明是任务相关的句子 

                sentence,intent,slot = self.NLUModel.nluSentence(sentCuted)   # 理解句子

                if self.isFirst == True:  # 表明是新一轮开始
                    self.strCode = self.dialogueManager.firstmanage(intent,slot,sentence)

                if self.dialogueManager.state == 2:  # 只有是完成状态才会产生答案
                    ans = self.Interactor.information_to_answer(sentence,
                                                            self.dialogueManager.intentHold,
                                                            self.dialogueManager.slotStrHold,
                                                            self.dialogueManager.slotDictHold)

                    input_x = self.dialogueManager.newSentence()
                    

                    answerSentence = self.answerGenerator.generateAnswer(input_x,ans,self.dialogueManager.intentHold,
                                                                        self.dialogueManager.slotStrHold)

                    # 这里应该有归零操作,将一些状态置为初始状态,可是是哪些状态置0呢???值得思考
                    self.isFirst = True
                    self.setIsShow(self.dialogueManager.intentHold)                    

                    return answerSentence

                elif self.dialogueManager.state == 1:  # 开启多轮对话状态
                    querySentence = self.dialogueManager.querySentence(intent,self.strCode)  # 产生问句
                    self.isFirst = False
                    self.isShow = "0"
                    return querySentence

                
                elif self.dialogueManager.state == 3:  # 处于多轮对话中
                    print("3333slot",slot)
                    print("33333sentence",sentence)
                    self.dialogueManager.informationFuse(self.dialogueManager.intentHold,slot,sentence)  # 将新旧信息融合
                    # strCode = dialogueManager.calState(intent,dialogueManager.slotStrHold)
                    self.dialogueManager.str2State(self.dialogueManager.intentHold,self.dialogueManager.slotStrHold) # 改变对话管理器状态
                    self.dialogueManager.buildSlotDict(self.dialogueManager.intentHold,slot,sentence)

                    if self.dialogueManager.state != 2:
                        print("不等于2222 ",self.dialogueManager.state)

                        querySentence = self.dialogueManager.querySentence(self.dialogueManager.intentHold,
                                                                            self.dialogueManager.slotStrHold)  # 产生问句
                        self.isFirst = False
                        self.isShow = "0"
                        return querySentence

                    else: # 完成状态
                        print("这里!!!!!")

                        ans = self.Interactor.information_to_answer(sentence,self.dialogueManager.intentHold,
                                                           self.dialogueManager.slotStrHold,
                                                           self.dialogueManager.slotDictHold)

                        input_x = self.dialogueManager.newSentence()
                        print("完成状态",self.dialogueManager.slotStrHold)
                        answerSentence = self.answerGenerator.generateAnswer(input_x,ans,self.dialogueManager.intentHold,
                                                                            self.dialogueManager.slotStrHold)
                        

                        print("self.dialogueManager.answerState",self.dialogueManager.answerState)
                        print("完成状态",answerSentence)                                                                       

                        
                        self.isFirst = True
                        self.setIsShow(self.dialogueManager.intentHold) 
                        
                        
                        return answerSentence


            else:
                return "您说的句子我暂时无法处理,请点击结束对话,将问题汇报给管理员"

        else:
            return "请输入内容"

    

def save(data):  # 将对话内容保存在本地
    
    filename = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    filename+='.txt'
    f = open('./log/'+filename,'w')
    f.write(data)
    f.close()



#传递根目录
app = Flask(__name__)

#默认路径访问登录页面
@app.route('/',methods=['GET', 'POST'])
def login():
    # intent = "query_location"
    print("--------进入初始化模块---------")
    if request.method == 'POST':

        global x3
        x3 = str(request.form['textoutput2'])
    
        if x3!="" and x3!="None":
            print("数据",x3)
            save(x3)
    
    x3 = ""
    return render_template('login.html')


@app.route('/solve',methods=['GET', 'POST'])
def show():
    print("-----------------执行----------------------")
    x1 = str(request.form['textinput1'])
    if x1 == "刘少君老师":
        x1 = "刘少军老师"
    sysRespond = mydialogServer.processSentecne(x1)
    intent = mydialogServer.dialogueManager.intentHold
    global x3
    x3 = x3+"问："+x1+"\n"+"答："+sysRespond+"\n"
    return render_template('show.html',x1 = x1,x2 = sysRespond,x3 = x3,intent=intent,isShow=mydialogServer.isShow)
    




#使用__name__ == '__main__'是 Python 的惯用法，确保直接执行此脚本时才
#启动服务器，若其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
    mydialogServer = dialogServer()
    global x3
    x3 = ""

    app.run(debug=True,threaded=False)
    # app.run(host="0.0.0.0")
    