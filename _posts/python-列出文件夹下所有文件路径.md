---
title: python-列出文件夹下所有文件名
date: 2018-07-09 18:34:41
tags: python
categories: python
cover_img: http://qiniucdn.timilong.com/154373690549.jpg
description: python-列出文件夹下所有文件名

---

# 题目
```
描述:
    给定一个文件夹的路径fpath, 请输出此文件夹下所有文件的路径，包括子文件夹中的文件路径
```

# 解答
```
#! /usr/bin/python3
# coding: utf-8

import os
rootdir = "/home/timilong/hexoBlog/source"

for parent, dirnames, filenames in os.walk(rootdir):
    for dirname in dirnames:
        print("目录名: ", dirname)

    print("\n\n")

    for filename in filenames:
        print("文件名: ", filename)
```

<!--more-->

```
目录名:  _posts
目录名:  categories
目录名:  tags
目录名:  about



文件名:  404.html
文件名:  CNAME



文件名:  变革中国.md
文件名:  世界因你不同-李开复传.md
文件名:  leetcode_valid_anagram.md
文件名:  linux-grep命令.md
文件名:  python爬虫入门3-Urllib的高级使用.md
文件名:  python爬虫实战2-爬取百度贴吧的帖子.md
文件名:  loadRunner入门教程.md
文件名:  linux-awk命令.md
文件名:  浏览器缓存机制剖析.md
文件名:  leetcode-sliding-windows-maximum.md
文件名:  doNotMakeMeThink.md
文件名:  成都卓航网络科技公司面试.md
文件名:  python爬虫入门4-URLError异常处理.md
文件名:  OS-进程调度.md
文件名:  leetcode-ugly_number_2.md
文件名:  与人交谈的艺术.md
文件名:  leetcode_single_number_1_2_3.md
文件名:  python-汉诺塔.md
文件名:  leetcode-h-index2.md
文件名:  Markdown简明语法手册.md
文件名:  leetcode_binary_tree_paths.md
文件名:  python-网络服务器.md
文件名:  python爬虫入门1-基础.md
文件名:  面试-链表归并.md
文件名:  python-列出文件夹下所有文件路径.md
文件名:  linux-rpm包管理命令.md
文件名:  JavaScript进阶-匿名函数.md
文件名:  leetcode-四数之和1.md
文件名:  leetcode_search_a_2d_matrix_1_2.md
文件名:  vim配置-vimrc.md
文件名:  leetcode-ugly_number_1.md
文件名:  初探Ajax.md
文件名:  icourse163_org_python爬虫_教程.md
文件名:  icourse163_org_python爬虫_中国大学排名.md
文件名:  leetcode-h-index1.md
文件名:  nodejs_模块系统.md
文件名:  vim教程-基础.md
文件名:  面试-堆排序.md
文件名:  程序员从优秀到卓越.md
文件名:  python-简单的爬虫.md
文件名:  linux-日常命令.md
文件名:  leetcode-first-bad-version.md
文件名:  面试-两个有序数组归并.md
文件名:  三体-第一部.md
文件名:  沃兹传-与苹果一起疯狂——读书笔记.md
文件名:  python-函数.md
文件名:  csAppLab4PerflabHandout优化方案.md
文件名:  leetcode-判断两字符串是否同构.md
文件名:  python爬虫入门6-正则表达式.md
文件名:  leetcode-missing-number.md
文件名:  html中将非a标签变成超链接.md
文件名:  linux-sed命令.md
文件名:  node的4大优势.md
文件名:  明朝那些事.md
文件名:  leetcode-add-two-numbers.md
文件名:  deepin2015加载windows7启动项.md
文件名:  MarkDown语法.md
文件名:  面试-字符查找.md
文件名:  linux-ifconfig命令.md
文件名:  leetcode-two-sum.md
文件名:  leetcode-各位相加得个位数是多少.md
文件名:  mySql-点分十进制.md
文件名:  面试-二叉树遍历.md
文件名:  面试-快速排序.md
文件名:  面试-实现一个装饰器计算函数运算时间.md
文件名:  面试-二分查找.md
文件名:  eisoo前端面试题.md
文件名:  面试-计算机网络.md
文件名:  浪潮之巅.md
文件名:  leetcode-integer-to-english-words.md
文件名:  python爬虫入门2-Urllib的基本使用.md
文件名:  mySql-linux下基本操作.md
文件名:  Linus_只是为了好玩.md
文件名:  重说中国近代史-读后感.md
文件名:  常用的hexo命令.md
文件名:  leetcode_add_digits.md
文件名:  python爬虫入门5-cookie的使用.md
文件名:  python-函数式编程.md
文件名:  python爬虫实战1-爬取糗事百科-md.md
文件名:  leetcode-93.复原IP地址.md
文件名:  JavaScript-DOM获取元素的三种方法.md
文件名:  linux-杀死进程.md
文件名:  MacTalk-人生元编程.md
文件名:  pyMysql学习1.md
文件名:  icourse163_org_python爬虫_题目.md
文件名:  Markdown高级语法手册.md









文件名:  index.md

```
