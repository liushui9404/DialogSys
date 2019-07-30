#! /usr/bin/python3
# coding=utf-8

import pickle
import random
import numpy as np



flatten = lambda l: [item for sublist in l for item in sublist]  # 二维展成一维
index_seq2slot = lambda s, index2slot: [index2slot[i] for i in s]
index_seq2word = lambda s, index2word: [index2word[i] for i in s]


def data_pipeline(data, length=30):
    # data为用readlines()读出来的list，内容为字符串["xxx","xxx"."xxxx"]
    data = [t[:-1] for t in data]  # 去掉'\n'
                                    # 这里方括号只表示这是一行语句，不表示它是list,
                                    # 所以经过这个处理，并没有在原来list外部增加了一层list
    # 数据的一行像这样：'BOS i want to fly from baltimore to dallas round trip EOS
    # \tO O O O O O B-fromloc.city_name O B-toloc.city_name B-round_trip I-round_trip atis_flight'
    # 分割成这样[原始句子的词，标注的序列，intent]
    data = [[t.split("\t")[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]] for t in
            data]
    #将一句话装在一个list里，一个list内有两个list一个字符串,注意split是字符串的成员函数，只能对字符串操作，返回的是list，其内容是分开的字符串

    data = [[t[0][1:-1], t[1][1:], t[2]] for t in data]  # 将BOS和EOS去掉，并去掉对应标注序列中相应的标注
    seq_in, seq_out, intent = list(zip(*data))
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

        temp = seq_out[i]
        if len(temp) < length:
            while len(temp) < length:
                temp.append('<PAD>')
        else:
            temp = temp[:length]
            temp[-1] = '<EOS>'
        sout.append(temp)
        data = list(zip(sin, sout, intent))
    #返回这样：[(['赵','教授',,,'?','EOS','<PAD>','<PAD>'],['o','o','o','student','o','<PAD>,'<PAD>'],'student_list'),([  ],[  ],'  ')]
    return data

# train_data = open('./lt_data/test_set',"r").readlines()
# train_data_ed = data_pipeline(train_data)
# print("train_data_ed",train_data_ed,'\n')



def get_info_from_training_data(data):
    #构建了3对词典，将词变为了数字，三个词典互相独立互不影响
    seq_in, seq_out, intent = list(zip(*data))
    vocab = set(flatten(seq_in))
    slot_tag = set(flatten(seq_out))
    intent_tag = set(intent)
    # 生成word2index
    # word2index = {'<PAD>': 0, '<UNK>': 1, '<SOS>': 2, '<EOS>': 3}
    # for token in vocab:
    #     if token not in word2index.keys():
    #         word2index[token] = len(word2index)


    input_f = open('/home/liu/新论文/classify_W/skip-gram-nopos/dictionary_words','rb')
    word2index = pickle.load(input_f)
    input_f.close()


    # 生成index2word
    index2word = {v: k for k, v in word2index.items()}  #将词典的键值对颠倒过来

    # 生成tag2index
    tag2index = {'<PAD>': 0, "o": 1}
    for tag in slot_tag:
        if tag not in tag2index.keys():
            tag2index[tag] = len(tag2index)

    # 生成index2tag
    index2tag = {v: k for k, v in tag2index.items()}

    # 生成intent2index
    intent2index = {'<UNK>': 0}
    for ii in intent_tag:
        if ii not in intent2index.keys():
            intent2index[ii] = len(intent2index)

    # 生成index2intent
    index2intent = {v: k for k, v in intent2index.items()}

    def save_dict():
        f_word2index = open("./dict_word2index",'wb')
        pickle.dump(word2index,f_word2index)
        f_word2index.close()
        
        f_index2word = open("./dict_index2word",'wb')
        pickle.dump(index2word,f_index2word)
        f_index2word.close()

        f_slot2index = open("./dict_slot2index",'wb')
        pickle.dump(tag2index,f_slot2index)
        f_slot2index.close()

        f_index2slot = open("./dict_index2slot",'wb')
        pickle.dump(index2tag,f_index2slot)
        f_index2slot.close()

        f_intent2index = open("./dict_intent2index",'wb')
        pickle.dump(intent2index,f_intent2index)
        f_intent2index.close()

        f_index2intent = open("./dict_index2intent",'wb')
        pickle.dump(index2intent,f_index2intent)
        f_index2intent.close()

    save_dict()

    return word2index, index2word, tag2index, index2tag, intent2index, index2intent

# word2index, index2word_notuse, slot2index, index2slot, intent2index, index2intent = get_info_from_training_data(train_data_ed)
# print("word2index",word2index,'\n')


def to_index(train, word2index, slot2index, intent2index):
    
    def q_w_dict(i):
        if i in word2index.keys():
            return word2index[i]
        else:
            return word2index['<UNK>']

    def q_s_dict(i):
        if i in slot2index.keys():
            return slot2index[i]
        else:
            return slot2index['o']

    new_train = []
    for sin, sout, intent in train:
        sin_ix = list(map(q_w_dict, sin))
        true_length = sin.index("<EOS>")   # 这里是指真正一句话真正的长度，不算EOS
        sout_ix = list(map(q_s_dict, sout))
        if intent in intent2index.keys():
            intent_ix = intent2index[intent] 
        else:
            intent_ix = intent2index['<UNK>']
            
        new_train.append([sin_ix, true_length, sout_ix, intent_ix])  # 注意append()里面有[]！！
    return new_train



# index_train = to_index(train_data_ed,word2index,slot2index,intent2index)
# print("index_train[0]",index_train[0])



def getBatch(batch_size, train_data):
    random.shuffle(train_data)
    sindex = 0
    eindex = batch_size
    while eindex < len(train_data):
        batch = train_data[sindex:eindex]
        temp = eindex
        eindex = eindex + batch_size
        sindex = temp
        yield batch
