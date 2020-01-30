# Sighan2013/2014/2015原始纠错数据提取

## 依赖

python2.7

regex、bs4、opencc_python_reimplemented

## 原始数据

raw_data/

SIGHAN-2013 shared task on CSC: [LINK](http://ir.itc.ntnu.edu.tw/lre/sighan7csc_release1.0.zip)

SIGHAN-2014 shared task on CSC: [LINK](http://ir.itc.ntnu.edu.tw/lre/clp14csc_release1.1.zip)

SIGHAN-2015 shared task on CSC: [LINK](http://ir.itc.ntnu.edu.tw/lre/sighan8csc_release1.0.zip)

注意：

- 原始训练数据中存在一定比例的标注错误，已经进行手工纠正，因此与原始下载数据（.zip文件）存在不同。


## 提取数据

繁体

pair_data/traditional/

简体（使用opencc转换）

pair_data/simplified/

注意：

- sighan纠错任务中正确句子和错误句子的长度是一致的。

- 存在正确/错误繁体字对应同一个简体字的情况，转换成简体后有的文本错误消失了，因此简体版本的文本错误数量少于繁体版本的。