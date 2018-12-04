title: Linux-awk命令
date: 2017-07-29 14:06:39
categories: Linux
tags: Linux
description: awk是一个强大的文本分析工具，相对于grep的查找，sed的编辑，awk在其对数据分析并生成报告时，显得尤为强大。
cover_img: http://qiniucdn.timilong.com/1543735251861.jpg
---

![tu](http://qiniucdn.timilong.com/1543735251861.jpg)

## 简介
awk是一个强大的文本分析工具，相对于grep的查找，sed的编辑，awk在其对数据分析并生成报告时，显得尤为强大。
简单来说awk就是把文件逐行的读入，以空格为默认分隔符将每行切片，切开的部分再进行各种分析处理。

awk有3个不同版本: awk、nawk和gawk，未作特别说明，一般指gawk，gawk 是 AWK 的 GNU 版本。

awk其名称得自于它的创始人 Alfred Aho 、Peter Weinberger 和 Brian Kernighan 姓氏的首个字母。
实际上 AWK 的确拥有自己的语言: AWK 程序设计语言， 三位创建者已将它正式定义为“样式扫描和处理语言”。
它允许您创建简短的程序，这些程序读取输入文件、为数据排序、处理数据、对输入执行计算以及生成报表，还有无数其他的功能。

## 语法

1. 语法如下
```
    awk '{pattern + action}' {filenames}
```



2. 例子
```
1. 假设last -n 5的输出如下:
[root@www ~]# last -n 5              <==仅取出前五行
root     pts/1   192.168.1.100  Tue Feb 10 11:21   still logged in
root     pts/1   192.168.1.100  Tue Feb 10 00:46 - 02:28  (01:41)
root     pts/1   192.168.1.100  Mon Feb  9 11:41 - 18:30  (06:48)
dmtsai   pts/1   192.168.1.100  Mon Feb  9 11:41 - 11:41  (00:00)
root     tty1                   Fri Sep  5 14:09 - 14:10  (00:01)

2. 如果只是显示最近登录的5个帐号:
[root@www ~]# last -n 5 | awk  '{print $1}'
root
root
root
dmtsai
root
```

## 详细教程

[linux-awk常见用法](http://www.cnblogs.com/ggjucheng/archive/2013/01/13/2858470.html)

