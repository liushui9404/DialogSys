# -*- coding: utf-8 -*-

# import cut
# import sys
# sys.path.append('/home/liu/01对话系统文字部分/RNN/skip_posRNN')
# sys.path.append('/home/liu/01对话系统文字部分/rdftest')
# import loadmodel


import rdflib
import re
from rdflib import Namespace,RDF,RDFS
import pickle



g1 = rdflib.Graph()
g1.parse("../../../01对话系统文字部分/rdftest/CMEE_2.owl", format="xml")  # 解析文件
# g1.parse("./rdftest/CMEE_2.owl", format="xml")  # 解析文件
ns = Namespace('http://www.semanticweb.org/liu/O-CMEE#')  # 命名空间

# 推理机,针对rdfs:subClassOf，向下推理，三级推理
def inference_machine(need_query_str):  
    s_1 = []
    for s in g1.subjects(RDFS.subClassOf,ns[need_query_str]):
        s_1.append(s.split('#')[1])

    s_2 = []
    if s_1!=[]:
        for ss in s_1:
            for s in g1.subjects(RDFS.subClassOf,ns[ss]):
                s_2.append(s.split('#')[1])
    s_3 = []
    if s_2 !=[]:
        for ss in s_2:
            for s in g1.subjects(RDFS.subClassOf,ns[ss]):
                s_3.append(s.split('#')[1])
    s_1.extend(s_2)
    s_1.extend(s_3)
    if s_1==[]:
        # 说明该类下面没有子类
        s_1=[need_query_str]
        # print(s_1)
    return s_1



# inference_machine('教授')

def intent_slot_2_string(input_sentence,input_intent,input_slot):
    sentence_str = ' '.join(input_sentence)
    intent_str = input_intent
    slot_str = ' '.join(input_slot)
    return sentence_str,intent_str,slot_str

# a,b,c = intent_slot_2_string(input_sentence,input_intent,input_slot)
# print(a,b,c)
# 返回值可以再加上标识符,表示状态
def classification_by_intent_slot(input_sentence,intent_str,slot_str,input_slot):

    if intent_str=='query_location':
        if re.match('first_name teacher',slot_str):  #匹配模式：王老师的办公室在哪
            state = 21
            # print('hahha')
            ans_1 = []
            for s in g1.subjects(ns['firstname_is'],ns[input_sentence[0]]):  # 这里索引0表示姓氏
                ans_1.append(s)
            # print("ans_1",ans_1)
            ans_2 = []
            for ss in inference_machine(input_sentence[1]):
                # print("ss",ss)
                for s in g1.subjects(RDF.type,ns[ss]):
                    ans_2.append(s)
            # print('ans_2',ans_2)

            ans_3 = list(set(ans_1).intersection(set(ans_2)))  # 表示既姓王，又是老师
            # 产生答案
            ans_4 = []
            for res in ans_3:
                for s in g1.objects(res,ns['is_located_in']):
                    ans_4.append(str(s).split('#')[-1])

            # print("slot_str",slot_str)
            if re.search('area',slot_str):
                # print('1111111111')
                if '层' in input_sentence:
                    for i in range(len(ans_4)):
                        ans_4[i] = ans_4[i][1]

                elif '栋' in input_sentence:
                    for i in range(len(ans_4)):
                        ans_4[i] = ans_4[i][0]

            return ans_4,state
        

        elif re.search('activity.*where',slot_str):  # 询问活动的地点
            state = 0
            ans_1 = []
            index_of_activity = input_slot.index('activity')
            types = inference_machine(input_sentence[index_of_activity])
            for t in types:
                for s in g1.subjects(RDF.type,ns[t]):
                    ans_1.append(s)

            ans_2 = []
            for ss in ans_1:
                for s in g1.objects(ss,ns['is_located_in']):
                    ans_2.append(str(s).split('#')[-1])
            return ans_2,state

        elif re.search('name teacher',slot_str):
            state = 0
            ans_1 = []
            index_of_name = input_slot.index('name')
            name = input_sentence[index_of_name]
            for s in g1.objects(ns[name],ns['is_located_in']):
                ans_1.append(str(s).split('#')[-1])
            
            
            if '层' in input_sentence:
                for i in range(len(ans_1)):
                    ans_1[i] = ans_1[i][1]

            elif '栋' in input_sentence:
                for i in range(len(ans_1)):
                    ans_1[i] = ans_1[i][0]
            
            return ans_1,state

        elif re.search('name.*where',slot_str):  # 匹配模式：王恒升的办公室在哪,哪层，哪栋
            state = 0
            ans_1 = []
            index_of_name = input_slot.index('name')
            name = input_sentence[index_of_name]
            for s in g1.objects(ns[name],ns['is_located_in']):
                ans_1.append(str(s).split('#')[-1])
            
            
            if '层' in input_sentence:
                for i in range(len(ans_1)):
                    ans_1[i] = ans_1[i][1]

            elif '栋' in input_sentence:
                for i in range(len(ans_1)):
                    ans_1[i] = ans_1[i][0]
            
            return ans_1,state


    elif intent_str=="query_student":  # 询问学生
        if re.search('first_name teacher.*student.*[(list)(who)]',slot_str):
            pass
            state = 21
        elif re.search('name.*who.*student',slot_str):
            state = 0
            ans_1 = []
            index_of_name = input_slot.index('name')
            name = input_sentence[index_of_name]
            for s in g1.objects(ns[name],ns['is_a_student_of']):
                ans_1.append(str(s).split('#')[-1])
            
            return ans_1,state



    elif intent_str=="query_activity": # 询问活动
        if re.search('activity.*a-prop',slot_str):
            state = 0
            index_of_activity = input_slot.index('activity')
            ans_1 = []
            types = inference_machine(input_sentence[index_of_activity])
            for t in types:
                for s in g1.subjects(RDF.type,ns[t]):
                    ans_1.append(s)
            ans_2 = []
            index_of_a_prop = input_slot.index('a-prop')
            a_prop = input_sentence[index_of_a_prop]
            if a_prop=='负责人':
                prop = 'host_is'
            elif a_prop=='时长':
                prop = 'len_of_time'

            for ss in ans_1:
                for s in g1.objects(ss,ns[prop]):
                    ans_2.append(s)
            return ans_2,state


    elif intent_str=="introduce":  # 介绍
        if re.search(' name teacher',slot_str):  # 介绍老师，介绍一下王恒升老师
            state = 0
            index_of_name = input_slot.index('name')
            name = input_sentence[index_of_name]
            ans_dict = dict()
            for p,o in g1.predicate_objects(ns[name]):
                k = p.split('#')[-1]
                v = o.split('#')[-1]
                ans_dict[k] = v
            return ans_dict,state
        elif re.search(' name',slot_str):  #介绍人，介绍一下王恒升
            state = 0
            index_of_name = input_slot.index('name')
            name = input_sentence[index_of_name]
            ans_dict = dict()
            for p,o in g1.predicate_objects(ns[name]):
                k = p.split('#')[-1]
                v = o.split('#')[-1]
                ans_dict[k] = v
            return ans_dict,state

	        	

        elif re.search('first_name teacher',slot_str):
            state = 21
            index_of_fn = input_slot.index('first_name')
            index_of_teacher = input_slot.index('teacher')
            types = inference_machine(input_sentence[index_of_teacher])
            fn = input_sentence[index_of_fn]
            ans_dict = dict()
            ans_1 = []
            for s in g1.subjects(ns['firstname_is'],ns[fn]):
                ans_1.append(s.split('#')[-1])
            ans_2 = []
            for t in types:
                for s in g1.subjects(RDF.type,ns[t]):
                    ans_2.append(s.split('#')[-1])

            ans_3  = list(set(ans_1).intersection(set(ans_2)))

            for ss in ans_3:
                for p,o in g1.predicate_objects(ns[ss]):
                    k = p.split('#')[-1]
                    v = o.split('#')[-1]
                    ans_dict[k] = v
                          


            for p,o in g1.predicate_objects(ns[fn]):
                k = p.split('#')[-1]
                v = o.split('#')[-1]
                ans_dict[k] = v
            

        return ans_dict,state


    elif intent_str=="confirm":  # 确认
    
        if re.search("room o room",slot_str):
            state = 0
            index_of_room_1 = input_slot.index('room')
            room_1 = input_sentence[index_of_room_1]
            room_2 = input_sentence[index_of_room_1+2]

            ans_1 = []
            for s in g1.predicates(ns[room_1],ns[room_2]):
                ans_1.append(s)
            if len(ans_1)>0:
                return True
            else:
                return False


    elif intent_str=="query_org": # 询问组织
        if re.search("org.*",slot_str):
            pass


    elif intent_str=="query_teacher":
        if re.search('first_name teacher.*p-prop',slot_str):
            state = 21
            ans_1 = []
            index_of_teacher = input_slot.index('teacher')
            types = inference_machine(input_sentence[index_of_teacher])
            for t in types:
                for s in g1.subjects(RDF.type,ns[t]):
                    ans_1.append(s)

            index_of_fn = input_slot.index('first_name')
            ans_2 = []
            for s in g1.subjects(ns['firstname_is'],ns[input_sentence[index_of_fn]]):
                ans_2.append(s)

            ans_3 = list(set(ans_1).intersection(set(ans_2)))

            ans_4 = []  # 求属性
            index_of_p_prop = input_slot.index('p-prop')
            p_prop = input_sentence[index_of_p_prop]
            if p_prop=='性别':
                p = 'gender'
            elif p_prop=='研究':
                p = 'research'

            for t in ans_3:
                for s in g1.objects(t,ns[p]):
                    ans_4.append(s.split('#')[-1])
            # print('ans4',ans_4)
            return ans_4,state

        elif re.search('name teacher.*p-prop',slot_str):
            state = 0
            ans_1 = []
            index_of_name = input_slot.index('name')
            name = input_sentence[index_of_name]

            index_of_p_prop = input_slot.index('p-prop')
            p_prop = input_sentence[index_of_p_prop]
            if p_prop=='性别' or ('性别' in input_sentence) :
                p = 'gender'
            elif p_prop=='研究':
                p = 'research'
            elif p_prop=='系':
                p = 'work_in'
            

            for s in g1.objects(ns[name],ns[p]):
                ans_1.append(str(s).split('#')[-1])
            return ans_1,state

        elif re.search('first_name teacher.*student.*[(list)(who)]',slot_str):
            state = 21

            index_of_fn = input_slot.index('first_name')
            index_of_teacher = input_slot.index('teacher')

            ans_1 = []
            for s in g1.subjects(ns['firstname_is'],ns[input_sentence[index_of_fn]]):
                ans_1.append(s)

            ans_2 = []
            types = inference_machine(input_sentence[index_of_teacher])
            for t in types:
                for s in g1.subjects(RDF.type,ns[t]):
                    ans_2.append(s)

            ans_3 = list(set(ans_1).intersection(set(ans_2)))  # 表示既姓王，又是老师

            ans_4 = []
            for ss in ans_3:
                for s in g1.objects(ss,ns['has_students']):
                    ans_4.append(s)
            index_of_stu = input_slot.index('student')

            ans_5 = []
            for s in g1.subjects(RDF.type,ns[input_sentence[index_of_stu]]):
                ans_5.append(s)

            ans_6 = list(set(ans_4).intersection(set(ans_5)))

            ans_6 = [s.split('#')[-1] for s in ans_6]

            return ans_6,state




        # elif re.match(['first_name teacher o room o where area']):
    elif intent_str=="query_room":  # A520是谁的办公室？
        if re.search('room o.*o room',slot_str):
            state=0
            ans_1 = []
            for s in g1.subjects(ns['is_located_in'],ns[input_sentence[0]]):  # 这里索引0表示姓氏
                ans_1.append(s)
            ans_2 = []
            for s in ans_1:
                s = str(s)
                # print("这里",s.split("#"))
                ans = s.split("#")[-1]
                ans_2.append(ans)
            return ans_2,state


# input_sentence = ['王', '教授', '的', '办公室', '在', '哪个', '房间']
# input_intent = 'query_location'
# input_slot = ['first_name', 'teacher', 'o', 'room', 'o', 'where', 'area']

# input_sentence = ['王', '老师', '在', '哪', '层', '办公']
# input_intent = 'query_location'
# input_slot = ['first_name', 'teacher', 'o', 'where', 'o', 'location']


def input_x(x):

    processed_x = cut.cut_sentence(x)
    # print("processed_x",processed_x)
    sentence,slot,intent = loadmodel.load_model(processed_x)
    print('sentence',sentence)
    print('intent',intent)
    print('slot',slot)
    return sentence,slot,intent

# x = '请问今天比赛在哪里举办'
# x = '王老师的学生有哪些'
# x = '本次讲座的负责人是谁'
# x = '帮我介绍一下王恒升导师'
# x = 'A302是办公室吗'
# x = '机电工程学院一共有多少老师'
# x = '王老师的性别是'


def read_sent(path):
    f_r = open(path,'r')
    sents = f_r.readlines()
    sents_list = []
    for sen in sents:
        s = sen.split()
        ss = ''.join(s)
        sents_list.append(ss)
    return sents_list



def main_test():
    f_w = open('./测试结果','w')
    sents_list = read_sent('./测试语句')
    for index,sent in enumerate(sents_list):

        sentence,slot,intent = input_x(sent)
        input_sentence = sentence
        input_intent = intent
        input_slot = slot
        
        sentence_str,intent_str,slot_str = intent_slot_2_string(input_sentence,input_intent,input_slot)
        a = classification_by_intent_slot(input_sentence,intent_str,slot_str,input_slot)
        f_w.write(str(a))
        f_w.write('\n')
        print("index = ",index+1)
        print("答案是：",a)
        print('\n\n')

# main_test()
# 加载所以的老师名字List
def load_teachername_list(path):
    f = open(path,'rb')
    teachername_list = pickle.load(f)
    f.close() 
    return teachername_list

def correct(input_sentence,input_slot,teachername_list):
    for index ,sent in enumerate(input_sentence):
        if sent in teachername_list:
            input_slot[index] = "name"
    return input_sentence,input_slot






def information_to_answer(input_sentence,input_intent,input_slot):
    # 在这里首先进行一步处理，将
    teachername_list = load_teachername_list("/home/liu/00毕业课题/developing/01对话系统文字部分/rdftest/teacher_name_list")
    input_sentence,input_slot = correct(input_sentence,input_slot,teachername_list)

    sentence_str,intent_str,slot_str = intent_slot_2_string(input_sentence,input_intent,input_slot)
    
    ans,state = classification_by_intent_slot(input_sentence,intent_str,slot_str,input_slot)
    # print("111111111111111")
    return ans,state
    
    