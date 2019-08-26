---
title: aliyun-挂载nas网络盘命令
cover_img: 'http://qiniucdn.timilong.com/1551520931257.jpg'
date: 2019-08-19 17:11:58
tags: 运维
feature_img:
description: 挂载阿里云NAS网络盘的一个命令
keywords: 运维
categories: 运维
---

![cover_img](http://qiniucdn.timilong.com/1551520931257.jpg)

## 命令如下
```python
mount -t nfs -o vers=4 xxxxxx.nas.aliyuncs.com:/ /root/nas
```
