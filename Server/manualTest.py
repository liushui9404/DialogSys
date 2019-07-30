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
    input_x = "介绍一下机电工程学院"
    i = 0
    # data = loadFile()
    
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
            for _ in range(5):
                if dialogueManager.state == 2:  # 只有是完成状态才会产生答案
                    print("-----单轮对话----")
                    # print("strCode",strCode)
                    print("sentence",sentence)
                    print("dialogueManager.intentHold",dialogueManager.intentHold)
                    print("dialogueManager.slotStrHold",dialogueManager.slotStrHold)
                    print("dialogueManager.slotDictHold",dialogueManager.slotDictHold)

                    ans = Interactor.information_to_answer(sentence,
                                                            dialogueManager.intentHold,
                                                            dialogueManager.slotStrHold,
                                                            dialogueManager.slotDictHold)
                    # print("myManager.state",dialogueManager.state)
                    # print("Interactor.interactState",Interactor.interactState)
                    print("ans",ans)
                    input_x = dialogueManager.newSentence()
                    print("newSentence",input_x)
                    answerSentence = answerGenerator.generateAnswer(input_x,ans,intent,dialogueManager.answerState)
                    print("answerSentence",answerSentence)
                    print("----- 单轮结束-------")
                    print()

                elif dialogueManager.state == 1: # 开启多轮对话
                    print("----开启多轮对话----")
                    querySentence = dialogueManager.querySentence(intent,strCode)  # 产生问句
                    print("querySentence",querySentence)

                elif dialogueManager.state == 3: # 处于多轮对话中
                    print("-----处于多轮对话中-----")
                    # intent_new = "query_location"
                    # slot_new = ["name"]
                    # sentence_new = ["王恒升"]
                    # input_x = "询问一个老师的办公室"
                    input_x = input("请输入句子:--- ")
                    print("dialogueManager.slotStrHold",dialogueManager.slotStrHold)
                    sentCuted = wordSegmentor.cut_sentence(input_x)
                    sentence_new,intent_new,slot_new = NLUModel.nluSentence(sentCuted)
                    print("intent_new",intent_new)

                    dialogueManager.informationFuse(dialogueManager.intentHold,slot_new,sentence_new)  # 将新旧信息融合
                    # strCode = dialogueManager.calState(intent,dialogueManager.slotStrHold)
                    dialogueManager.str2State(dialogueManager.intentHold,dialogueManager.slotStrHold) # 确定对话管理器状态
                    dialogueManager.buildSlotDict(dialogueManager.intentHold,slot_new,sentence_new)

                    print("ialogueManager.state==3",dialogueManager.state)
                    # 不一定产生问句啊，有可能是完成状态，就不需要产生问句了
                    if dialogueManager.state==3:
                        print("sentence_new333 ",sentence_new)
                        print("dialogueManager.slotStrHold333 ",dialogueManager.slotStrHold)
                        querySentence = dialogueManager.querySentence(dialogueManager.intentHold,dialogueManager.slotStrHold)  # 产生问句
                        print("querySentence333 ",querySentence)

                    print("---------多轮对话中(结束)---------------------------------")
        else:
            print("您的请求不在本系统支持范围内")
                
        
    else:
        print("请输入内容")
    # except:
    #     print("第 ",i," 句话出现错误")

main()