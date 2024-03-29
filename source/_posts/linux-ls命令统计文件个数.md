---
title: linux-ls命令统计文件个数
date: 2018-09-07 15:49:20
tags: Linux
keywords: Linux
categories: Linux
feature_img:
cover_img: http://qiniucdn.timilong.com/1543736935686.jpg
description: Linux下有三个命令：ls、grep、wc。通过这三个命令的组合可以统计目录下文件及文件夹的个数。
---

![tu](http://qiniucdn.timilong.com/1543736935686.jpg)

> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

Linux下有三个命令：<code>ls</code>、<code>grep</code>、<code>wc</code>。通过这三个命令的组合可以统计目录下文件及文件夹的个数。

### 统计当前目录下文件的个数（不包括目录）
```shell
$ ls -l | grep "^-" | wc -l
```

### 统计当前目录下文件的个数（包括子目录）
```shell
$ ls -lR | grep "^-" | wc -l
```

### 查看某目录下文件夹(目录)的个数（包括子目录）
```shell
$ ls -lR | grep "^d" | wc -l
```

命令解析：
```shell
$ ls -l
# 长列表输出该目录下文件信息(注意这里的文件是指目录、链接、设备文件等)。
# 每一行对应一个文件或目录，ls -lR是列出所有文件，包括子目录。

$ grep "^-"
# 过滤ls的输出信息，只保留一般文件，只保留目录是grep "^d"。

$ wc -l
# 统计输出信息的行数，统计结果就是输出信息的行数，一行信息对应一个文件，所以就是文件的个数。
```
