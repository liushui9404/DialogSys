# coding:utf-8

from wordSegmentation import wordSegment  # 分词器
from sentenceFilter import sentenceFilter  # 过滤器
from NLU import NLU   # 对话理解器
from manage import Manage  # 对话管理器
from interactWithKB import InteractWithKB  # 知识交互器
from answerGenerator import AnswerGenerator  # 回答产生器

def loadFile():
    f = open("./system-test/测试文本-单轮-完成2.txt",'r')
    data = f.readlines()
    f.close()
    return data





def main():
    
    wordSegmentor = wordSegment() # 生成 分词器
    sentFilter = sentenceFilter()  # 生成　过滤器
    NLUModel = NLU()        # 生成 对话理解器
    dialogueManager = Manage()  # 生成 对话管理器
    Interactor = InteractWithKB()  # 生成 知识交互器
    answerGenerator = AnswerGenerator()  # 生成 回答产生器

    # input_x = "刘通是谁的学生"
    # input_x = "介绍一下邓华老师"
    # input_x = "邓华老师的研究方向是什么"
    # input_x = "A513是谁的办公室"
    i = 0
    data = loadFile()
    for input_x in data:
        print()
        print("输入的句子是",input_x)

        sentCuted = wordSegmentor.cut_sentence(input_x)
        # sentFilter.filtSent(sentCuted)  # 先不加过滤器
        # try:

        if wordSegmentor.hasSentence == True:  # 保证有内容
            if True == True:  #　保证是任务相关的句子
                i+=1
                print("这是第",i,"句话")
            # input_x = "王老师的办公室在哪"
            # input_x = "王恒升老师的办公室在哪"

            # intent = "query_location"
            # slot = ["first_name","teacher","o","room","o","o"]
            # slot = ["name","teacher","o","room","o","o"]

            # sentence = ["王","老师","的","办公室","在","哪里"]
            # sentence = ["王恒升","老师","的","办公室","在","哪里"]

                # sentFilter.filtSent(sentCuted)
                # print("sentCuted",sentCuted)
                sentence,intent,slot = NLUModel.nluSentence(sentCuted)
                print("intent = ",intent)

                strCode = dialogueManager.firstmanage(intent,slot,sentence)
                # print("strCode",strCode)

                if dialogueManager.state == 2:  # 只有是完成状态才会产生答案
                    print("-----单轮对话----")
                    # print("strCode",strCode)
                    ans = Interactor.information_to_answer(sentence,dialogueManager.intentHold,dialogueManager.slotStrHold,dialogueManager.slotDictHold)
                    # print("myManager.state",dialogueManager.state)
                    # print("Interactor.interactState",Interactor.interactState)
                    # print("ans",ans)
                    answerSentence = answerGenerator.generateAnswer(input_x,ans,intent,dialogueManager.answerState)
                    print("answerSentence",answerSentence)
                    print("----- 单轮结束-------")
                    print()

                elif dialogueManager.state == 1: # 开启多轮对话
                    print("----开启多轮对话----")
                    querySentence = dialogueManager.querySentence(intent,strCode)  # 产生问句
                    print(querySentence)

                elif dialogueManager.state == 3: # 处于多轮对话中
                    print("-----处于多轮对话中-----")
                    intent_new = "query_location"
                    slot_new = ["name"]
                    sentence_new = ["王恒升"]
                    dialogueManager.informationFuse(intent_new,slot_new,sentence_new)  # 将新旧信息融合
                    # strCode = dialogueManager.calState(intent,dialogueManager.slotStrHold)
                    dialogueManager.str2State(intent_new,dialogueManager.slotStrHold) # 确定对话管理器状态
                    dialogueManager.buildSlotDict(intent_new,slot_new,sentence_new)

                    # 这里改，不一定产生问句啊，有可能是完成状态，就不需要产生问句了
                    if dialogueManager.state==3:
                        querySentence = dialogueManager.querySentence(intent,strCode)  # 产生问句
                        print(querySentence)
            else:
                print("您的请求不在本系统支持范围内")
                    
            
        else:
            print("请输入内容")
        # except:
        #     print("第 ",i," 句话出现错误")

main()