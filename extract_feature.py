#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2019/9/26 9:13
#@Author  :花神庙
#@email  :m201871632@hust.edu.cn
#@FileName: extract_feature.py
#@Software: PyCharm


import pandas as pd
import jieba
from jieba import analyse
import collections

jieba.load_userdict('dict/user_dict.txt')
def tf_idf(text,key_num):
    # 引入TF-IDF关键词抽取接口
    tfidf = analyse.extract_tags
    # 基于TF-IDF算法进行关键词抽取
    keywords = tfidf(text,allowPOS=['n','ns','v','a','ad'])
    print('tfidf提取关键词：')
    # 输出抽取出的关键词
    tfidf_keywords=[]
    for keyword in keywords[:key_num]:
        tfidf_keywords.append(keyword)
    tfidf_keyword=' '.join(tfidf_keywords) #以空格分隔各关键信息
    print(tfidf_keyword)
    return tfidf_keywords

def get_count(cut_words,save_path):
    word_counts = collections.Counter(cut_words)  # 对分词做词频统计
    word_counts_top = word_counts.most_common(1000)  # 获取最高频的词
    print(word_counts_top)
    word_data={}
    for index,word in enumerate(word_counts_top):
        word_data[index]={'word':word[0],'num':word[1]}
    data = pd.DataFrame(word_data).T
    data.to_excel(save_path, index=None,encoding='utf-8-sig')
    return word_data
def main():
    """主程序"""
    tf_idf_words = []
    filename='data/sight_comment.xlsx'
    data=pd.read_excel(filename)
    comments=data['content']
    for comment in comments:
        comment=comment.replace('\n','')
        comment = comment.replace('纳木错', '纳木措')
        print('评论为：{}'.format(comment))
        num=int(len(comment)/2)
        tfidf_keyword=tf_idf(comment,num)
        tf_idf_words+=tfidf_keyword
    get_count(tf_idf_words,'result/tfidf_feature.xlsx')

if __name__ == '__main__':
    main() #程序入口