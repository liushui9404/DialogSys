# coding:utf-8
import aiml

from pathPlan import pathPlan

# 定义 结果生成器
class AnswerGenerator(object):
    def __init__(self):

        # 创建Kernel()和 AIML 学习文件
        self.kernel = aiml.Kernel()
        self.kernel.learn("/home/liu/00毕业课题/developing/01对话系统文字部分/aiml_files/basic_chat.aiml")
        self.kernel.respond("LOAD AIML B")  #加载basic_chat.aiml文件
        self.pathPlaner = pathPlan()
        


    # 用于把句子分开
    def setAnswerState(self,answerState):
        self.answerState = answerState  # 0是初始状态；1是只需要产生文字回答；2是不止需要产生文本，还要产生图片
        # answerState由对话管理器给定


    def split_sentence(self,sentence):
        res = ""
        for s in sentence:
            res = res + s + " "
        res = res[:-1]
        return res
    
    def final_sentence(self,ans,sent,intent):  # 用于产生最终的回答
        
        if ans!=None:
            # 去掉空格
            print("sent",sent)
            sent = [s for s in sent if s!=" "]
            # sent = "".join(sent)
            print("1111",sent)
            index_of_symbol = sent.index('#')
            if intent == 'introduce':
                temp = ''
                for k in ans:
                    if k =="gender":
                        temp = temp+'性别是'+ans[k]+';'
                    elif k=="type":
                        if "机" not in sent:
                         
                            temp = temp+'职称是'+ans[k]+':'

                    elif k=='work_in':
                        temp = temp+'所在系是'+ans[k]+';'
                    elif k=="is_located_in":
                        temp = temp+"办公室在"+ans[k]+';'
                    elif k=="research":
                        temp = temp+"研究方向是"+ans[k]+';'
                    elif k == 'history':
                        temp = temp+ans[k]+';'
                    elif k == 'num_of_teacher':
                        temp = temp+"有老师"+ans[k]+';'
                    elif k == 'num_of_stu':
                        temp = temp+"有学生"+ans[k]+';'
                        
                sent[index_of_symbol] = temp
            else:
                sent[index_of_symbol] = "".join(ans)

            sentence = "".join(sent)
        else:
            sentence = "未能检索到答案"

        return sentence

    def textAnswer(self,input_x,ans,intent,strCode):  # 产生文字回答
        if intent != "query_location":
            print("intent1111111",intent)
            print("input_x",input_x)
            a = self.split_sentence(input_x)
            print("aaa",a)
            AIMLsentence = self.kernel.respond(a)
            print("AIMLsentence",AIMLsentence)
            answerSentence = self.final_sentence(ans,AIMLsentence,intent)
        else:
            print("ans-----",ans[0])
            if strCode=="01000":
                answerSentence = self.pathPlaner.gen_path("起点",ans[0])
            else:
                a = self.split_sentence(input_x)
                print("aaa",a)
                AIMLsentence = self.kernel.respond(a)
                print("AIMLsentence11111111",AIMLsentence)

                answerSentence1 = self.final_sentence(ans,AIMLsentence,intent)
                # answerSentence = ans[0]
                answerSentence2 = self.pathPlaner.gen_path("起点",ans[0])
                print("answerSentence1",answerSentence1)
                print("answerSentence2",answerSentence2)
                answerSentence = answerSentence1+'\n'+answerSentence2

        
        return answerSentence

    def pictureAnswer(self):  # 产生图片
        pass

    def generateAnswer(self,input_x,ans,intent,strCode):  # 产生总的回答
        # self.setAnswerState(answerState)
        sentence = self.textAnswer(input_x,ans,intent,strCode)

        return sentence


# def test():
#     # input_x = '你好张三'
#     # input_x = "王恒升的办公室在哪个房间"
#     # input_x = "王恒升老师在哪层办公"
#     # input_x = "王恒升的办公室在哪"
#     # input_x = '王恒升老师的学生有谁'
#     # input_x = "王恒升老师的学生有哪些"
#     # input_x = '王恒升老师的研究方向是什么'
#     # input_x = '王恒升老师是什么系的'
#     # input_x = '王恒升老师的性别是'
#     # input_x = "姜成是谁的学生"
#     input_x = "王恒升老师办公室在哪"
#     answerGenerator = AnswerGenerator(1)
#     answerSentence = answerGenerator.generateAnswer(input_x,["A513"],"query_location")
#     print("answerSentence:",answerSentence)

# test()