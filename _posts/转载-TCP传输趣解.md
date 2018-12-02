---
title: 转载-TCP传输趣解
date: 2018-09-19 13:36:52
tags: 计算机网络
cover_img: http://qiniucdn.timilong.com/1543736950216.jpg
feature_img:
description: 1，下载一个15K的文件，和下载一个28K的文件，时间其实几乎是一样的，但下载一个15K的文件和一个14K的文件，前者比后者耗时几乎多了一倍。这是因为一个TCP请求窗口在绝大部分情况下是1480 * 10/1024=14.45K。
keywords: 计算机网络
categories: 计算机网络
---

> 转载自:[有哪些计算机的事实，没有一定计算机知识的人不会相信？ - 猫爱吃鱼不吃耗子的回答 - 知乎](https://www.zhihu.com/question/288115796/answer/483284593)

### TCP传输大小

![TCP](http://qiniucdn.timilong.com/tcp_bao_chaungkou01.png)

### TCP慢启动
![TCP](http://qiniucdn.timilong.com/tcp_bao_chuangkou02.png)

![TCP](http://qiniucdn.timilong.com/tcp_bao_chuangkou_03.png)

### TCP包大小为1480字节
![TCP](http://qiniucdn.timilong.com/tcp_bao_chuangkou_04.png)

![TCP](http://qiniucdn.timilong.com/tcp_bao_chuangkou_06.png)


