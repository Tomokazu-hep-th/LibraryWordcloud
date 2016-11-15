# -*- coding: utf-8 -*-
import pandas as pd
import MeCab
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from tqdm import tqdm
from time import sleep
from langdetect import detect
import sys
import codecs
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
import argparse

#To use this code, you need to install pandas, mecab-python3,
#pillow(PIL), matplotlib, WordCloud, langdetect and tqdm.


parser=argparse.ArgumentParser(description='word cloud generator')
parser.add_argument("-i", nargs="?", dest="input_file_name",
                        default="data/takeout201410-201609UTF-8.csv", metavar="filename",
                        help="input csv file name.")
parser.add_argument("--col", nargs="?", dest="column",
                        default='書誌情報', metavar="columnname",
                        help="column name of input file to use analyze.")
parser.add_argument("--sday", nargs="?", dest="startday",action="store",type=int,
                        default=20141001, metavar="startday",
                        help="the first day of dayrange.")
parser.add_argument("--eday", nargs="?", dest="endday",action="store",type=int,
                        default=20141002, metavar="endday",
                        help="the last day of dayrange.")
parser.add_argument("--lan", nargs="?", action="store", dest="lan",
                        default="non", metavar="lanuage", help="language of book title")
parser.add_argument("--langlist", action="store_true", dest="language_list",
                        help="show language list of available")
parser.add_argument("--mjr", nargs="?", action="store", dest="major",
                        default="non", metavar="major", help="major of the person who takeout books")
#parser.add_argument("--mjrlist", action="store_true", dest="major_list",
#                        help="show major list of available")
parser.add_argument("--grd", nargs="?", action="store", dest="grade",
                        default="non", metavar="grade", help="grade of the person who takeout books")
args=parser.parse_args()

if args.language_list:
    print('af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, '+
          'he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, '+
          'pa, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, '+
          'ur, vi, zh-cn, zh-tw')
    sys.exit()

def mjr_extract(data_frame,major):
    try:
        ln=len(data_frame)
        columnlist=data_frame.columns
        for i in tqdm(range(ln)):
            if i==0:
                new_df=pd.DataFrame(index=[-1],columns=columnlist)
                if (str(data_frame.loc[i,'所属名称'])==str(major)):
                    d=data_frame.ix[[i],columnlist]
                    new_df=pd.concat([new_df,d],ignore_index=True)
            else:
                if (str(data_frame.loc[i,'所属名称'])==str(major)):
                    d=data_frame.ix[[i],columnlist]
                    new_df=pd.concat([new_df,d],ignore_index=True)
            sleep(0.01)
        dfln=new_df.drop(0)
        dfln=dfln.reset_index(drop=True)
        return dfln
    except:
        print('There is no major entry.')
        sys.exit()


def grd_extract(data_frame,grade):
    try:
        ln=len(data_frame)
        columnlist=data_frame.columns
        for i in tqdm(range(ln)):
            if i==0:
                new_df=pd.DataFrame(index=[-1],columns=columnlist)
                if (str(data_frame.loc[i,'学年'])==str(grade)):
                    d=data_frame.ix[[i],columnlist]
                    new_df=pd.concat([new_df,d],ignore_index=True)
            else:
                if (str(data_frame.loc[i,'学年'])==str(grade)):
                    d=data_frame.ix[[i],columnlist]
                    new_df=pd.concat([new_df,d],ignore_index=True)
            sleep(0.01)
        dfln=new_df.drop(0)
        dfln=dfln.reset_index(drop=True)
        return dfln
    except:
        print('There is no grade entry.')
        sys.exit()

def language_extract(data_frame,language):
    try:
        if language=='ja':
            ln=len(data_frame)
            columnlist=data_frame.columns
            for i in tqdm(range(ln)):
                if i==0:
                    new_df=pd.DataFrame(index=[-1],columns=columnlist)
                    if (data_frame.loc[i,'和洋区分名称']=='和書'):
                        d=data_frame.ix[[i],columnlist]
                        new_df=pd.concat([new_df,d],ignore_index=True)
                else:
                    if (data_frame.loc[i,'和洋区分名称']=='和書'):
                        d=new_df.ix[[i],columnlist]
                        new_df=pd.concat([new_df,d],ignore_index=True)
                sleep(0.01)
        else:
            ln=len(data_frame)
            columnlist=data_frame.columns
            for i in tqdm(range(ln)):
                if i==0:
                    new_df=pd.DataFrame(index=[-1],columns=columnlist)
                    if (detect(data_frame.loc[i,args.column])==language)&(data_frame.loc[i,'和洋区分名称']=='洋書'):
                        d=data_frame.ix[[i],columnlist]
                        new_df=pd.concat([data_frame,d],ignore_index=True)
                else:
                    if (detect(data_frame.loc[i,args.column])==language)&(data_frame.loc[i,'和洋区分名称']=='洋書'):
                        d=data_frame.ix[[i],columnlist]
                        new_df=pd.concat([data_frame,d],ignore_index=True)
                sleep(0.01)
        new_df=new_df.drop(0)
        new_df=new_df.reset_index(drop=True)
        return new_df
    except:
        print('There is no language entry.')
        sys.exit()

def mcb(text):
    m = MeCab.Tagger ("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    m.parse('')
    node=m.parseToNode(text)
    keywords=[]
    while node:
        if node.feature.split(",")[0] == u"名詞":
            keywords.append(node.surface)
        node=node.next
    return keywords

def format_text(text):
    if '/'or'; :'or'-- Heinl' in text:
        pattern = re.compile("./.")
        matchedlist = pattern.split(text)
        ftext=matchedlist[0]
        if '/'or'; :'or'-- Heinl' in text:
            pattern = re.compile(".; :.")
            matchedlist = pattern.split(ftext)
            ftext=matchedlist[0]
            if '/'or'; :'or'-- Heinl' in text:
                pattern = re.compile(".-- Heinl.")
                matchedlist = pattern.split(ftext)
                ftext=matchedlist[0]
    else:
        ftext=text
    return ftext

def create_wordcloud(text):
    fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.otf"
    # ストップワードの設定
    stop_words = ['The','the','of','and','cm','in','ため','to','from','for','on','at','with','der','und']
    wordcloud = WordCloud(background_color="white",font_path=fpath, width=900, height=500, \
                          stopwords=set(stop_words)).generate(text)
    plt.figure(figsize=(15,12))
    plt.imshow(wordcloud)
    plt.axis("off")
    if args.grade=='non':
        if args.major=='non':
            if args.lan=='non':
                plt.savefig("output/wordcloud"+str(args.startday)+'-'+str(args.endday)+".pdf")
            else:
                plt.savefig("output/"+args.lan+"/wordcloud"+str(args.startday)+'-'+str(args.endday)+args.lan+".pdf")
        else:
            if args.lan=='non':
                plt.savefig("output/"+args.major+'/wordcloud'+str(args.startday)+'-'+str(args.endday)+str(args.major)+".pdf")
            else:
                plt.savefig('output/'+args.major+'/'+args.lan+"/wordcloud"+str(args.startday)+'-'+str(args.endday)+str(args.major)+args.lan+".pdf")
    else:
        if args.major=='non':
            if args.lan=='non':
                plt.savefig("output/"+str(args.grade)+'/'+"wordcloud"+str(args.startday)+'-'+str(args.endday)+str(args.grade)+".pdf")
            else:
                plt.savefig("output/"+str(args.grade)+'/'+args.lan+"/wordcloud"+str(args.startday)+'-'+str(args.endday)+str(args.grade)+args.lan+".pdf")
        else:
            if args.lan=='non':
                plt.savefig("output/"+args.major+'/'+str(args.grade)+'/wordcloud'+str(args.startday)+'-'+str(args.endday)+str(args.major)+str(args.grade)+".pdf")
            else:
                plt.savefig('output/'+args.major+'/'+str(args.grade)+'/'+args.lan+"/wordcloud"+str(args.startday)+'-'+str(args.endday)+str(args.major)+str(args.grade)+args.lan+".pdf")

    #plt.show()


#csvデータの読み込み
df=pd.DataFrame(pd.read_csv(args.input_file_name,encoding='utf-8'))

#指定期間の抽出
df1=df.rename(columns={'貸出日': 'takeoutday'})
dfex=df[(df1.takeoutday>=args.startday)&(df1.takeoutday<=args.endday)]
dfex=dfex.reset_index(drop=True)

if args.grade=='non':
    pass
else:
    dfex=grd_extract(dfex,args.grade)

if args.major=='non':
    pass
else:
    dfex=mjr_extract(dfex,args.major)

if args.lan=='non':
    pass
else:
    dfex=language_extract(dfex,args.lan)



#名詞の抽出
lnln=len(dfln)
for i in tqdm(range(lnln)):
    if i==0:
        lis=mcb(format_text(dfln.loc[i,args.column]))
    else:
        lis.extend(mcb(format_text(dfln.loc[i,args.column])))
    sleep(0.01)
df2=pd.DataFrame({'key':lis})
df2rank=df2['key'].value_counts()




#抽出結果の保存
if args.grade=='non':
    if args.major=='non':
        if args.lan=='non':
            if os.path.exists('output'):
                df2.to_csv('output/keywords'+str(args.startday)+'-'+str(args.endday)+'.csv',encoding='utf-8')
                df2rank.to_csv('output/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking.csv',encoding='utf-8')
            else:
                os.mkdir('output')
                df2.to_csv('output/keywords'+str(args.startday)+'-'+str(args.endday)+'.csv',encoding='utf-8')
                df2rank.to_csv('output/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking.csv',encoding='utf-8')
        else:
            if os.path.exists('output/'+args.lan):
                df2.to_csv('output/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+args.lan+'.csv',encoding='utf-8')
                df2rank.to_csv('output/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+args.lan+'_ranking'+args.lan+'.csv',encoding='utf-8')
            else:
                if os.path.exists('output'):
                    pass
                else:
                    os.mkdir('output')
                os.mkdir('output/'+args.lan)
                df2.to_csv('output/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+args.lan+'.csv',encoding='utf-8')
                df2rank.to_csv('output/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking'+args.lan+'.csv',encoding='utf-8')
    else:
        if args.lan=='non':
            if os.path.exists('output/'+args.major):
                df2.to_csv('output/'+args.major+'/keywords'+str(args.startday)+'-'+str(args.endday)+'.csv',encoding='utf-8')
                df2rank.to_csv('output/'+args.major+'/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking.csv',encoding='utf-8')
            else:
                if os.path.exists('output'):
                    pass
                else:
                    os.mkdir('output')
                if os.path.exists('output/'+args.major):
                    pass
                else:
                    os.mkdir('output/'+args.major)
                df2.to_csv('output/'+args.major+'/keywords'+str(args.startday)+'-'+str(args.endday)+'.csv',encoding='utf-8')
                df2rank.to_csv('output/'+args.major+'/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking.csv',encoding='utf-8')
        else:
            if os.path.exists('output/'+args.major+'/'+args.lan):
                df2.to_csv('output/'+args.major+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+args.lan+'.csv',encoding='utf-8')
                df2rank.to_csv('output/'+args.major+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+args.lan+'_ranking'+args.lan+'.csv',encoding='utf-8')
            else:
                if os.path.exists('output'):
                    pass
                else:
                    os.mkdir('output')
                if os.path.exists('output/'+args.major):
                    pass
                else:
                    os.mkdir('output/'+args.major)
                if os.path.exists('output/'+args.major+'/'+args.lan):
                    pass
                else:
                    os.mkdir('output/'+args.major+'/'+args.lan)
                df2.to_csv('output/'+args.major+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+args.lan+'.csv',encoding='utf-8')
                df2rank.to_csv('output/'+args.major+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking'+args.lan+'.csv',encoding='utf-8')
else:
    if args.major=='non':
        if args.lan=='non':
            if os.path.exists('output'):
                if os.path.exists('output/'+str(args.grade)):
                    pass
                else:
                    os.mkdir('output/'+str(args.grade))
            else:
                os.mkdir('output')
                os.mkdir('output/'+str(args.grade))
            df2.to_csv('output/'+str(args.grade)+'/keywords'+str(args.grade)+str(args.startday)+'-'+str(args.endday)+'.csv',encoding='utf-8')
            df2rank.to_csv('output/'+str(args.grade)+'/keywords'+str(args.grade)+str(args.startday)+'-'+str(args.endday)+'_ranking.csv',encoding='utf-8')
        else:
            if os.path.exists('output'):
                if os.path.exists('output/'+str(args.grade)):
                    if os.path.exists('output/'+str(args.grade)+'/'+args.lan):
                        pass
                    else:
                        os.mkdir('output/'+str(args.grade)+'/'+args.lan)
                else:
                    os.mkdir('output/'+str(args.grade))
                    os.mkdir('output/'+str(args.grade)+'/'+args.lan)
            else:
                os.mkdir('output')
                os.mkdir('output/'+str(args.grade))
                os.mkdir('output/'+str(args.grade)+'/'+args.lan)
            df2.to_csv('output/'+str(args.grade)+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+str(args.grade)+args.lan+'.csv',encoding='utf-8')
            df2rank.to_csv('output/'+str(args.grade)+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking'+str(args.grade)+args.lan+'.csv',encoding='utf-8')
    else:
        if args.lan=='non':
            if os.path.exists('output'):
                if os.path.exists('output/'+str(args.major)):
                    if os.path.exists('output/'+str(args.major)+'/'+str(args.grade)):
                        pass
                    else:
                        os.mkdir('output/'+str(args.major)+'/'+str(args.grade))
                else:
                    os.mkdir('output/'+str(args.major))
                    os.mkdir('output/'+str(args.major)+'/'+str(args.grade))
            else:
                os.mkdir('output')
                os.mkdir('output/'+str(args.major))
                os.mkdir('output/'+str(args.major)+'/'+str(args.grade))
            df2.to_csv('output/'+str(args.major)+'/'+str(args.grade)+'/keywords'+str(args.startday)+'-'+str(args.endday)+str(args.major)+str(args.grade)+'.csv',encoding='utf-8')
            df2rank.to_csv('output/'+str(args.major)+'/'+str(args.grade)+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking'+str(args.major)+str(args.grade)+'.csv',encoding='utf-8')
        else:
            if os.path.exists('output'):
                if os.path.exists('output/'+str(args.major)):
                    if os.path.exists('output/'+str(args.major)+'/'+str(args.grade)):
                        if os.path.exists('output/'+str(args.major)+'/'+str(args.grade)+'/'+str(args.lan)):
                            pass
                        else:
                            os.mkdir('output/'+str(args.major)+'/'+str(args.grade)+'/'+str(args.lan))
                    else:
                        os.mkdir('output/'+str(args.major)+'/'+str(args.grade))
                        os.mkdir('output/'+str(args.major)+'/'+str(args.grade)+'/'+str(args.lan))
                else:
                    os.mkdir('output/'+str(args.major))
                    os.mkdir('output/'+str(args.major)+'/'+str(args.grade))
                    os.mkdir('output/'+str(args.major)+'/'+str(args.grade)+'/'+str(args.lan))
            else:
                os.mkdir('output')
                os.mkdir('output/'+str(args.major))
                os.mkdir('output/'+str(args.major)+'/'+str(args.grade))
                os.mkdir('output/'+str(args.major)+'/'+str(args.grade)+'/'+str(args.lan))
            df2.to_csv('output/'+args.major+'/'+str(args.grade)+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+args.major+str(args.grade)+args.lan+'.csv',encoding='utf-8')
            df2rank.to_csv('output/'+args.major+'/'+str(args.grade)+'/'+args.lan+'/keywords'+str(args.startday)+'-'+str(args.endday)+'_ranking'+args.major+str(args.grade)+args.lan+'.csv',encoding='utf-8')

#WordCloudの作成
text=' '.join(lis)
create_wordcloud(text)
