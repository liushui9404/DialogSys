#! /usr/local/bin/python3
#coding:utf-8


import tensorflow as tf 
import numpy as np 
import pickle
# from data import data_pipeline,to_index
import time
# /home/liu/01对话系统文字部分/RNN/skip_posRNN
# x1 = ["BOS 王 老师 的 办公室 在 哪 一 层 ? EOS"]
def load_file():  # x1是输入的一句话
    
    # 将之前保存的字典加载进来
    f_index2slot = open("../../../01对话系统文字部分/RNN/skip_posRNN/dict_index2slot",'rb')
    # f_index2slot = open("./RNN/skip_posRNN/dict_index2slot",'rb')
    index2slot = pickle.load(f_index2slot)  # 用
    f_index2slot.close()

    f_index2intent = open("../../../01对话系统文字部分/RNN/skip_posRNN/dict_index2intent","rb")
    # f_index2intent = open("./RNN/skip_posRNN/dict_index2intent","rb")
    index2intent = pickle.load(f_index2intent)   # 用
    f_index2intent.close()

    f_word2index = open("../../../01对话系统文字部分/RNN/skip_posRNN/dict_word2index","rb")
    # f_word2index = open("./RNN/skip_posRNN/dict_word2index","rb")
    word2index = pickle.load(f_word2index)   # 用
    f_word2index.close()

    f_slot2index = open("../../../01对话系统文字部分/RNN/skip_posRNN/dict_slot2index","rb")
    # f_slot2index = open("./RNN/skip_posRNN/dict_slot2index","rb")
    slot2index = pickle.load(f_slot2index)  # 用
    f_slot2index.close()

    f_intent2index = open("../../../01对话系统文字部分/RNN/skip_posRNN/dict_intent2index","rb")
    # f_intent2index = open("./RNN/skip_posRNN/dict_intent2index","rb")
    intent2index = pickle.load(f_intent2index)  
    f_intent2index.close()


    index_seq2word = lambda s, index2word: [index2word[i] for i in s]

    return index2slot,index2intent,word2index

    # x = ["BOS SURNAME 老师 的 办公室 在 哪 一 层 ? EOS	o first_name teacher1-2 o office2-3-1 o where o floor2-1 o is_located_in&is_in_floor_of",
    # "BOS SURNAME 老师 的 办公室 在 哪 一 层 ? EOS	o first_name teacher1-2 o office2-3-1 o where o floor2-1 o is_located_in&is_in_floor_of",
    # "BOS SURNAME 讲师 的 硕士生 有 哪些 ? EOS	o o o master1-1-1-1 o list o is_a_teacher_of&is_a",
    # "BOS SURNAME 老师 的 硕士生 有 哪些 人 ? EOS	o first_name teacher1-2 o master1-1-1-1 o list person1 o is_a_teacher_of&is_a"]
    # x = ["BOS SURNAME 老师 的 办公室 在 哪 一 层 ? EOS	o first_name teacher1-2 o office2-3-1 o where o floor2-1 o is_located_in&is_in_floor_of",
    # "BOS SURNAME 老师 的 办公室 在 哪 一 层 ? EOS	o first_name teacher1-2 o office2-3-1 o where o floor2-1 o is_located_in&is_in_floor_of"]


def data_pipeline_1(data, length=30):
    
    data = [t.split() for t in data]
    seq_in = [t[1:-1] for t in data]  # 将BOS和EOS去掉
    # print("seq_in",seq_in)  # [['SURNAME', '老师', '的', '办公室', '在', '哪', '一', '层', '?']]
    sin = []
    sout = []
    # padding，原始序列和标注序列结尾+<EOS>+n×<PAD>
    for i in range(len(seq_in)):
        temp = seq_in[i]
        if len(temp) < length:
            temp.append('<EOS>')
            while len(temp) < length:
                temp.append('<PAD>')
        else:
            temp = temp[:length]
            temp[-1] = '<EOS>'
        sin.append(temp)

    return sin    





def to_index_1(train, word2index):

    def q_w_dict(i):
        if i in word2index.keys():
            return word2index[i]
        else:
            return word2index['<UNK>']

    new_train = []
    for sin in train:
        sin_ix = list(map(q_w_dict, sin))
        true_length = sin.index("<EOS>")   # 这里是指真正一句话真正的长度，不算EOS
        new_train.append([sin_ix,true_length])  # 注意append()里面有[]！！
    return new_train         

    # x1 = ["BOS SURNAME 老师 的 办公室 在 哪 一 层 ? EOS	o first_name teacher1-2 o office2-3-1 o where o floor2-1 o is_located_in&is_in_floor_of"]


def loadRnn():
    # graph = tf.Graph()
    
    # sess = tf.Session()
    # sess.as_default()
    # global saver
    time_b = time.time()
    saver = tf.train.import_meta_graph("../../../01对话系统文字部分/RNN/skip_posRNN/model/lt_model.ckpt-48.meta")   # 加载图
    # saver = tf.train.import_meta_graph("./RNN/skip_posRNN/model/lt_model.ckpt-48.meta")   # 加载图
    sess = tf.Session()
    saver.restore(sess,"../../../01对话系统文字部分/RNN/skip_posRNN/model/lt_model.ckpt-48")
    # saver.restore(sess,"./RNN/skip_posRNN/model/lt_model.ckpt-48")
    time_e = time.time()
    print("加载模型所用时间1",time_e-time_b,"秒")
    # saver.restore(sess,"./RNN/skip_posRNN/model/lt_model.ckpt-48")    # 加载模型
    # time_e1 = time.time()
    # print("加载模型所用时间1",time_e1-time_e,"秒")
    graph = tf.get_default_graph()
    

    return sess,saver,graph


def load_model(x1,sess,saver,graph,index2slot,index2intent,word2index):
    x_return = x1[0].split()[1:-1]
    test_data_1 = data_pipeline_1(x1,length=30)

    index_train_1 = to_index_1(test_data_1, word2index)

    time_e = time.time()
    # print("加载模型所用时间1",time_e-time_b,"秒")
    
    # saver.restore(sess,"../../../01对话系统文字部分/RNN/skip_posRNN/model/lt_model.ckpt-48")    # 加载模型
    # saver.restore(sess,"./RNN/skip_posRNN/model/lt_model.ckpt-48")    # 加载模型
    
    with graph.as_default():
        x_input_sentence = graph.get_operation_by_name("encoder_inputs").outputs[0]
        x_input_actual_length = graph.get_operation_by_name("encoder_inputs_actual_length").outputs[0]

        y_intent_pred = graph.get_operation_by_name("pred_intent").outputs[0]
        y_solt_pred = tf.get_collection("pred_solt")
        

        unziped = list(zip(*index_train_1))
        # print("unzipde",unziped)
        time_b = time.time()
        decoder_prediction, intent = sess.run([y_solt_pred,y_intent_pred],feed_dict={x_input_sentence:np.transpose(unziped[0],[1,0]),
                                                                                        x_input_actual_length:unziped[1]})
        # print("decoder_prediction",np.shape(decoder_prediction))
        # print("decoder_prediction",np.transpose(decoder_prediction,[0,2,1]))
        time_e = time.time()
        print("运行所用时间2",time_e-time_b,"秒")
        decoder_prediction = np.transpose(decoder_prediction,[0,2,1])

        index_seq2slot = lambda s, index2slot: [index2slot[i] for i in s]
        index=0

        result  = index_seq2slot(decoder_prediction[index][0], index2slot)
        print("result = ",result)
        del(result[-1])  # 删除<EOS>对应的o
        # print(result)
        # print(index2intent[intent[index]])
    return x_return,result,index2intent[intent[index]]


# x1 = ["BOS SURNAME 老师 的 办公室 在 哪 一 层"]
# sess,saver = loadRnn()  #加载模型
# index2slot,index2intent,word2index = load_file()
# x_return,slot,intent = load_model(x1,sess,saver,index2slot,index2intent,word2index)

# a = time.time()
# for _ in range(100):
#     x_return,slot,intent = load_model(x1,saver)   
#     # print(intent)
# b  = time.time()

# print("100: ",b-a)