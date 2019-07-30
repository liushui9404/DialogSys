#! /usr/local/bin/python3
#coding:utf-8
import tensorflow as tf
import pickle
import os
import numpy as np 
import sys


def generate_embedding():
    saver = tf.train.import_meta_graph("./embedding_model/model.ckpt.meta")

    with tf.Session() as sess:
        saver.restore(sess,"./embedding_model/model.ckpt")
        embeddings = sess.run(tf.get_default_graph().get_tensor_by_name("embeddings:0"))#为矩阵numpy.ndarray，
                                                                                        #行数为单词个数，列数为词向量维数
        # print type(embeddings)

    return embeddings             

embeddings = generate_embedding()

file_input = open("./reverse_dictionary","rb")
reverse_dictionary = pickle.load(file_input)
file_input.close()

# os.remove("./reverse_dictionary")
# print reverse_dictionary

def bulid_dict(embeddings,reverse_dictionary):
    dict_embeddings=dict()
    # print "dictionary_size",len(reverse_dictionary)
    for i in range(len(reverse_dictionary)):
        dict_embeddings[reverse_dictionary[i]] = embeddings[i]
    
    return dict_embeddings
dict_embeddings = bulid_dict(embeddings,reverse_dictionary)
# print "dict_emb\n",dict_embeddings
file_save = open("./embeddings","wb")
pickle.dump(embeddings,file_save)
file_save.close()

file_save = open("./wordembeddings","wb")
pickle.dump(dict_embeddings,file_save)
file_save.close()



def cal_top_sim(top_num,input):
    print(input)
    dict_embeddings = bulid_dict(embeddings,reverse_dictionary)
    cos_dict = dict()
    # print len(dict_embeddings)
    j = 0
    vec_target =np.array(dict_embeddings[input])
    for i in dict_embeddings:  #{"原点"：[0.1,0.4,0.8...]}
        if i != input:
            vec = np.array(dict_embeddings[i])
            # print(vec)
            cos = np.matmul(vec,vec_target)/(np.sqrt(np.matmul(vec,vec.T))*np.sqrt(np.matmul(vec_target,vec_target.T)))
            cos_dict[i] = cos
    vals = sorted(cos_dict.values(),reverse = True )
    reverse_dict = {v:k for k,v in cos_dict.items()}

    j = 0
    for cos_val in vals:
        print(cos_val,reverse_dict[cos_val])
        j=j+1
        if j>=top_num:
            break
        
    print()    
    return cos_dict      

cos_dict = cal_top_sim(10,"学生")
cos_dict = cal_top_sim(10,"研究生")
cos_dict = cal_top_sim(10,"硕士生")
cos_dict = cal_top_sim(10,"硕士")
cos_dict = cal_top_sim(10,"博士")
cos_dict = cal_top_sim(10,"博士生")

cos_dict = cal_top_sim(10,"老师")
cos_dict = cal_top_sim(10,"教授")
cos_dict = cal_top_sim(10,"讲师")
cos_dict = cal_top_sim(10,"副教授")
cos_dict = cal_top_sim(10,"导师")
#改写成类
