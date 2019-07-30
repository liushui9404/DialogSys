#coding:utf-8

import sys
import collections
import math
import os
import random
import zipfile
import re
import numpy as np
# from six.moves import urllib
# from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
import pickle



def read_and_seg(files_read):
    '''
    将文本变为一个list
    '''
    data = list()
    for file in files_read:
        f_read = open(file,'r')
        lines_r = f_read.readlines()
        for sentence in lines_r:
            sen = sentence[:-1]  #去掉最后的换行符号
            words = re.split(' ',sen)
            for word in words:
                data.append(word)


    return data

files_read = ['/home/liu/新论文/语料/整理中/初步完成/用于词向量训练']

words = read_and_seg(files_read)
for i in range(10):
	print(words[i])

print('Data size', len(words))

# Step 2: Build the dictionary and replace rare words with UNK token.
vocabulary_size = len(set(words))+3
print ("vocabulary_size",vocabulary_size)

def build_dataset(words, vocabulary_size):
    count= [('<UNK>', 0),('<PAD>',1),('<EOS>',2)]
    count.extend(collections.Counter(words).most_common(vocabulary_size))#最常用的100个词,注意此处是extend
    dictionary = dict()
    # print("count",count)
  #------------------没弄清楚-----------------
    for word, _ in count:
        dictionary[word] = len(dictionary)#明白了，这里实现词频越大，编号越小，_下划线表示 值（键值对的值，由于用不到，所以给_）
  #------------------------------------------

    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0  # dictionary['UNK']
            unk_count += 1
        data.append(index)#索引
    # count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))#将键和值颠倒过来，值在前，键在后
    return data, count, dictionary, reverse_dictionary

data, count, dictionary, reverse_dictionary = build_dataset(words, vocabulary_size)
print(dictionary['<PAD>'])


output = open('./reverse_dictionary','wb')
pickle.dump(reverse_dictionary,output)
output.close()

output = open('./dictionary_words','wb')
pickle.dump(dictionary,output)
output.close()

del words  # Hint to reduce memory.
print('Most common words (+UNK)', count[:5])
print('Sample data', data[:10], [reverse_dictionary[i] for i in data[:10]])


def load_pos_lay_dict():
    dict_pos = dict()
    pos_set = set()
    file_r = open("/home/liu/新论文/语料/整理中/初步完成/pos_dict",'r')
    text = file_r.readlines()
    for t in text:
        data = t.split()
        if data[0]  not in dict_pos:
            pos_set.add(data[1])
            dict_pos[dictionary[data[0]]] = len(pos_set)-1

    reverse_pos_dict = dict(zip(dict_pos.values(), dict_pos.keys()))
    
    return dict_pos,list(pos_set),len(pos_set)

dict_pos,pos2str,len_set = load_pos_lay_dict()

print("dict_pos",pos2str)
data_index = 0

# Step 3: Function to generate a training batch for the skip-gram model.
def generate_batch(batch_size, num_skips, skip_window):
    global data_index
    assert batch_size % num_skips == 0   #断言，如果为假则抛出异常
    assert num_skips <= 2 * skip_window
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)  # ndarray  n维数组
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    labels_pos = np.ndarray(shape=(batch_size),dtype = np.int32)   # 标签
    span = 2 * skip_window + 1  # [ skip_window target skip_window ]，跨度
    buffer = collections.deque(maxlen=span)   # 双端队列结构，提供了两端插入与删除的操作

    for _ in range(span):
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)# %取余数，将span个单词顺序读入buffer

    for i in range(batch_size // num_skips):#整除，num_skips为对每 个 单词生成多少个训练样本
        target = skip_window  # target label at the center of the buffer。   skip_windows为最远可以联系到的距离
        targets_to_avoid = [skip_window]

        for j in range(num_skips):
            while target in targets_to_avoid:
                target = random.randint(0, span - 1)   #当target在targets_to_void里时，给target赋予新值（新值也有可能在targets_to_void里）
                                               #直到新值不在targets_to_void里。targets_to_void是一个list
                                               #random.randint(a,b),区间为[a,b]，即a b都会包括

            targets_to_avoid.append(target)
            batch[i * num_skips + j] = buffer[skip_window]  #skip_windows为最远可以联系到的距离
            labels[i * num_skips + j, 0] = buffer[target]
            if buffer[skip_window] in dict_pos:
                labels_pos[i * num_skips + j] = dict_pos[buffer[skip_window]]
            else:
                labels_pos[i * num_skips + j] = len_set


        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
  # Backtrack a little bit to avoid skipping words in the end of a batch
    data_index = (data_index + len(data) - span) % len(data)
    return batch, labels,labels_pos

#---------------------测试该函数功能----------------------------------#
batch, labels,labels_pos = generate_batch(batch_size=8, num_skips=2, skip_window=1)
for i in range(8):
    if batch[i] in dict_pos:
        print(batch[i], reverse_dictionary[batch[i]],
            '->', labels[i, 0], reverse_dictionary[labels[i, 0]],dict_pos[batch[i]],pos2str[dict_pos[batch[i]]])
        




# Step 4: Build and train a skip-gram model.

batch_size = 8
embedding_size = 30 # Dimension of the embedding vector.
skip_window = 1       # How many words to consider left and right.
num_skips = 2         # How many times to reuse an input to generate a label.
class_num = len_set+1  # 因为还有一个种类是其他

# We pick a random validation set to sample nearest neighbors. Here we limit the
# validation samples to the words that have a low numeric ID, which by
# construction are also the most frequent.
valid_size = 6     # Random set of words to evaluate similarity on.#验证集的个数
valid_window = 60  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)#从100里面随机抽取16个数
num_sampled = 10    # Number of negative examples to sample.#负采样的个数

graph = tf.Graph()

with graph.as_default():#创建图，并设置为默认

    # Input data.
    train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
    train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])

    train_labels_class = tf.placeholder(tf.int32, shape=[batch_size])  # class_num为要分类的种类数量

    valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

    # Ops and variables pinned to the CPU because of missing GPU implementation
    with tf.device('/cpu:0'):
        # Look up embeddings for inputs.
        embeddings = tf.Variable(
        tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0),name = "embeddings")#平均分布50000*128
        embed = tf.nn.embedding_lookup(embeddings, train_inputs)        #在embedding中查找train_input所对应的表示

        w_class = tf.Variable(tf.random_uniform([embedding_size,class_num], -1.0, 1.0),name = "w_class")
        b_class = tf.Variable(tf.zeros(class_num))
        a_class = tf.nn.bias_add(tf.matmul(embed,w_class),b_class)

        # Construct the variables for the NCE loss
        nce_weights = tf.Variable(
            tf.truncated_normal([vocabulary_size, embedding_size],
                            stddev=1.0 / math.sqrt(embedding_size)))
							
        nce_biases = tf.Variable(tf.zeros([vocabulary_size]))


  # Compute the average NCE loss for the batch.
  # tf.nce_loss automatically draws a new sample of the negative labels each
  # time we evaluate the loss.

  #--------------------------------------------------------------------------#
    with tf.variable_scope("loss"):
        loss_semantics = tf.reduce_mean(
            tf.nn.nce_loss(weights=nce_weights,
                        biases=nce_biases,
                        labels=train_labels,
                        inputs=embed,
                        num_sampled=num_sampled,
                        num_classes=vocabulary_size))
        # tf.scalar_summary("loss",loss)      #语义误差
    loss_class = tf.losses.sparse_softmax_cross_entropy(train_labels_class,a_class)  # 分类误差

    alpha = 0.7  # 控制Loss的比例

    loss = (1-alpha)*loss_semantics + alpha*loss_class




  #--------------------------------------------------------------------------#                   

  # Construct the SGD optimizer using a learning rate of 1.0.
    optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)

  # Compute the cosine similarity between minibatch examples and all embeddings.
    norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
    normalized_embeddings = embeddings / norm
    valid_embeddings = tf.nn.embedding_lookup(
        normalized_embeddings, valid_dataset)
    similarity = tf.matmul(
        valid_embeddings, normalized_embeddings, transpose_b=True)

    saver = tf.train.Saver()

  # Add variable initializer.
    init = tf.global_variables_initializer()
    # merged = tf.merge_all_summaries()  #整理所有的日志文件
    # Step 5: Begin training.
num_steps = 2000
SUMMARY_PATH = "./summary"

with tf.Session(graph=graph) as session:#启动图
  # We must initialize all variables before we use them.
    # summary_writer = tf.train.SummaryWriter(SUMMARY_PATH,session.graph)
    init.run()                            #初始化数据
    print("Initialized")

    average_loss = 0
    for step in range(num_steps):#开始训练
        batch_inputs, batch_labels,batch_labels_pos = generate_batch(
            batch_size, num_skips, skip_window)
        feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels,train_labels_class:batch_labels_pos}

      # We perform one update step by evaluating the optimizer op (including it
      # in the list of returned values for session.run()
        _, loss_val = session.run([optimizer, loss], feed_dict=feed_dict)
        average_loss += loss_val
        # summary_writer.add_summary(summary,step)  #将所有日志写入文件

        if step % 2000 == 0:
            if step > 0:
                average_loss /= 2000
            # The average loss is an estimate of the loss over the last 2000 batches.
            print("Average loss at step ", step, ": ", average_loss)
            average_loss = 0

      # Note that this is expensive (~20% slowdown if computed every 500 steps)
        # if step % 10000 == 0:
        #     sim = similarity.eval()
        #     for i in xrange(valid_size):
        #         # print("valid_example",valid_examples)
        #         # print("reverse_dictionary",reverse_dictionary)
        #         valid_word = reverse_dictionary[valid_examples[i]]
        #         # print("valid_word",valid_word)
        #         top_k = 5  # number of nearest neighbors
        #         nearest = (-sim[i, :]).argsort()[1:top_k + 1]
        #         log_str = "Nearest to %s:" % valid_word
        #         for k in xrange(top_k):
        #             close_word = reverse_dictionary[nearest[k]]
        #             log_str = "%s %s," % (log_str, close_word)
        #         print(log_str)
    final_embeddings = normalized_embeddings.eval()
    print(final_embeddings.shape)
    saver.save(session,"./embedding_model/model.ckpt")
# summary_writer.close()   #关闭日志文件


# Step 6: Visualize the embeddings.可视化


def plot_with_labels(low_dim_embs, labels, filename='tsne.png'):
    assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
    plt.figure(figsize=(18, 18))  # in inches
    zhfont = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/ukai.ttc")
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i, :]
        plt.scatter(x, y)
        label = str(label)
        # print(label)
        plt.annotate(label,
                 xy=(x, y),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom',
                 fontproperties = zhfont)

    plt.savefig(filename)

try:
    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt
    import matplotlib
 

  

    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
    plot_only = vocabulary_size
    low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
    labels = [reverse_dictionary[i] for i in range(plot_only)]
    plot_with_labels(low_dim_embs, labels)

except ImportError:
    print("Please install sklearn, matplotlib, and scipy to visualize embeddings.")
