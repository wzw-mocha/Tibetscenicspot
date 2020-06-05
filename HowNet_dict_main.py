# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import warnings
import jieba
warnings.filterwarnings("ignore")

#读取文件，返回一个list
def read_lines(filename):
    fp = open(filename,'r', encoding='utf-8')
    lines = []
    for line in fp.readlines():
        line = line.strip()
        lines.append(line)
    fp.close()
    return lines
# 分句
def cut_sents(text, punctuation_list='!?。！？'):
    """
       将文本段安装标点符号列表里的符号切分成句子，将所有句子保存在列表里。
       """
    sentence_set = []  #存放分句结果
    inx_position = 0  # 索引标点符号的位置
    char_position = 0  # 移动字符指针位置
    for char in text:  #逐个遍历字符
        char_position += 1  #移动字符位置
        if char in punctuation_list:  #遍历分句符号
            next_char = list(text[inx_position:char_position + 1]).pop()  #获取下一个字符
            if next_char not in punctuation_list:  #下一个字符不是分句符号，在此处进行分句
                sentence_set.append(text[inx_position:char_position])
                inx_position = char_position   #改变标点符号的位置
    if inx_position < len(text):  #处理句尾没有符号的情况
        sentence_set.append(text[inx_position:])
    return sentence_set  #返回分句列表

# 去除停用词
def del_stopwords(seg_sent):
    stopwords = read_lines("./Sentiment_dict/emotion_dict/stop_words.txt")  # 读取停用词表
    new_sent = []   # 去除停用词后的句子
    for word in seg_sent:
        if word in stopwords:
            continue
        else:
            new_sent.append(word)
    return new_sent

# 1.读取情感词典和待处理文件
# 情感词典
print("reading...")

posdict = read_lines("./Sentiment_dict/emotion_dict/pos_dict.txt") #读取积极情感词典
negdict = read_lines("./Sentiment_dict/emotion_dict/neg_dict.txt") #读取消极情感词典

# 程度副词词典
mostdict = read_lines('./Sentiment_dict/degree_dict/most.txt')   # 权值为2
verydict = read_lines('./Sentiment_dict/degree_dict/very.txt')   # 权值为1.5
moredict = read_lines('./Sentiment_dict/degree_dict/more.txt')   # 权值为 1.25
ishdict = read_lines('./Sentiment_dict/degree_dict/ish.txt')   # 权值为0.5
insufficientdict = read_lines('./Sentiment_dict/degree_dict/insufficiently.txt')  # 权值为0.25
inversedict = read_lines('./Sentiment_dict/degree_dict/notDic.txt')  # 权值为-1


# 2.程度副词处理，根据程度副词的种类不同乘以不同的权值
def match(word, sentiment_value):
    if word in mostdict:
        sentiment_value *= 2.0
    elif word in verydict:
        sentiment_value *= 1.5
    elif word in moredict:
        sentiment_value *= 1.25
    elif word in ishdict:
        sentiment_value *= 0.5
    elif word in insufficientdict:
        sentiment_value *= 0.25
    elif word in inversedict:
        sentiment_value *= -1
    return sentiment_value

# 求单条评论的情感倾向总得分
def single_review_sentiment_score(text):

    seg_sent = jieba.lcut(text)   # 分词
    seg_sent =del_stopwords(seg_sent)  #去除停用词
    print('去除停用词结果',seg_sent)
    i = 0    # 记录扫描到的词的位置
    all_poscount = 0    # 记录该分句中的积极情感得分
    all_negcount = 0    # 记录该分句中的消极情感得分
    for word in seg_sent:   # 逐词分析
        poscount=0
        negcount=0
        if word in posdict:  # 如果是积极情感词
            if i==0 or i ==len(seg_sent)-1:
                poscount=1.2    #首尾情感积极得分+1.2
            else:
                poscount = 1   # 其他位置积极得分+1

            if i-3>0:   #滑移窗口的设置，滑移步长为3，即判定情感词前面三个词语的程度值
                for w in seg_sent[i-3:i+2]:  #情感词的位置小于3时，将扫描情感词前面的所有词语（词语数小于3）
                    poscount = match(w, poscount)
            else:
                for w in seg_sent[0:i+2]:
                    poscount = match(w, poscount)

        elif word in negdict:  # 如果是消极情感词
            if i == 0 or i == len(seg_sent) - 1:
                negcount = 1.2    #首尾消极情感得分+1.2
            else:
                negcount = 1    # 其他位置积极得分+1
            if i - 3 > 0:  # 滑移窗口的设置，滑移步长为3，即判定情感词前面三个词语的程度值
                for w in seg_sent[i-3:i+2]:   #情感词的位置小于3时，将扫描情感词前面的所有词语（词语数小于3）
                    negcount = match(w, negcount)
            else:
                for w in seg_sent[0:i+2]:
                    negcount = match(w, negcount)

        # 如果是感叹号，表示已经到本句句尾
        elif (word == "！"or word == "!") and (i ==len(seg_sent)-1):
            for w2 in seg_sent[::-1]:  # 倒序扫描感叹号前的情感词，发现后权值+2，然后退出循环
                if w2 in posdict:
                    poscount = 2
                    break
                elif w2 in negdict:
                    negcount = 2
                    break
        i += 1
        all_negcount+=negcount
        all_poscount+=poscount
    text_score=all_poscount-all_negcount
    if text_score>1:
        text_score=1
    elif text_score<-1:
        text_score=-1
    return text_score,' '.join(seg_sent)

# 分析文本，返回一个列表，列表中元素为（分值，评论）元组
def run_score(data,savepath):
    data = data.drop_duplicates()
    contents = data['content']
    scores = []
    cut_words=[]
    for index, content in enumerate(contents):
        content = str(content).replace('\n', '****')  # 用****替换换行符
        print(content)
        score,cut_word = single_review_sentiment_score(content)
        print('情感得分：{}\n'.format(score))
        scores.append(score)
        cut_words.append(cut_word)
    data['cut_word'] = cut_words
    data['sentiment'] = scores
    data.to_excel(savepath,index=None, encoding='utf-8-sig')

def main():

    path='result/指标关键词文本.xlsx'
    savepath='result/情感分析结果.xlsx'
    data = pd.read_excel(path)
    run_score(data,savepath)

if __name__ == '__main__':
    main()


