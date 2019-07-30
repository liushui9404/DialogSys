# coding:utf-8
#!/usr/bin/python3 
from pyltp import Segmentor
# /home/liu/ltp_data

def cut_sentence():
    segmentor = Segmentor()
    # segmentor.load_with_lexicon("../../../../../ltp_data/cws.model","../../../../../ltp_data/fulluserdict")
    segmentor.load_with_lexicon("/home/liu/ltp_data/cws.model","/home/liu/ltp_data/fulluserdict")
    # 分词模块，输入句子，输出分词，可考虑加入用户词典！
    # input_sentence = "王老师的办公室在哪里"
    f = open('./负样本未分词文件.txt','r')
    sentences = f.readlines()
    fW = open("./负样本",'w')
    for sentence in sentences:
        words = segmentor.segment(sentence)
        result = ' '.join(words)
        fW.write(result+'\n')

    fW.close()
    f.close()
# input_sentence = '王老师的办公室在哪' 
# a = cut_sentence(input_sentence)
# print(a[0])

# def generateCutedFile():
#     f = open('./负样本未分词文件.txt','r')
#     sentences = f.readlines()
#     fW = open("./负样本",'w')
#     for sentence in sentences:
#         cuted = cut_sentence(sentence)
#         fW.write(cuted+'\n')
#     fW.close()
#     f.close()    

cut_sentence()