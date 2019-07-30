# coding:utf-8

import aiml

# 创建Kernel()和 AIML 学习文件
kernel = aiml.Kernel()
kernel.learn("/home/liu/00毕业课题/developing/01对话系统文字部分/aiml_files/basic_chat.aiml")
kernel.respond("LOAD AIML B")  #加载basic_chat.aiml文件

# 用于把句子分开
def split_sentence(sentence):
    res = ""
    for s in sentence:
        res = res + s + " "
    res = res[:-1]
    return res

# input_x = '你好张三'
# input_x = "王恒升的办公室在哪个房间"
# input_x = "王恒升老师在哪层办公"
# input_x = "王恒升的办公室在哪"
# input_x = '王恒升老师的学生有谁'
# input_x = "王恒升老师的学生有哪些"
# input_x = '王恒升老师的研究方向是什么'
# input_x = '王恒升老师是什么系的'
# input_x = '王恒升老师的性别是'
# input_x = "姜成是谁的学生"
# input_x = "介绍一下王恒升老师"

def gen_sentence(input_x):

    a = split_sentence(input_x)
    # print("aaa",len(a))
    sent = kernel.respond(a)
    # print(sent)
    return sent

# gen_sentence(input_x)

