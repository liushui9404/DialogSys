#coding:utf-8

import re
from loadmodel import *
# input_sentence = ['SURNAME', '老师', '的', '办公室', '在', '哪', '一', '层', '?']
# result_slot = ['first_name', 'teacher1-2', 'o', 'office2-3-1', 'o', 'where', 'o', 'floor2-1', 'o']
# result_intent = "is_located_in&is_in_floor_of"

# input_sentence = ["SURNAME","老师","的" ,"研究生" ,"是", "谁," ,"?"]
# result_slot = ["first_name", "teacher1-2", "o", "postgraduate1-1-1", "o", "who", "o"]
# result_intent = "is_a_teacher_of&is_a"

# input_sentence = ["SURNAME", "老师" ,"的", "办公室","在", "哪","?"]
# result_slot = ["first_name", "teacher1-2", "o","office2-3-1","o","where","o"]
# result_intent = "is_located_in"

# input_sentence = ['SURNAME', '老师', '的', '办公室', '在', '哪', '一', '栋', '?']
# result_slot = ['first_name', 'teacher1-2', 'o', 'office2-3-1', 'o', 'where', 'o', 'block2-2', 'o']
# result_intent = "is_located_in&is_in_block_of"

# input_sentence = ['SURNAME', '老师', '的', '研究', '方向', '是','?']
# result_slot = ['first_name', 'teacher1-2', 'o', 'research', 'o', 'o', 'o']
# result_intent = "is_interested_in"

# input_sentence = ['SURNAME', '老师', '的', '系所', '是','?']
# result_slot = ['first_name', 'teacher1-2', 'o', 'department', 'o', 'o']
# result_intent = "work_in"

# input_sentence = ['本次', '会议', '的', '议题', '是','?']
# result_slot = ['o', 'meeting3-1', 'o', 'subject', 'o', 'o']
# result_intent = "has_a_topic_of"

# input_sentence = ['请问', '学校', '安全', '知识', '竞赛','在','哪里','举行','?']
# result_slot = ['o', 'o', 'att_b', 'att_e', 'match3-4', 'o','location','o','o']
# result_intent = "is_located_in"


# input_sentence = ['本次', '会议', '的', '地点', '是','?']
# result_slot = ['o', 'meeting3-1', 'o', 'location', 'o', 'o']
# result_intent = "is_located_in"

# input_sentence = ['请问', '华为', '公司', '笔试', '的','地点','是','?']
# result_slot = ['o', 'att_b', 'att_e', 'exam3-3-1', 'o','location', 'o','?']
# result_intent = "is_located_in"




def re_match(i_list,pattern):
    for i in range(len(i_list)):
        if re.match(pattern,i_list[i]):
            return i
        else:
            pass


def sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=""):
    rdf_list_1 = []
    rdf_list_2 = []
    predicate = result_intent
    for i in succ_list:
        
        if result_slot[i]=="first_name":
            rdf_list_1.append(input_sentence[i]+input_sentence[i+1])
            rdf_list_1.append(predicate)
            rdf_list_1.append("object1")
            
        if re.match(pattern,result_slot[i]):
            rdf_list_1.append(input_sentence[i])
            rdf_list_1.append(predicate)
            rdf_list_1.append("object1")
            if "att_b" in result_slot:
                index_b = 10000
                index_e = 10000
                for j in succ_list:
                    if result_slot[j]=="att_b":
                        index_b=j

                    if result_slot[j]=="att_e":
                        index_e=j

                att = input_sentence[index_b:index_e+1]
                att = "".join(att)
                rdf_list_2.append(input_sentence[i])
                rdf_list_2.append("has_attribute")
                rdf_list_2.append(att)

    print(rdf_list_1)
    if len(rdf_list_2)==3:
        print(rdf_list_2)
                        
def sub_rdf_2(succ_list,result_intent,input_sentence,result_slot):
    rdf_list_1 = []
    rdf_list_2 = []
    temp = result_intent.split('&')
    predicate_1 = temp[0]
    predicate_2 = temp[1]
    for i in succ_list:
        if result_slot[i]=="first_name":
            rdf_list_1.append(input_sentence[i]+input_sentence[i+1])
            rdf_list_1.append(predicate_1)
            rdf_list_1.append("object1")
        
            rdf_list_2.append("object1")
            rdf_list_2.append(predicate_2)
            rdf_list_2.append("object2")
    print(rdf_list_1,'\n',rdf_list_2)

def sub_rdf_3(succ_list,result_intent,input_sentence,result_slot,pattern):
    rdf_list_1 = []
    rdf_list_2 = []
    temp = result_intent.split('&')
    predicate_1 = temp[0]
    predicate_2 = temp[1]
    for i in succ_list:
        if result_slot[i]=="first_name":
            rdf_list_1.append(input_sentence[i]+input_sentence[i+1])
            rdf_list_1.append(predicate_1)
            rdf_list_1.append("object1")
        
            rdf_list_2.append("object1")
            rdf_list_2.append(predicate_2)
            index = re_match(result_slot,pattern)
            
            rdf_list_2.append(result_slot[index])
    print(rdf_list_1,'\n',rdf_list_2)
    


    

def re_process(result_slot,result_intent):  # 返回成功提取到的slot
    succ_list = []
    for i in range(len(result_slot)):
        if result_slot[i]!='o':
            succ_list.append(i)
    return succ_list






def generate_rdf(succ_list,input_sentence,result_slot,result_intent):
    
    if result_intent=="is_located_in&is_in_floor_of":
        sub_rdf_2(succ_list,result_intent,input_sentence,result_slot)

    elif result_intent=="is_a_teacher_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot)

    elif result_intent=="is_a_teacher_of&is_a":
        sub_rdf_3(succ_list,result_intent,input_sentence,result_slot,r'.*1-1')
    
    elif result_intent=="is_located_in":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="is_located_in&is_in_block_of":
        sub_rdf_2(succ_list,result_intent,input_sentence,result_slot)

    elif result_intent=="is_interested_in":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot)
    
    elif result_intent=="work_in":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot)
    
    elif result_intent=="is_named":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot)
    
    elif result_intent=="gender_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot)

    elif result_intent=="major_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot)

    elif result_intent=="title_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot)

    elif result_intent=="duty_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot)

    elif result_intent=="has_a_topic_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="is_in_charge_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')
    
    elif result_intent=="is_held_by":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="has_participants_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')
    
    elif result_intent=="time_b":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')
    
    elif result_intent=="time_e":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="time_length":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="has_host_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="has_speaker_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')
    
    elif result_intent=="has_guests_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="has_requirement_of":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')
    
    elif result_intent=="recruit_people_number":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="recruit_people_major":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')
    
    elif result_intent=="recruit_people_major":
        sub_rdf_1(succ_list,result_intent,input_sentence,result_slot,pattern=r'[a-z]*3')

    elif result_intent=="is_a_teacher_of&is_in_block_of":
        sub_rdf_3(succ_list,result_intent,input_sentence,result_slot,r'.*1-1')
     
if __name__ == '__main__':
    
    x1 = ["BOS SURNAME 老师 的 办公室 在 哪 一 层 ? EOS"]
    input_sentence,result_slot,result_intent = load_model(x1)
    succ_list = re_process(result_slot,result_intent)
    generate_rdf(succ_list,input_sentence,result_slot,result_intent)



