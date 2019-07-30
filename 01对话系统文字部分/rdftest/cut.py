# coding:utf-8
#!/usr/bin/python3 
from pyltp import Segmentor


def cut_sentence(input_sentence):
    segmentor = Segmentor()
    segmentor.load_with_lexicon("/home/liu/ltp_data/cws.model","/home/liu/ltp_data/fulluserdict")
    # 分词模块，输入句子，输出分词，可考虑加入用户词典！
    # input_sentence = "王老师的办公室在哪里"
    words = segmentor.segment(input_sentence)

    result = ' '.join(words)
    result = 'BOS '+result+' EOS'
    return [result] 
# input_sentence = '王老师的办公室在哪' 
# a = cut_sentence(input_sentence)
# print(a[0])

