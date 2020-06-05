
import collections # 词频统计库
import numpy as np # numpy数据处理库
import jieba
from jieba import posseg as pseg
import wordcloud # 词云展示库
from PIL import Image # 图像处理库
import matplotlib.pyplot as plt # 图像展示库
import matplotlib as mpl
import pandas as pd
mpl.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号

jieba.load_userdict('dict/user_dict.txt')
def read_lines(filename):
    fp = open(filename,'r', encoding='utf-8')
    lines = []
    for line in fp.readlines():
        line = line.strip()
        lines.append(line)
    fp.close()
    return lines

def cut_word(paragraph):
    stop_word=read_lines('./Sentiment_dict/emotion_dict/stop_words.txt')
    wordsCutList = []  # 分词列表
    words=[]
    flags=[]
    paragraphToWords = pseg.cut(str(paragraph))  # 分词
    for word, flag in paragraphToWords:
        if (word != ' ' and word != '' and len(word)>1 and word not in stop_word and flag in ['n','ns','nr','v']):
            wordsCutList.append((word,flag))  # 加入分词列表
            words.append(word)
            flags.append(flag)
    print('分割句子为：', words)
    return words
def get_count(cut_words,save_path):
    word_counts = collections.Counter(cut_words)  # 对分词做词频统计
    word_counts_top = word_counts.most_common(200)  # 获取最高频的词
    print(word_counts_top)  # 输出检查
    word_data={}
    for index,word in enumerate(word_counts_top):
        word_data[index]={'word':word[0],'num':word[1]}
    data = pd.DataFrame(word_data).T
    data=data[['word','num']]
    data.to_excel(save_path, index=None,encoding='utf-8-sig')
    return word_counts
def draw_cloud_pic(cut_words,save_path,savename):
    word_counts=get_count(cut_words,save_path)
    # 词频展示
    mask = np.array(Image.open('cloud.jpg'))  # 定义词频背景
    wc = wordcloud.WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体格式
        background_color='white',  # 背景颜色
        mask=mask,  # 设置背景图
        max_words=80,  # 最多显示词数
        max_font_size=100,  # 字体最大值
        min_font_size=5
    )
    wc.generate_from_frequencies(word_counts)  # 从字典生成词云
    wc.to_file(savename)  # 图片保存
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    # plt.show()  # 显示图像

# 统计名词词频，并绘制云图
def draw_noun_pic(data):
    contents = data['content']
    cut_words = []
    for content in contents:
        content = content.replace('纳木错', '纳木措')
        cut_words += cut_word(content)
    draw_cloud_pic(cut_words, 'result/词频统计.xlsx', 'result/云图.png')

def main():
    filename='data/sight_comment.xlsx'
    data=pd.read_excel(filename)
    draw_noun_pic(data)  #统计名词词频，并绘制云图


if __name__=='__main__':
    main()