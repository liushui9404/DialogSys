# coding:utf-8
from NLURNN import NLURNN
from NLURule import NLURule

class NLU(object):
    def __init__(self):
        # 初始化
        self.NLUModel1 = NLURNN()
        self.NLUModel2 = NLURule()

    def fuse(self,slot1,slot2,catchFlag):
        # print("slot1",slot1)
        # print("slot2",slot2)
        # print("catchFlag",catchFlag)
        length = len(catchFlag)
        for i in range(length):
            if catchFlag[i]==0:
                slot2[i] = slot1[i]
        # print("slot",slot2)
        return slot2

    def nluSentence(self,x1):
        sentList1,slot1,intent1 = self.NLUModel1.solve(x1)
        sentList2,slot2,intent2 = self.NLUModel2.sent2IntentSlot(x1)
        print("intnt1",intent1)
        print("intent2",intent2)
        # slot = self.fuse(slot1,slot2,self.NLUModel2.catchFlag)
        slot = slot2
        print("slot22222",slot)
        
        self.NLUModel2.catchFlag = []  # 复位

        intent = intent2
        sentList = sentList2

        return sentList,intent,slot

# def test():
#     x1 = ["BOS 王 老师 的 办公室 在 哪 一 层"]
#     NLUModel = NLU()
#     sentList,intent,slot = NLUModel.nluSentence(x1)
#     print("sentence",sentList)
#     print("slot",slot)
#     print("intent",intent)

# test()