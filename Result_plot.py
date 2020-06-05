#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2020/2/7 22:26
#@Author  :花神庙
#@email  :m201871632@hust.edu.cn
#@FileName: data_analysis.py
#@Software: PyCharm

import pandas as pd
import numpy as np
import os
import collections
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
import pyecharts.options as opts
from pyecharts.charts import Line
def draw_pie(labels,sizes,title,savepath):
    explode = (0.1,0,0)  #突出显示
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)  #绘制饼图
    plt.title(title)  #图标题
    plt.axis('equal')  # 绘制饼图为圆形
    plt.savefig(savepath)  #保存图片
    plt.close()
    # plt.show()  #图片显示
def draw_line(x,y):
    plt.figure(figsize=(10, 6), dpi=200)
    font = {
        'weight': 'normal',
        'size': 14,
    }
    plt.plot(x, y)
    plt.yticks(size=10)
    plt.xticks(size=10)
    plt.title('纳木措各月评论数', font)
    plt.ylabel('评论数', font)
    plt.xlabel('月份', font)
    plt.savefig('result/出游人数.png')
    plt.show()
def draw_bar(labels,y,title,savepath):
    x = np.arange(len(labels))  # 柱状图在横坐标上的位置
    # 列出你要显示的数据，数据的列表长度与x长度相同
    bar_width = 0.3  # 设置柱状图的宽度
    # 绘制并列柱状图
    font = {
        'weight': 'normal',
        'size': 14,
    }
    plt.figure(figsize=(12,10),dpi=200)
    plt.bar(x, y, bar_width, color='salmon', label='情感得分')
    plt.title(title,font)
    plt.legend()  # 显示图例，即label
    plt.xticks(x, labels,size=10,rotation=360, ha='center')  # 显示x坐标轴的标签,即tick_label
    plt.yticks(size=10)
    plt.savefig(savepath)
    plt.show()
def get_sentiment_labels(class_data):
    scores = class_data['sentiment']
    pos_num = len([item for item in scores if item > 0])  # 积极文本数量
    neg_num = len([item for item in scores if item < 0])  # 消极文本数量
    neu_num = len([item for item in scores if item == 0])  # 中性文本数量
    labels = ['积极文本', '消极文本', '中性文本']  # 标签
    nums = [pos_num, neg_num, neu_num]  # 数据
    mean_score=np.round(np.mean(scores),3)
    print(nums)
    return labels,nums,mean_score

def sentiment_pie(data,feature_name):
    class_groups = data.groupby([feature_name])  #按属lass进行分组
    result={}
    for class_name, class_data in class_groups:
        labels, nums,score=get_sentiment_labels(class_data)
        pos_num = nums[0]
        neg_num = nums[1]
        neu_num = nums[2]

        pos_pre = nums[0]/(sum(nums))
        neg_pre = nums[1]/(sum(nums))
        neu_pre = nums[2]/(sum(nums))

        result[class_name]={'积极文本数量':pos_num,'消极文本数量':neg_num,'中性文本数量':neu_num,'积极文本占比':pos_pre,'消极文本占比':neg_pre,'中性文本占比':neu_pre,'情感得分':score}
        draw_pie(labels,nums,'{}-文本情感分布'.format(class_name),'result/情感分析可视化图表/{}/{}-文本情感分布.png'.format(feature_name,class_name))  #绘制饼图并保存
    result=pd.DataFrame(result).T
    result.to_excel('result/情感分析可视化图表/{}-各指标情感类型统计.xlsx'.format(feature_name))
def sentiment_plot(feature_name):
    filename = 'result/情感分析结果.xlsx'
    Save_Root = 'result/情感分析可视化图表/{}'.format(feature_name)
    if not os.path.exists(Save_Root):
        os.makedirs(Save_Root)
    data = pd.read_excel(filename)
    sentiment_pie(data, feature_name)
def comment_line():
    filename = 'data/sight_comment.xlsx'
    data = pd.read_excel(filename)
    months = [date.month for date in data['date']]
    data['month'] = months
    groups = data.groupby(['month'])
    x = []
    y = []
    for month, month_data in groups:
        x.append(str(month) + '月')
        y.append(len(month_data))
    draw_line(x, y)
def sentiment_bar(feature_name):
    filename = 'result/情感分析结果.xlsx'
    data = pd.read_excel(filename)
    groups = data.groupby([feature_name])
    x = []
    y = []
    for feature, feature_data in groups:
        scores = feature_data['sentiment']
        mean_scores = np.round(np.mean(scores), 3)
        print(feature, mean_scores)
        x.append('\n'.join(feature))
        y.append(mean_scores)
    draw_bar(x, y, title='情感分类均值分布图', savepath='result/{}-情感分类均值分布图.png'.format(feature_name))
def main():
    filename = 'result/情感分析结果.xlsx'
    data=pd.read_excel(filename)
    labels, nums, score = get_sentiment_labels(data)
    draw_pie(labels, nums, '全部-文本情感分布','result/情感分析可视化图表/全部-文本情感分布.png') # 绘制饼图并保存

    feature_names=['first_class','second_class']
    for feature_name in feature_names:
        sentiment_plot(feature_name)
        sentiment_bar(feature_name)
    comment_line()


if __name__=='__main__':
    main()