# coding:utf-8

# import cut
# import sys
# sys.path.append('/home/liu/01对话系统文字部分/RNN/skip_posRNN')
# sys.path.append('/home/liu/01对话系统文字部分/rdftest')
# import loadmodel


import rdflib
import re
from rdflib import Namespace,RDF,RDFS
import pickle


class InteractWithKB(object):
    def __init__(self):

        self.g1 = rdflib.Graph()
        self.g1.parse("/home/liu/00毕业课题/developing/01对话系统文字部分/rdftest/CMEE_2.owl", format="xml")  # 解析文件
        # self.g1.parse("../../../01对话系统文字部分/rdftest/CMEE_2.owl", format="xml")  # 解析文件
        # self.g1.parse("./rdftest/CMEE_2.owl", format="xml")  # 解析文件
        self.ns = Namespace('http://www.semanticweb.org/liu/O-CMEE#')  # 命名空间
        self.interactState = 0  # 0表示初始化交互状态，1表示没有成功返回答案，2表示成功返回答案
    
    # 加载所有的老师名字List
    def load_teachername_list(self,path):
        f = open(path,'rb')
        teachername_list = pickle.load(f)
        f.close() 
        return teachername_list

    def correct(self,input_sentence,input_slot,teachername_list):
        for index ,sent in enumerate(input_sentence):
            if sent in teachername_list:
                input_slot[index] = "name"
        return input_sentence,input_slot

        # inference_machine('教授')
    def intent_slot_2_string(self,input_sentence,input_intent):
        sentence_str = ' '.join(input_sentence)
        intent_str = input_intent
        # slot_str = ' '.join(input_slot)
        return sentence_str,intent_str
    


    # 推理机,针对rdfs:subClassOf，向下推理，三级推理
    def inference_machine(self,need_query_str):  
        s_1 = []
        for s in self.g1.subjects(RDFS.subClassOf,self.ns[need_query_str]):
            s_1.append(s.split('#')[1])

        s_2 = []
        if s_1!=[]:
            for ss in s_1:
                for s in self.g1.subjects(RDFS.subClassOf,self.ns[ss]):
                    s_2.append(s.split('#')[1])
        s_3 = []
        if s_2 !=[]:
            for ss in s_2:
                for s in self.g1.subjects(RDFS.subClassOf,self.ns[ss]):
                    s_3.append(s.split('#')[1])
        s_1.extend(s_2)
        s_1.extend(s_3)
        if s_1==[]:
            # 说明该类下面没有子类
            s_1=[need_query_str]
            # print(s_1)
        return s_1


    
    def classification_by_intent_slot(self,input_sentence,intent_str,slotCode,slotDict):
        # slotCode形式 ：“11011”
        
        if intent_str=='query_location':
            
            if re.match('0.*11',slotCode):  #匹配模式：王老师的办公室在哪
                
                ans_1 = []
                for s in self.g1.subjects(self.ns['firstname_is'],self.ns[input_sentence[0]]):  # 这里索引0表示姓氏
                    ans_1.append(s)
                # print("ans_1",ans_1)
                ans_2 = []
                for ss in self.inference_machine(input_sentence[1]):
                    # print("ss",ss)
                    for s in self.g1.subjects(RDF.type,self.ns[ss]):
                        ans_2.append(s)
                # print('ans_2',ans_2)

                ans_3 = list(set(ans_1).intersection(set(ans_2)))  # 表示既姓王，又是老师
                # 产生答案
                ans_4 = []
                for res in ans_3:
                    for s in self.g1.objects(res,self.ns['is_located_in']):
                        ans_4.append(str(s).split('#')[-1])

                # print("slotCode",slotCode)
                if re.search('area',slotCode):
                    # print('1111111111')
                    if '层' in input_sentence:
                        for i in range(len(ans_4)):
                            ans_4[i] = ans_4[i][1]

                    elif '栋' in input_sentence:
                        for i in range(len(ans_4)):
                            ans_4[i] = ans_4[i][0]
                
                if ans_4==[]:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案

                return ans_4
            

            elif re.search('activity.*where',slotCode):  # 询问活动的地点
                
                ans_1 = []
                # index_of_activity = input_slot.index('activity')
                # types = self.inference_machine(input_sentence[index_of_activity])
                types = self.inference_machine(slotDict['activity'])
                for t in types:
                    for s in self.g1.subjects(RDF.type,self.ns[t]):
                        ans_1.append(s)

                ans_2 = []
                for ss in ans_1:
                    for s in self.g1.objects(ss,self.ns['is_located_in']):
                        ans_2.append(str(s).split('#')[-1])
                
                if ans_2==[]:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案

                return ans_2

            elif re.search("1.{2}10",slotCode):  # 匹配张xx老师办公室在哪
                # print("是这里吗")
                
                ans_1 = []
                # index_of_name = input_slot.index('name')
                # name = input_sentence[index_of_name]
                name = slotDict["name"]
                for s in self.g1.objects(self.ns[name],self.ns['is_located_in']):
                    ans_1.append(str(s).split('#')[-1])
                
                if '层' in input_sentence:
                    for i in range(len(ans_1)):
                        ans_1[i] = ans_1[i][1]

                elif '栋' in input_sentence:
                    for i in range(len(ans_1)):
                        ans_1[i] = ans_1[i][0]
                
                if ans_1==[]:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案
                
                return ans_1

            elif re.search("01000",slotCode):  # 匹配我想去A513
                # print("是这里吗")
                
                ans_1 = []
                # index_of_name = input_slot.index('name')
                # name = input_sentence[index_of_name]
                room = slotDict["room"]
                ans_1.append(room)

                
                
                return ans_1

            elif re.search('11.{3}',slotCode):  # 匹配模式：王恒升的办公室在哪,哪层，哪栋
                
                ans_1 = []
                # index_of_name = input_slot.index('name')
                # name = input_sentence[index_of_name]
                print("slotDict",slotDict)
                name = slotDict['name']
                for s in self.g1.objects(self.ns[name],self.ns['is_located_in']):
                    ans_1.append(str(s).split('#')[-1])
                
                
                if '层' in input_sentence:
                    for i in range(len(ans_1)):
                        ans_1[i] = ans_1[i][1]

                elif '栋' in input_sentence:
                    for i in range(len(ans_1)):
                        ans_1[i] = ans_1[i][0]
                
                if ans_1==[]:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案
                
                return ans_1


        elif intent_str=="query_student":  # 询问学生
                            
            if re.search('111',slotCode):
                
                ans_1 = []
                # index_of_name = input_slot.index('name')
                # name = input_sentence[index_of_name]
                print("slotDict",slotDict)
                name = slotDict['name']
                for s in self.g1.objects(self.ns[name],self.ns['is_a_student_of']):
                    ans_1.append(str(s).split('#')[-1])
                
                if ans_1==[]:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案

                return ans_1



        elif intent_str=="query_activity": # 询问活动
            if re.search('111*',slotCode):
                ans_1 = []
                # index_of_activity = input_slot.index('activity')
                # types = self.inference_machine(input_sentence[index_of_activity])
                # types = self.inference_machine(slotDict['activity'])
                name = slotDict['name']
                activity = slotDict['activity']
                nameOfActivity = name+activity
                a_prop = slotDict['a-prop']

                if a_prop=='主讲人':
                    prop = 'speaker_is'
                elif a_prop=='时长':
                    prop = 'len_of_time'
                elif a_prop == "开始时间":
                    prop = 'b_time'
                elif a_prop == "结束时间":
                    prop = 'e_time'
                elif a_prop =="主题":
                    prop = 'theme_is'
                elif a_prop == "哪里":
                    prop = 'is_located_in'
                    
            
            for s in self.g1.objects(self.ns[nameOfActivity],self.ns[prop]):
                ans_1.append(s)
            # ans_2 = []
            #     # index_of_a_prop = input_slot.index('a-prop')
            #     # a_prop = input_sentence[index_of_a_prop]
                
                

            #     for ss in ans_1:
            #         for s in self.g1.objects(ss,self.ns[prop]):
            #             ans_2.append(s)

            if ans_1==[]:
                self.interactState = 1  # 没有成功返回答案
            else:
                self.interactState = 2 # 成功返回答案

            return ans_1


        elif intent_str=="introduce":  # 介绍
            if re.search('01.{2}',slotCode):  # 介绍人物，介绍一下王恒升老师
                
                # index_of_name = input_slot.index('name')
                # name = input_sentence[index_of_name]
                name = slotDict['name']
                ans_dict = dict()
                for p,o in self.g1.predicate_objects(self.ns[name]):
                    k = p.split('#')[-1]
                    v = o.split('#')[-1]
                    ans_dict[k] = v

                if len(ans_dict)==0:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案 
                # print("ans_dict",ans_dict)

                return ans_dict
            
            elif re.search('1000',slotCode):  # 介绍组织
                
                # index_of_name = input_slot.index('name')
                # name = input_sentence[index_of_name]
                org = "机电工程学院"
                ans_dict = dict()
                for p,o in self.g1.predicate_objects(self.ns[org]):
                    k = p.split('#')[-1]
                    v = o.split('#')[-1]
                    ans_dict[k] = v

                if len(ans_dict)==0:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案 
                
                return ans_dict

           


        elif intent_str=="query_org": # 询问组织
            if re.search("11*",slotCode):
            
                ans_1 = []
                # index_of_activity = input_slot.index('activity')
                # types = self.inference_machine(input_sentence[index_of_activity])
                # types = self.inference_machine(slotDict['activity'])
                org = "机电工程学院"
                o_prop = slotDict['o-prop']

                if o_prop=="多少":
                    if "teacher" in slotDict:
                        prop = "num_of_teacher"
                    elif "student" in slotDict:
                        prop = "num_of_stu"
                elif o_prop=="历史":
                    prop = "history"

                
                for s in self.g1.objects(self.ns[org],self.ns[prop]):
                    ans_1.append(s)
                        
                print("这里!!!")
                if ans_1==[]:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案

                return ans_1
                


        elif intent_str=="query_teacher":
            # if re.search('01011',slotCode):
                
            #     ans_1 = []
            #     # index_of_teacher = input_slot.index('teacher')
            #     # types = self.inference_machine(input_sentence[index_of_teacher])
            #     types = self.inference_machine(slotDict['teacher'])
            #     for t in types:
            #         for s in self.g1.subjects(RDF.type,self.ns[t]):
            #             ans_1.append(s)

            #     # index_of_fn = input_slot.index('first_name')
            #     fn = slotDict['first_name']
            #     ans_2 = []
            #     for s in self.g1.subjects(self.ns['firstname_is'],self.ns[fn]):
            #         ans_2.append(s)

            #     ans_3 = list(set(ans_1).intersection(set(ans_2)))

            #     ans_4 = []  # 求属性
            #     # index_of_p_prop = input_slot.index('p-prop')
            #     # p_prop = input_sentence[index_of_p_prop]
            #     p_prop = slotDict['p-prop']
            #     if p_prop=='性别':
            #         p = 'gender'
            #     elif p_prop=='研究':
            #         p = 'research'

            #     for t in ans_3:
            #         for s in self.g1.objects(t,self.ns[p]):
            #             ans_4.append(s.split('#')[-1])
            #     # print('ans4',ans_4)
            #     if ans_4==[]:
            #         self.interactState = 1  # 没有成功返回答案
            #     else:
            #         self.interactState = 2 # 成功返回答案
                
            #     return ans_4

            if re.search('110.*',slotCode):
                ans_1 = []
                # index_of_name = input_slot.index('name')
                # name = input_sentence[index_of_name]

                name = slotDict['name']
                

                # index_of_p_prop = input_slot.index('p-prop')
                # p_prop = input_sentence[index_of_p_prop]
                p_prop = slotDict['p-prop']
                if p_prop=='性别' or ('性别' in input_sentence) :
                    p = 'gender'
                elif p_prop=='研究':
                    
                    p = 'research'
                elif p_prop=='系':
                    p = 'work_in'

                if p_prop=="职称":
                    for s in self.g1.objects(self.ns[name],RDF.type):
                        ans_1.append(str(s).split('#')[-1])
                

                else:
                    
                    for s in self.g1.objects(self.ns[name],self.ns[p]):
                        ans_1.append(str(s).split('#')[-1])
                    print("这里!!!",ans_1)
                
                if ans_1 == []:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    if len(ans_1)!=2:
                        pass
                    else:
                        ans_1.remove("NamedIndividual")
                    self.interactState = 2 # 成功返回答案

                return ans_1

            elif re.search('1010.',slotCode):
                

                # index_of_fn = input_slot.index('first_name')
                # index_of_teacher = input_slot.index('teacher')

                # fn = slotDict['first_name']
                # teacher = slotDict['teacher']
                name = slotDict['name']

                # ans_1 = []
                # for s in self.g1.subjects(self.ns['firstname_is'],self.ns[fn]):
                #     ans_1.append(s)

                # ans_2 = []
                # types = self.inference_machine(teacher)
                # for t in types:
                #     for s in self.g1.subjects(RDF.type,self.ns[t]):
                #         ans_2.append(s)

                # ans_3 = list(set(ans_1).intersection(set(ans_2)))  # 表示既姓王，又是老师
                # ans_3 = 
                ans_4 = []
                # for ss in ans_3:
                for s in self.g1.objects(self.ns[name],self.ns['has_students']):
                    ans_4.append(s)

                # index_of_stu = input_slot.index('student')
                student = slotDict['student']
                ans_5 = []
                for s in self.g1.subjects(RDF.type,self.ns[student]):
                    ans_5.append(s)

                ans_6 = list(set(ans_4).intersection(set(ans_5)))

                ans_6 = [s.split('#')[-1] for s in ans_6]

                if ans_6==[]:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案

                return ans_6
            # elif re.match(['first_name teacher o room o where area']):
        elif intent_str=="query_room":  # A520是谁的办公室？
            if re.search('1',slotCode):
                print("这里",input_sentence[0])
                

                ans_1 = []
                for s in self.g1.subjects(self.ns['is_located_in'],self.ns[input_sentence[0]]):
                    ans_1.append(s)
                ans_2 = []
                for s in ans_1:
                    s = str(s)
                    # print("这里",s.split("#"))
                    ans = s.split("#")[-1]
                    ans_2.append(ans)

                if ans_2==[]:
                    self.interactState = 1  # 没有成功返回答案
                else:
                    self.interactState = 2 # 成功返回答案

                return ans_2


    def information_to_answer(self,input_sentence,input_intent,slotCode,slotDict):
        teachername_list = self.load_teachername_list("/home/liu/00毕业课题/developing/01对话系统文字部分/rdftest/teacher_name_list")
        # input_sentence,input_slot = self.correct(input_sentence,input_slot,teachername_list)
        sentence_str,intent_str = self.intent_slot_2_string(input_sentence,input_intent)
        ans = self.classification_by_intent_slot(input_sentence,intent_str,slotCode,slotDict)
        # print("111111111111111")
        return ans


#------------------------------------------------测试用--------------------------------------------
# a,b,c = intent_slot_2_string(input_sentence,input_intent,input_slot)
# print(a,b,c)
# 返回值可以再加上标识符,表示状态


# input_sentence = ['王', '教授', '的', '办公室', '在', '哪个', '房间']
# input_intent = 'query_location'
# input_slot = ['first_name', 'teacher', 'o', 'room', 'o', 'where', 'area']

# input_sentence = ['王', '老师', '在', '哪', '层', '办公']
# input_intent = 'query_location'
# input_slot = ['first_name', 'teacher', 'o', 'where', 'o', 'location']


# def input_x(x):
    
#     processed_x = cut.cut_sentence(x)
#     # print("processed_x",processed_x)
#     sentence,slot,intent = loadmodel.load_model(processed_x)
#     print('sentence',sentence)
#     print('intent',intent)
#     print('slot',slot)
#     return sentence,slot,intent

# # x = '请问今天比赛在哪里举办'
# # x = '王老师的学生有哪些'
# # x = '本次讲座的负责人是谁'
# # x = '帮我介绍一下王恒升导师'
# # x = 'A302是办公室吗'
# # x = '机电工程学院一共有多少老师'
# # x = '王老师的性别是'


# def read_sent(path):
#     f_r = open(path,'r')
#     sents = f_r.readlines()
#     sents_list = []
#     for sen in sents:
#         s = sen.split()
#         ss = ''.join(s)
#         sents_list.append(ss)
#     return sents_list



# def main_test():
#     f_w = open('./测试结果','w')
#     sents_list = read_sent('./测试语句')
#     for index,sent in enumerate(sents_list):

#         sentence,slot,intent = input_x(sent)
#         input_sentence = sentence
#         input_intent = intent
#         input_slot = slot
        
#         sentence_str,intent_str,slot_str = intent_slot_2_string(input_sentence,input_intent,input_slot)
#         a = classification_by_intent_slot(input_sentence,intent_str,slot_str,input_slot)
#         f_w.write(str(a))
#         f_w.write('\n')
#         print("index = ",index+1)
#         print("答案是：",a)
#         print('\n\n')

# main_test()