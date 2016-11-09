# 図書館貸出書籍に基づくキーワードランキングとWord Cloudの作成コード

図書館から取得したexcelデータをcsv化して、エンコーディングをutf-8にしたものが/dataの中に格納されており、これを読み込んで動作します。

指定期間、指定学部、指定言語の貸出書籍からキーワードランキングとそれに基づくword cloudを作成することができます。

(注意)本体はkeywords3.pyのpythonコードです。cmd.pyはkeywords3.pyを連続的に作動させる為に書いたコマンドで、
コンピュータのマルチコアを16スレッド並列に作動させます。自分用です。スペックの低いパソコンだと落ちるかもしれないので、使わない方がいいと思います。
どうしても使いたい場合は、cmd.py内の
```
Parallel(n_jobs=16)([delayed(main)(i) for i in range(l)])
```
の16を、自分のパソコンのスペックに対応した数に直して使ってください。


**動作要件**:
このプログラムはpython3を想定して書かれています。また、動作には以下のモジュールのインストールが必要です。
- pandas
- mecab-python3
- pillow(PIL)
- matplotlib
- WordCloud
- langdetect
- tqdm

これらをインストールするにはシェルスクリプト上で、以下のコマンドを実行してください。
```
pip install pandas
pip install mecab-python3
pip install pillow
pip install matplotlib
pip install WordCloud
pip install langdetect
pip install tqdm

```

Basic usage:
```
>>>python keywords3.py -h
usage: keywords3.py [-h] [-i [filename]] [--col [columnname]]
                    [--sday [startday]] [--eday [endday]] [--lan [lanuage]]
                    [--langlist] [--mjr [major]]

word cloud generator

optional arguments:
  -h, --help          show this help message and exit
  -i [filename]       input csv file name.
  --col [columnname]  column name of input file to use analyze.
  --sday [startday]   the first day of dayrange.
  --eday [endday]     the last day of dayrange.
  --lan [lanuage]     language of book title
  --langlist          show language list of available
  --mjr [major]       major of the person who takeout books
```
