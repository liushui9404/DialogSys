# coding:utf-8

from pyltp import Segmentor
# /home/liu/ltp_data

class wordSegment(object):
    def __init__(self):
        self.hasSentence = False  # 表示是否有词语进入分词器中
        self.segmentor = Segmentor()
        self.segmentor.load_with_lexicon("/home/liu/ltp_data/cws.model","/home/liu/ltp_data/fulluserdict")
    
    def isEmpty(self,result):
        self.hasSentence = False
        for w in result:
            if w !="" or w!=" ":
                self.hasSentence = True
        
    def cut_sentence(self,input_sentence):
        
        # segmentor.load_with_lexicon("../../../../../ltp_data/cws.model","../../../../../ltp_data/fulluserdict")
        
        # 分词模块，输入句子，输出分词，可考虑加入用户词典！
        # input_sentence = "王老师的办公室在哪里"
        words = self.segmentor.segment(input_sentence)

        result = ' '.join(words)
        self.isEmpty(result)
        result = 'BOS '+result+' EOS'
        return [result] 

# input_sentence = '李世玮的学术报告开始时间是几点' 
# wordSegmentor = wordSegment()
# a = wordSegmentor.cut_sentence(input_sentence)
# print("分词结果",a)
# print(wordSegmentor.hasSentence)


