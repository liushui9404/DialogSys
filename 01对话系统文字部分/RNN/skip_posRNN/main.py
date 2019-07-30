#! /usr/local/bin/python3
# coding=utf-8

import matplotlib.pyplot as plt   # 导入画图库
import tensorflow as tf
from data import *
# from model import Model
from model import Model
from my_metrics import *
from tensorflow.python import debug as tf_debug
import os
import pickle

input_steps = 30   #展开步数为30
embedding_size = 30 #内部生成词向量维数为30
hidden_size = 200  #LSTM隐藏层神经元个数
n_layers = 2       #隐藏层数
batch_size = 64     #训练bitch
vocab_size = 707    #输入句子词典的大小，不包括pos
slot_size = 22      #槽的个数
intent_size = 9    #意图的个数
epoch_num = 50     #训练的轮数


SAVE_PATH = "./model/"
MODEL_NAME = "lt_model.ckpt"

    

def get_model():
    model = Model(input_steps, embedding_size, hidden_size, vocab_size, slot_size,
                 intent_size, epoch_num, batch_size, n_layers)
    model.build()
    return model


def train(is_debug=False):
    model = get_model()
    saver = tf.train.Saver()   # 初始化一个保存器,一定要放在模型的后面
    sess = tf.Session()
    if is_debug:
        sess = tf_debug.LocalCLIDebugWrapperSession(sess)
        sess.add_tensor_filter("has_inf_or_nan", tf_debug.has_inf_or_nan)
        
    sess.run(tf.global_variables_initializer())
    # print(tf.trainable_variables())
    train_data = open("/home/liu/新论文/语料/整理中/初步完成/用于评价", "r").readlines()
    test_data = open("/home/liu/新论文/语料/整理中/初步完成/用于评价", "r").readlines()
    train_data_ed = data_pipeline(train_data)
    test_data_ed = data_pipeline(test_data)
    # print("test_data_ed",train_data_ed[0])
    

    word2index, index2word, slot2index, index2slot, intent2index, index2intent = \
        get_info_from_training_data(train_data_ed)
    # print("slot2index: ", slot2index)
    # print("index2slot: ", index2slot)
    index_train = to_index(train_data_ed, word2index, slot2index, intent2index)
    index_test = to_index(test_data_ed, word2index, slot2index, intent2index)
    # print index_train[0]
    # [[631, 167, 18, 829, 114, 530, 18, 401, 49, 834, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 10, [2, 2, 2, 2, 2, 83, 2,
    #  94, 89, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 21]
    
    step_total = 0  #用于确定总步数

    epoch_list = []    # 用于记录步数
    slot_acc_list_mean = []
    intent_acc_list_mean = []
    f1_list = []

    for epoch in range(epoch_num):
        mean_loss = 0.0
        train_loss = 0.0
        for i, batch in enumerate(getBatch(batch_size, index_train)):
            # 执行一个batch的训练
            _, loss, decoder_prediction, intent, mask, slot_W = model.step(sess, "train", batch)

            # if i == 0:
            #     index = 0
            #     print("training debug:")
            #     print("input:", list(zip(*batch))[0][index])
            #     print("length:", list(zip(*batch))[1][index])
            #     print("mask:", mask[index])
            #     print("target:", list(zip(*batch))[2][index])
            #     # print("decoder_targets_one_hot:")
            #     # for one in decoder_targets_one_hot[index]:
            #     #     print(" ".join(map(str, one)))
            #     print("decoder_logits: ")
            #     for one in decoder_logits[index]:
            #         print(" ".join(map(str, one)))
            #     print("slot_W:", slot_W)
            #     print("decoder_prediction:", decoder_prediction[index])
            #     print("intent:", list(zip(*batch))[3][index])

            mean_loss += loss
            train_loss += loss
            if i % 10 == 0:
                if i > 0:
                    mean_loss = mean_loss / 10.0
                print('Average train loss at epoch %d, step %d: %f' % (epoch, i, mean_loss))
                mean_loss = 0
        train_loss /= (i + 1)
        print("[Epoch {}] Average train loss: {}".format(epoch, train_loss))
        print("训练步数：",i+1)

        # 每训一个epoch，测试一次
        slot_acc_list = []   #用于记录slot的准确率
        intent_acc_list = [] #用于记录Intent的准确率

        pred_slots = []
        for j, batch in enumerate(getBatch(batch_size, index_test)):
            decoder_prediction, intent = model.step(sess, "test", batch)
            decoder_prediction = np.transpose(decoder_prediction, [1, 0])
            if j == 0:
                index = random.choice(range(len(batch)))   #只从中选择一个数
                # print("len_batch",len(batch))   #16
                # index = 0
                print("Input Sentence        : ", index_seq2word(batch[index][0], index2word))
                print("Slot Truth            : ", index_seq2slot(batch[index][2], index2slot))
                print("Slot Prediction       : ", index_seq2slot(decoder_prediction[index], index2slot))
                print("Intent Truth          : ", index2intent[batch[index][3]])
                print("Intent Prediction     : ", index2intent[intent[index]])
            slot_pred_length = list(np.shape(decoder_prediction))[1]
            pred_padded = np.lib.pad(decoder_prediction, ((0, 0), (0, input_steps-slot_pred_length)),
                                     mode="constant", constant_values=0)
            pred_slots.append(pred_padded)
            # print("slot_pred_length: ", slot_pred_length)
            true_slot = np.array((list(zip(*batch))[2]))
            true_length = np.array((list(zip(*batch))[1]))
            true_slot = true_slot[:, :slot_pred_length]
            # print(np.shape(true_slot), np.shape(decoder_prediction))
            # print(true_slot, decoder_prediction)
            slot_acc = accuracy_score(true_slot, decoder_prediction, true_length)
            intent_acc = accuracy_score(list(zip(*batch))[3], intent)
            print("slot accuracy: {}, intent accuracy: {}".format(slot_acc, intent_acc))
        pred_slots_a = np.vstack(pred_slots)
        # print("pred_slots_a: ", pred_slots_a.shape)
        true_slots_a = np.array(list(zip(*index_test))[2])[:pred_slots_a.shape[0]]
        # print("true_slots_a: ", true_slots_a.shape)
        epoch_list.append(epoch)  # 记录步数
        slot_acc_list_mean.append(np.mean(slot_acc_list))  # 记录平均acc
        intent_acc_list_mean.append(np.mean(intent_acc_list))  # 记录平均acc
        f1_list.append(f1_for_sequence_batch(true_slots_a, pred_slots_a))

        saver.save(sess,os.path.join(SAVE_PATH,MODEL_NAME),global_step=epoch)  #保存模型,每一个epoch保存一次

        print("F1 score for epoch {}: {}".format(epoch, f1_for_sequence_batch(true_slots_a, pred_slots_a)))
    # plt.plot(epoch_list,slot_acc_list_mean,'b-',lw=2,label='slot_acc')
    # plt.plot(epoch_list,intent_acc_list_mean,'r-',lw=2,label='intent_acc')


    file_o = open("./f1_list_skip","wb")
    pickle.dump(f1_list,file_o)
    file_o.close()

    plt.plot(epoch_list,f1_list,'r-',lw=2,label='f1')
    plt.legend(loc='upper left')
    # plt.show()
    plt.savefig('./show_result.png')


#用于测试数据
def test_data():
    train_data = open("/home/liu/新论文/语料/整理中/初步完成/用于评价", "r").readlines()
    test_data = open("/home/liu/新论文/语料/整理中/初步完成/用于评价", "r").readlines()
    train_data_ed = data_pipeline(train_data)
    test_data_ed = data_pipeline(test_data)

    word2index, index2word, slot2index, index2slot, intent2index, index2intent = \
        get_info_from_training_data(train_data_ed)
    # print("slot2index: ", slot2index)
    # print("index2slot: ", index2slot)
    index_train = to_index(train_data_ed, word2index, slot2index, intent2index)
    # print("index_train",index_train)

    index_test = to_index(test_data_ed, word2index, slot2index, intent2index)

    
    batch = next(getBatch(batch_size, index_test))
    unziped = list(zip(*batch))
    print("word num: ", len(word2index.keys()), "slot num: ", len(slot2index.keys()), "intent num: ",
          len(intent2index.keys()))
    print("各种shape",np.shape(unziped[0]), np.shape(unziped[1]), np.shape(unziped[2]), np.shape(unziped[3]))
    print(np.transpose(unziped[0], [1, 0]))
    print(unziped[1])
    print(np.shape(list(zip(*index_test))[2]))
    

    


if __name__ == '__main__':
    # train(is_debug=True)
    # test_data()
    train()
    