#-*-coding:utf-8 -*-
import pickle
import io
from os import path
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#创建stopword list
def stopwordslist(filepath):  
    stopwords = [line.strip() for line in io.open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords  

def make_worldcloud(file_path):
    jieba.add_word('少女心')
    jieba.add_word('颜值')
    jieba.del_word('男主')
    jieba.del_word('女主')
    text_from_file_with_apath = io.open(file_path,'r',encoding='UTF-8').read()
    wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=False)#精确模式
    # wl_space_split = " ".join(wordlist_after_jieba)
    # print(wl_space_split)
    backgroud_Image = plt.imread('./dou1.jpg')
    # print('loaded ipg！')

    '''set wordcloud mode'''
    #stopwords = STOPWORDS.copy()
    # stopwords = set(STOPWORDS)
    stopwords = stopwordslist('./stopwords.txt')  # 这里加载停用词的路径  
    # stopwords.add("哈哈")
    # stopwords.add("就是")
    # stopwords.add("电视剧")
    # stopwords.add("男主")
    # stopwords.add("女主")
    # stopwords.add("还是")#单项添加
    # stopwords.update([u'哈哈', u'就是', u'男主', u'女主', u'还是', u'电视剧'])#多项添加

    outstr = ''  
    for word in wordlist_after_jieba:  
        if word not in stopwords:  
            if word != '\t':  
                outstr += word  
                outstr += " "  
    print outstr

    wc = WordCloud(
        width=1024,
        height=768,
        background_color='white',# 设置背景颜色
        mask=backgroud_Image,# 设置背景图片
        font_path='/Library/Fonts/华文仿宋.ttf',  # 设置中文字体，若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        max_words=300, # 设置最大现实的字数
        #stopwords=stopwords,# 设置停用词
        #stopwords=STOPWORDS.add('男主'),# 设置停用词
        random_state=50,# 设置有多少种随机生成状态，即有多少种配色方案
    )
    #wc.generate_from_text(wl_space_split)#开始加载文本
    wc.generate_from_text(outstr)
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)#字体颜色为背景图片的颜色
    plt.imshow(wc)# 显示词云图
    plt.axis('off')# 是否显示x轴、y轴下标
    plt.show()#显示
    # 获得模块所在的路径的
    d = path.dirname(__file__)
    wc.to_file(path.join(d, "test.jpg"))
    print('word cloud!')

make_worldcloud('./comments.txt')