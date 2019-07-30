# coding:utf-8

# 定义一个对话管理类

class Manage(object):
    def __init__(self): # 初始化成员数据
        self.state = 0 # 0表示初始化状态，1表示开启多轮对话状态,2表示该语句是单轮语句，同时关闭多轮对话；3表示处于多轮对话中
        self.answerState = 0 # 0是初始状态；1是只需要产生文字回答；2是不止需要产生文本，还要产生图片,传给AnswerGenerator
        # self.sentenceHold = []
        self.intentHold = ""  # 用于记录多轮对话中上一轮的Intent
        self.slotStrHold = ""  # 用于记录多轮对话中上一轮的slot码10100
        self.slotDictHold = dict()   # 记录多轮对话的slot
    

    def setState(self,setNum):   # 用于改变对话状态
        self.state = setNum
        if self.state == 0:  # 设置为初始化，则将信息保存清空
            self.intentHold = ""
            self.slotStrHold = ""
    
    def calSlotCode(self,intent,slot):
        slotCode = 0  # 0表示不确定的状态
        if intent == "query_location":
            if "first_name" in slot:
                slotCode+=1
            if "teacher" in slot:
                slotCode+=2
            if "area" in slot:
                slotCode+=4
            if "room" in slot:
                slotCode+=8
            if "name" in slot:
                slotCode+=16

        elif intent == "query_student":
            if "student" in slot:
                slotCode+=1
            if "who" in slot:
                slotCode+=2
            if "name" in slot:
                slotCode+=4
        
        elif intent == "introduce":
            if "first_name" in slot:
                slotCode+=1
            if "teacher" in slot:
                slotCode+=2
            if "name" in slot:
                slotCode+=4
            if "org" in slot:
                slotCode+=8
        elif intent == "query_teacher":
            if "teacher" in slot:
                slotCode+=1
            if "first_name" in slot:
                slotCode+=2
            if "student" in slot:
                slotCode+=4
            if "p-prop" in slot:
                slotCode+=8
            if "name" in slot:
                slotCode+=16
        elif intent == "query_room":
            if "room" in slot:
                slotCode+=1
        
        elif intent == "query_activity":
            if "att" in slot:
                slotCode+=1
            if "a-prop" in slot:
                slotCode+=2
            if "activity" in slot:
                slotCode+=4
            if "name" in slot:
                slotCode+=8
        elif intent == "query_org":
            if "student" in slot:
                slotCode+=1
            if "teacher" in slot:
                slotCode+=2
            if "persion" in slot:
                slotCode+=4
            if "o-prop" in slot:
                slotCode+=8
            if "org" in slot:
                slotCode+=16





            


        return slotCode
    
    def code2str(self,slotCode,intent):  # 
        strCode = bin(slotCode)
        strCode = strCode[2:]
        addZero = ""
        if intent=="query_location" or intent=="query_teacher":
            numOfSlot = 5
        elif intent=="query_student" :
            numOfSlot = 3
        
        elif intent == "introduce":
            numOfSlot = 4
        
        elif intent == "query_room":
            numOfSlot = 1
        
        elif intent == "query_activity":
            numOfSlot = 4
        
        elif intent == "query_org":
            numOfSlot = 5
        
        if len(strCode)<numOfSlot:
            for i in range(numOfSlot-len(strCode)):
                addZero+="0"
            # print(addZero)
            strCode=addZero+strCode
        # print(strCode)
        return strCode

    def str2State(self,intent,strCode):  # 根据slot状态码得到对话管理器状态
        if intent == "query_location":
            print("str2State:",intent)
            print("str2state:",strCode)
            if strCode[0] == "1":
                self.state = 2
            elif strCode[1] == "1" and strCode[3]!="1" and strCode[4]!=1:
                self.state = 2
            else:
                if self.state == 3:# 处于多轮对话 
                    self.state = 3 # 依旧处于多轮对话中
                else:
                    self.state = 1 # 首次进入多轮对话
        elif intent == "query_student":
            if strCode=="111":
                self.state = 2
            else:
                if self.state == 3:# 处于多轮对话 
                    self.state = 3 # 依旧处于多轮对话中
                else:
                    self.state = 1 # 首次进入多轮对话
        elif intent == "introduce":
            if strCode[0]=="1" or strCode[1]=="1":
                self.state = 2
            else:
                if self.state == 3:# 处于多轮对话 
                    self.state = 3 # 依旧处于多轮对话中
                else:
                    self.state = 1 # 首次进入多轮对话

        elif intent == "query_teacher":
            if strCode[0] == "1" and (strCode[1]=="1" or strCode[2]=="1"):
                self.state = 2
            else:
                if self.state == 3:# 处于多轮对话 
                    self.state = 3 # 依旧处于多轮对话中
                else:
                    self.state = 1 # 首次进入多轮对话
        elif intent == "query_room":
            if strCode=="1":
                self.state = 2
            else:
                if self.state == 3:# 处于多轮对话 
                    self.state = 3 # 依旧处于多轮对话中
                else:
                    self.state = 1 # 首次进入多轮对话

        elif intent == "query_activity":
            if strCode=="1110" or strCode=="1111":
                self.state = 2
            
            else:
                if self.state == 3:# 处于多轮对话 
                    self.state = 3 # 依旧处于多轮对话中
                else:
                    self.state = 1 # 首次进入多轮对话
        
        elif intent == "query_org":
            if strCode[:2]=="11":
                self.state = 2
            
            else:
                if self.state == 3:# 处于多轮对话 
                    self.state = 3 # 依旧处于多轮对话中
                else:
                    self.state = 1 # 首次进入多轮对话








    def setPictureState(self,intent,slotCode): 
        if intent == "query_location":
            self.answerState = 2  # 告诉结果生成器需要画图
        else:
            self.answerState = 1
            
    
    def querySlot(self,intent,strCode):
        querySentence = ""
        if intent == "query_location":
            # print("啊啊啊啊")
            if strCode[0] == "0" and strCode[1] == "1" and strCode[3]=="1":
                querySentence = "请问您说的是哪个"+self.slotDictHold['teacher']
            elif strCode[0] == "0" and strCode[1] == "0":
                querySentence = "请问您要去哪"
            
            elif strCode[0] == "0" and strCode[1] == "1" and strCode[3]=="0":
                querySentence = "请问您要找的是谁"
 

        if intent == "introduce":
            if strCode[0] == "0" :
            
                querySentence = "请问您说的是谁？"
        if intent == "query_teacher":
            if strCode[0] == "0" :
                querySentence = "请问您说的是谁？"



        return querySentence
    
    def querySentence(self,intent,strCode):
        querySentence = ""
        if self.state==1:  # 信息不全，首次进入多轮对话
            # 记录当前信息
            self.intentHold = intent
            self.slotStrHold = strCode

            # 确定需要查询的槽是哪个
            querySentence = self.querySlot(intent,strCode)
            self.state = 3 # 处于多轮对话中

        elif self.state==3: # 信息不全，处于多轮对话中
            
            # 确定需要查询的槽是哪个
            # print("确定需要查询的槽是哪个")
            querySentence = self.querySlot(intent,strCode)

        
        return querySentence
    
    def strCodeFuse(self,code1,code2):  # 状态码融合
        code = ""
        # print("code1",code1)
        # print("code2",code2)
        assert len(code1)==len(code2)
        for i in range(len(code1)):
            if code1[i]=="1" or code2[i]=="1":
                code = code + "1"
            else:
                code = code + "0"
    
        return code
    
    def buildSlotDict(self,intent,slot,sentence):
        if intent=="query_location":
            if "name" in slot:
                self.slotDictHold["name"] = sentence[slot.index("name")]
            if "room" in slot:
                self.slotDictHold["room"] = sentence[slot.index("room")]
            if "area" in slot:
                self.slotDictHold["area"] = sentence[slot.index("area")]
            if "teacher" in slot:
                self.slotDictHold["teacher"] = sentence[slot.index("teacher")]
            if "first_name" in slot:
                self.slotDictHold["first_name"] = sentence[slot.index("first_name")]

        elif intent == "query_student":
            if "name" in slot:
                self.slotDictHold["name"] = sentence[slot.index("name")]
            if "who" in slot:
                self.slotDictHold["who"] = sentence[slot.index("who")]
            if "student" in slot:
                self.slotDictHold["student"] = sentence[slot.index("student")]
        
        elif intent == "introduce":
            if "name" in slot:
                self.slotDictHold["name"] = sentence[slot.index("name")]
            if "teacher" in slot:
                self.slotDictHold["teacher"] = sentence[slot.index("teacher")]
            if "student" in slot:
                self.slotDictHold["first_name"] = sentence[slot.index("first_name")]
        
        elif intent == "query_teacher":
            if "name" in slot:
                self.slotDictHold["name"] = sentence[slot.index("name")]
            if "p-prop" in slot:
                self.slotDictHold["p-prop"] = sentence[slot.index("p-prop")]
            if "student" in slot:
                self.slotDictHold["student"] = sentence[slot.index("student")]
            if "teacher" in slot:
                self.slotDictHold["teacher"] = sentence[slot.index("teacher")]
            if "first_name" in slot:
                self.slotDictHold["first_name"] = sentence[slot.index("first_name")]
        
        elif intent == "query_room":
            if "room" in slot:
                self.slotDictHold["room"] = sentence[slot.index("room")]

        elif intent == "query_activity":
            if "name" in slot:
                self.slotDictHold["name"] = sentence[slot.index("name")]
            
            if "a-prop" in slot:
                self.slotDictHold["a-prop"] = sentence[slot.index("a-prop")]
            
            if "activity" in slot:
                self.slotDictHold["activity"] = sentence[slot.index("activity")]
            
            if "att" in slot:
                self.slotDictHold["att"] = sentence[slot.index("att")]
        
        elif intent == "query_org":
            if "org" in slot:
                self.slotDictHold["org"] = sentence[slot.index("org")]
            
            if "o-prop" in slot:
                self.slotDictHold["o-prop"] = sentence[slot.index("o-prop")]
            
            if "persion" in slot:
                self.slotDictHold["persion"] = sentence[slot.index("persion")]
            
            if "teacher" in slot:
                self.slotDictHold["teacher"] = sentence[slot.index("teacher")]
            
            if "student" in slot:
                self.slotDictHold["student"] = sentence[slot.index("student")]
            


        
        


    def newSentence(self):  
        newSent = ""
        if self.intentHold == "query_location":
            if self.slotStrHold[0]=="1" and self.slotStrHold[3]=="1" and self.slotStrHold[1]=="1" and self.slotStrHold[2]!="1":
                newSent = newSent + self.slotDictHold['name']
                newSent = newSent + self.slotDictHold['teacher']
                newSent = newSent + self.slotDictHold['room']+"在哪里"
            
            if self.slotStrHold[0]=="1" and self.slotStrHold[3]=="1" and self.slotStrHold[1]=="1" and self.slotStrHold[2]=="1":
                newSent = newSent + self.slotDictHold['name']
                newSent = newSent + self.slotDictHold['teacher']
                newSent = newSent + self.slotDictHold['room']+"在哪"+self.slotDictHold['area']

            if self.slotStrHold[1]=="1" and self.slotStrHold[0]!="1":
                newSent = "我想去"+self.slotDictHold['room']+"怎么走"
            
        elif self.intentHold == "introduce":
            if self.slotStrHold[1]=="1":
                newSent = "介绍一下"+ self.slotDictHold['name']
            elif self.slotStrHold[0]=="1":
                newSent = "介绍一下机电工程学院"
        elif self.intentHold == "query_teacher":
            if self.slotStrHold[0]=="1" and self.slotStrHold[1]=="1" and self.slotStrHold[4]=="1":
                newSent = self.slotDictHold['name']+self.slotDictHold['teacher']+self.slotDictHold['p-prop']+"是什么"
            elif self.slotStrHold[0]=="1" and self.slotStrHold[1]=="1" and self.slotStrHold[4]=="0":
                newSent = self.slotDictHold['name']+"的"+self.slotDictHold['p-prop']+"是什么"
        
        elif self.intentHold == "query_student":
            if self.slotStrHold[0] == "1" and self.slotStrHold[2] =="1":
                newSent = self.slotDictHold['name']+"是谁的"+self.slotDictHold['student']
        elif self.intentHold == "query_room":
            if self.slotStrHold[0] == "1":
                newSent = self.slotDictHold['room']+"是谁的办公室"
        
        elif self.intentHold == "query_activity":
            if self.slotStrHold[0] == "1" and self.slotStrHold[1] =="1" and self.slotStrHold[2] =="1":
                newSent = self.slotDictHold['name']+'的'+self.slotDictHold['activity']+self.slotDictHold['a-prop']
        
        elif self.intentHold == "query_org":
            if self.slotStrHold == "11010":
                newSent = "机电工程学院有"+self.slotDictHold["o-prop"]+self.slotDictHold['teacher']

            elif self.slotStrHold == "11001":
                newSent = "机电工程学院有"+self.slotDictHold["o-prop"]+self.slotDictHold['student']
            
            elif self.slotStrHold == "11000":
                # print("222222")
                newSent = "机电工程学院"+self.slotDictHold["o-prop"]
            
            


        
        else:
            pass
        
        return newSent



    def informationFuse(self,intent,slot,sentence):  # 必须处于多轮对话中，将上轮对话和本轮对话进行信息融合
        
        slotCode = self.calSlotCode(intent,slot)
        strCode = self.code2str(slotCode,intent)  # 计算当前状态码10010
        print("self.slotStrHold1",self.slotStrHold)
        code = self.strCodeFuse(self.slotStrHold,strCode)  # 将之前与当前状态码进行融合
        
        
        self.slotStrHold = code
        print("self.slotStrHold2",code)
        self.buildSlotDict(intent,sentence,slot)  # 构建slot:具体值 词典，给知识交互器使用
        
        # 这个code形式为“10100”,如果code满足完成状态，就传给知识交互器，用于产生知识；若不满足，则继续询问
            
    
    def firstmanage(self,intent,slot,sentence):
        
        slotCode = self.calSlotCode(intent,slot)
        # slotCode是十进制数字
        # print("slotCode",slotCode)
        strCode = self.code2str(slotCode,intent)

        self.str2State(intent,strCode)  # 设置对话管理器状态
        
        
        self.intentHold = intent
        self.slotStrHold = strCode
        self.slotHold = slot
        self.buildSlotDict(intent,slot,sentence)  # 构建slot:具体值 词典，给知识交互器使用
        return strCode
        


# def test():
#     intent = "query_location"
#     slot = ["first_name","teacher","o","room","o","o"]
#     # slot = ["o","o","o","room","o","o"]
#     myManage = Manage()
#     myManage.manage(intent,slot)
#     print(myManage.slotStrHold)
#     print(myManage.state)
     

# test()