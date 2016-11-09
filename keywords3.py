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
args=parser.parse_args()

if args.language_list:
    print('af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, '+
          'he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, '+
          'pa, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, '+
          'ur, vi, zh-cn, zh-tw')
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
    if args.major=='non':
        if args.lan=='non':
            plt.savefig("output/wordcloud"+str(args.startday)+'-'+str(args.endday)+".pdf")
        else:
            plt.savefig("output/"+args.lan+"/wordcloud"+str(args.startday)+'-'+str(args.endday)+args.lan+".pdf")
    else:
        if args.lan=='non':
            plt.savefig("output/"+args.major+'/wordcloud'+str(args.startday)+'-'+str(args.endday)+".pdf")
        else:
            plt.savefig('output/'+args.major+'/'+args.lan+"/wordcloud"+str(args.startday)+'-'+str(args.endday)+args.lan+".pdf")

    #plt.show()


#csvデータの読み込み
df=pd.DataFrame(pd.read_csv(args.input_file_name,encoding='utf-8'))

#指定期間の抽出
df1=df.rename(columns={'貸出日': 'takeoutday'})
dfex=df[(df1.takeoutday>=args.startday)&(df1.takeoutday<=args.endday)]
dfex=dfex.reset_index(drop=True)


#指定言語の抽出
try:
    if args.major=='non':
        if args.lan=='non':
            dfln=dfex
        else:
            if args.lan=='ja':
                ln=len(dfex)
                columnlist=df1.columns
                for i in tqdm(range(ln)):
                    if i==0:
                        dfln=pd.DataFrame(index=[-1],columns=columnlist)
                        if (dfex.loc[i,'和洋区分名称']=='和書'):
                            d=dfex.ix[[i],columnlist]
                            dfln=pd.concat([dfln,d],ignore_index=True)
                    else:
                        if (dfex.loc[i,'和洋区分名称']=='和書'):
                            d=dfex.ix[[i],columnlist]
                            dfln=pd.concat([dfln,d],ignore_index=True)
                    sleep(0.01)
            else:
                ln=len(dfex)
                columnlist=df1.columns
                for i in tqdm(range(ln)):
                    if i==0:
                        dfln=pd.DataFrame(index=[-1],columns=columnlist)
                        if (detect(dfex.loc[i,args.column])==args.lan)&(dfex.loc[i,'和洋区分名称']=='洋書'):
                            d=dfex.ix[[i],columnlist]
                            dfln=pd.concat([dfln,d],ignore_index=True)
                    else:
                        if (detect(dfex.loc[i,args.column])==args.lan)&(dfex.loc[i,'和洋区分名称']=='洋書'):
                            d=dfex.ix[[i],columnlist]
                            dfln=pd.concat([dfln,d],ignore_index=True)
                    sleep(0.01)
            dfln=dfln.drop(0)
            dfln=dfln.reset_index(drop=True)
    else:
        if args.lan=='non':
            dfln=dfex
        else:
            if args.lan=='ja':
                ln=len(dfex)
                columnlist=df1.columns
                for i in tqdm(range(ln)):
                    if i==0:
                        dfln=pd.DataFrame(index=[-1],columns=columnlist)
                        if (dfex.loc[i,'和洋区分名称']=='和書')&(dfex.loc[i,'所属名称']==args.major):
                            d=dfex.ix[[i],columnlist]
                            dfln=pd.concat([dfln,d],ignore_index=True)
                    else:
                        if (dfex.loc[i,'和洋区分名称']=='和書')&(dfex.loc[i,'所属名称']==args.major):
                            d=dfex.ix[[i],columnlist]
                            dfln=pd.concat([dfln,d],ignore_index=True)
                    sleep(0.01)
            else:
                ln=len(dfex)
                columnlist=df1.columns
                for i in tqdm(range(ln)):
                    if i==0:
                        dfln=pd.DataFrame(index=[-1],columns=columnlist)
                        if (detect(dfex.loc[i,args.column])==args.lan)&(dfex.loc[i,'和洋区分名称']=='洋書')&(dfex.loc[i,'所属名称']==args.major):
                            d=dfex.ix[[i],columnlist]
                            dfln=pd.concat([dfln,d],ignore_index=True)
                    else:
                        if (detect(dfex.loc[i,args.column])==args.lan)&(dfex.loc[i,'和洋区分名称']=='洋書')&(dfex.loc[i,'所属名称']==args.major):
                            d=dfex.ix[[i],columnlist]
                            dfln=pd.concat([dfln,d],ignore_index=True)
                    sleep(0.01)
            dfln=dfln.drop(0)
            dfln=dfln.reset_index(drop=True)
    if len(dfln)==0:
        print('There is no book entry wrote in such a language in the date range.')
        sys.exit()
    else:
        pass
except:
    print('There is no book entry wrote in such a language in the date range.')
    sys.exit()

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


#WordCloudの作成
text=' '.join(lis)
create_wordcloud(text)
