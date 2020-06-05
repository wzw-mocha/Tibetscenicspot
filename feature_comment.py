#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2020/2/1 10:54
#@Author  :花神庙
#@email  :m201871632@hust.edu.cn
#@FileName: extract_comment.py
#@Software: PyCharm

import os
import jieba
import pandas as pd

# 获取评价指标词典
def get_dict():
    filename='dict/关键指标.xlsx'  #指标文件路径
    data=pd.read_excel(filename)  #读取文件
    groups=data.groupby(['一级元素'])  #按指标分组
    keyword_dict={}
    for group,group_data in groups:
        second_groups=group_data.groupby(['二级元素'])
        second_dict={}
        for second_index,second_data in second_groups:
            keywords=list(second_data['指标特征关键词'])[0].split('、')  #获取指标关键词
            second_dict[second_index]=keywords  #将关键词和指标一一对应，保存在字典里
        keyword_dict[group]=second_dict
    return keyword_dict  #返回关键字字典
# 分句
def split_sentence(text, punctuation_list='!?。！？～'):
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
# 提取评论数据
def extract_comment():
    keyword_dict = get_dict()  #获取关键字字典
    print(keyword_dict)
    filename = 'data/sight_comment.xlsx'  #评论文件路径
    savepath = 'result/指标关键词文本.xlsx'  #保存文件路径
    data = pd.read_excel(filename)  #获取评论数据
    print(data)
    all_index = 0
    result = {}
    for index in data.index:
        index_data = data.iloc[index]  #按行读取数据
        index_data = dict(index_data)  #转为字典格式
        content = index_data['content']  #评论内容
        content = str(content)  #转为sting格式
        sentences=split_sentence(content)
        for sentence in sentences:
            words = jieba.lcut(sentence)    #将文本jieba分词
            for i in keyword_dict:
                for j in keyword_dict[i]:
                    keywords = keyword_dict[i][j]  #指标对应的关键词
                    for keyword in keywords:  #遍历关键词
                        if keyword in words:  #如果关键词在评论里，则保存评论
                            result[all_index] = {
                                'id': index_data['id'], 'user_name': index_data['user_name'],
                                'content': sentence,'score':index_data['score'],
                                'date':index_data['date'],'sight_name':index_data['sight_name'],
                                 'first_class': i,'second_class':j, 'keyword': keyword}
                            all_index += 1  #序号加一
                            break
    result = pd.DataFrame(result).T  #数据转为Dataframe格式
    print(result)
    result = result[['id', 'user_name', 'content', 'score', 'date', 'sight_name', 'first_class','second_class', 'keyword']]
    result.to_excel(savepath, index=None, encoding='utf-8')  #保存数据

def main():
    extract_comment()  #提取评价语句

if __name__=='__main__':
    main()