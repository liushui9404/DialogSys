#coding:utf-8
import pickle
import numpy as np 

def read_data(data_path):
    f_input  = open(data_path,'r')
    data = f_input.readlines()
    sen_list = []
    intent_list = []
    max_len = 1
    for sentence in data:
        part = sentence.split('\t')
        sen = part[0].strip(' BOSEOS').split()

        len_sen = len(sen) # 求字的个数
        
        if len_sen>max_len:
            max_len = len_sen
        intent = part[1].split()[-1]
        sen_list.append(sen)
        intent_list.append(intent)
    f_input.close()
    # print(sen_list,intent_list)
    
    return sen_list,intent_list
    

def str2vec(sen_list,intent_list,max_len,embedding_size):
    # 将字符变为向量
    # 现将词变为数字
    input_f = open('/home/liu/新论文/classify_W/skip-gram-nopos/wordembeddings','rb') # 打开之前训练词向量的词典，词->数字
    word2vec= pickle.load(input_f)
    input_f.close()

    embed_list = []
    data_list = []

    padding_random = np.random.rand(embedding_size)
    padding_0 = [0]*embedding_size

    for sentence in sen_list:
        embed_list = []
        for i in range(max_len):
            if i < len(sentence):
                if sentence[i] in word2vec:
                    embed_list.extend(word2vec[sentence[i]])
                else:
                    embed_list.extend(padding_random)
            else:
                embed_list.extend(padding_0)
        data_list.append(embed_list)

    dict_intent = dict()
    data_intent_list = []
    for i in range(len(intent_list)):
        if intent_list[i] not in dict_intent:
            dict_intent[intent_list[i]] = len(dict_intent)
        data_intent_list.append(dict_intent[intent_list[i]])

    # 返回sentence与Intent均是数字形式的
    f_w = open('./dict_intent','wb')
    pickle.dump(dict_intent,f_w)
    f_w.close()
    return data_list,data_intent_list

def str2vec_dev(sen_list,intent_list,max_len,embedding_size):
    # 将字符变为向量
    # 现将词变为数字
    input_f = open('/home/liu/新论文/classify_W/skip-gram-nopos/wordembeddings','rb') # 打开之前训练词向量的词典，词->数字
    word2vec= pickle.load(input_f)
    input_f.close()

    embed_list = []
    data_list = []

    padding_random = np.random.rand(embedding_size)
    padding_0 = [0]*embedding_size

    for sentence in sen_list:
        embed_list = []
        for i in range(max_len):
            if i < len(sentence):
                if sentence[i] in word2vec:
                    embed_list.extend(word2vec[sentence[i]])
                else:
                    embed_list.extend(padding_random)
            else:
                embed_list.extend(padding_0)
        data_list.append(embed_list)
    f_r = open('./dict_intent','rb')
    dict_intent = pickle.load(f_r)
    f_r.close()

    # dict_intent = dict()
    data_intent_list = []
    for i in range(len(intent_list)):
        data_intent_list.append(dict_intent[intent_list[i]])

    # 返回sentence与Intent均是数字形式的
    return data_list,data_intent_list



def build_data(data_path,embedding_size=30,max_len=25):
    sen_list,intent_list= read_data(data_path)
    data_sentence,data_intent = str2vec(sen_list,intent_list,max_len,embedding_size)
    return data_sentence,data_intent

def build_dev(data_path,embedding_size=30,max_len=25):
    sen_list,intent_list= read_data(data_path)
    data_list,data_intent_list = str2vec_dev(sen_list,intent_list,max_len,embedding_size)
    return data_list,data_intent_list


    
    
        

                
            




    
    



