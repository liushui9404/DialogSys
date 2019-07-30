# coding:utf-8
import sklearn

from sklearn.externals import joblib
import pickle
import numpy as np
# import cut
#---------------------------基础数据------------------------------
# 副教授
name_of_teacher_1 = ['何玉辉','何虎','冯佩','刘厚根','刘峙林','刘春辉','刘景琳','吴旺青','吴波','周亚军','崔晓辉','张星星','戴瑜',
                    '朱桂华','李松柏','李毅波','李群明','柳波','樊广军','汤晓燕','王刚','王聪','王青山','申儒林','石琛','罗春雷',
                    '罗筱英','胡友旺','胡小舟','胡琼','谢习华','谢敬华','贺继林','赵宏强','郑煜','钟国梁','陈思雨','陈明松','韩奉林',
                    '黄始全','龚海']

# 教授
name_of_teacher_2 = ['严宏志','云忠','何竞飞','傅志红','刘义伦','刘少军','刘德福','吴万荣','吴运新','周海波','唐华平','唐进元','喻海良',
                    '夏建芳','夏益敏','孙小燕','帅词俊','廖平','张怀亮','张立华','徐海良','易幼平','朱建新','朱文辉','李军辉','李力',
                    '李建军','李建平','李新和','李晓谦','李涵雄','李艳','杨忠炯','杨放琼','欧阳鸿武','段吉安','汪炼成','湛利华','王恒升',
                    '王福亮','王艾伦','翁灿','胡仕成','胡军科','胡均平','蒋炳炎','蔺永诚','谭建平','谭青','贺地求','赵海鸣','邓华','邓圭玲',
                    '钟掘','陆新江','韩雷','黄元春','黄志辉','黄明辉','黄长清','王恒升']
# 讲师
name_of_teacher_3 = ['周亮','周元生','李向华','王彦','赵兴','邓积微','陈桌','陈志','魏文元','黄志雄']


name_of_teacher = name_of_teacher_1+name_of_teacher_2+name_of_teacher_3
name_of_student = ['刘通','刘润华','章壮','邱伟俊','姜成','王韬']

p_prop = ['性别','研究 方向','所属 系所','研究','系所','系']

first_name = ['严','云','何','傅','冯','刘','吴','周','唐','喻','夏','姜','孙','崔','帅','廖','张','徐','戴','易','朱','李',
                '杨','柳','樊','欧阳','段','汤','汪','湛','王','申','石','罗','翁','胡','蒋','蔺','谢','谭','贺','赵','邓',
                '郑','钟','陆','陈','韩','魏','黄','龚']
types = ["老师","教授","副教授","导师","讲师"]
# print(len(name_of_teacher[0])+len(name_of_teacher[1])+len(name_of_teacher[2]))

office = ["A509","A511","A512","A513","A514","A515","A517","A518","A519","A520","A521","A521","A522","A523","A524",
            "A526","A601","A602","A603","A604","A605","A606","A607","A608","A609","A610","A611","A612","A613","A614",
            "A616","A618","A620","A621","A622","A623","A624","A625","A626","A401","A402","A403","A404","A405","A406",
            "A407","A408","A409","A410","A411","A412","A413","A414","A415","A416","A417","A418","A419","A420","A421",
            "A422","A423","A425","A301","A302","A303","A304","A305","A306","A307","A308","A309","A310","A311","A312",
            "A313","A314","A315","A316","A317","A318","A319","A320","A321","A322","A323","A324","A325","A326","A327",
            "A328"]
student = ['学生','博士','硕士','本科生','研究生','硕士生','博士生']
o = ['在','有','哪些','请问','本次','是']

#---------------------------以上是基础数据------------------------------


def loaddict():
    input_f = open('/home/liu/新论文/classify_W/skip-gram-nopos/wordembeddings','rb') # 打开之前训练词向量的词典，词->数字
    word2vec= pickle.load(input_f)
    input_f.close()
    f_r = open('../../../01对话系统文字部分/tplt/dict_intent','rb')
    # f_r = open('./tplt/dict_intent','rb')
    dict_intent = pickle.load(f_r)
    f_r.close()

    return word2vec,dict_intent

def sent2vec(sentList,word2vec,dict_intent,embedding_size,maxLength):
    embed_list = []
    data_list = []

    padding_random = np.random.rand(embedding_size)
    padding_0 = [0]*embedding_size

    for i in range(maxLength):
        if i<len(sentList):
            if sentList[i] in word2vec:
                embed_list.extend(word2vec[sentList[i]])
            else:
                embed_list.extend(padding_random)
        else:
            embed_list.extend(padding_0)
            
    return [embed_list]
    
def reverseIntentDict(dict_intent):
    return dict((v,k) for k,v in dict_intent.items())



# sentList = ['王恒升','老师','办公室','在','哪']
def genIntent(sentList,clf):

    word2vec,dict_intent = loaddict()
    embedList = sent2vec(sentList,word2vec,dict_intent,embedding_size=30,maxLength=25)
    num2intent = reverseIntentDict(dict_intent)

    
    intent = clf.predict(embedList)[0]
    return num2intent[intent]




def toString(cutedSentence):  # 去掉开头与结尾BOS EOS
    sentence = cutedSentence[0]
    sentList = sentence.split()
    return sentList[1:-1]


def genSlot(sentList):
    slot = []
    catchFlag = []
    lengthOfSent = len(sentList)
    for i in range(lengthOfSent):
        slot.append('o')
        catchFlag.append(0)

    # 这里要有一个状态位！！表明这个槽位被模板引擎捕获！，目的是与RNN模块得到的结果进行比较，没有被捕获的使用RNN!

    for index,word in enumerate(sentList):
        if word in name_of_teacher or word in name_of_student:
            slot[index] = 'name'
            catchFlag[index]=1
        elif word in first_name:
            slot[index] = 'first_name'
            catchFlag[index]=1
        elif word in ["老师","教授","副教授","讲师"]:
            slot[index] = 'teacher'
            catchFlag[index]=1
        elif word in ["办公室"]:
            slot[index] = 'room'
            catchFlag[index]=1
        elif word in ["哪","哪里"]:
            slot[index] = 'where'
            catchFlag[index]=1
        elif word in ['层','栋']:
            slot[index]='area'
            catchFlag[index]=1
        elif word in p_prop:
            slot[index] = 'p-prop'
            catchFlag[index]=1
        elif word in ['谁']:
            slot[index] = 'who'
            catchFlag[index]=1
        elif word in student:
            slot[index] = 'student'
            catchFlag[index]=1
        elif word in office:
            slot[index] = 'room'
            catchFlag[index]=1
        elif word in o:
            slot[index] = 'o'
            catchFlag[index]=1
        

    return slot,catchFlag
    # print(name_of_teacher)

def sent2IntentSlot(cutedSentence,clf):

    sentList = toString(cutedSentence)
    slot,catchFlag = genSlot(sentList)  # 产生槽
    
    intent = genIntent(sentList,clf)  # 产生意图

    return sentList,slot,intent,catchFlag


# x = "王恒升老师在哪层办公"
# x = "王恒升在哪办公"
# x = "王恒升在哪"
# x = "王恒升老师办公室在哪"
# x = "王恒升老师办公室在哪栋"
# x = "王恒升老师办公室在哪"
# x = "王恒升老师的研究方向是什么"
# x = "王恒升的研究方向是什么"
# x = '王恒升老师是什么系的'
# x = '王恒升老师的性别是'
# x = '王恒升的性别是'
# x = '姜成是谁的学生'
# x = '刘通是谁的学生'
# x = '介绍一下王恒升老师' 
# x = '介绍一下王恒升'
# x = '我想找王恒升老师怎样走'
# x = '王老师的办公室在哪'
# x = '我想'
# x = "王恒升老师"
# x = "邓老师的研究方向是" 
# x = "A513是谁的办公室" 

# cutedSentence = cut.cut_sentence(x)
# print("分词后的句子",cutedSentence)

# sent2IntentSlot(cutedSentence)
