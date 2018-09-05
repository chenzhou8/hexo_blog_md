---
title: python-三方开源库hashids
date: 2018-08-09 15:05:16
tags: python
---

[转载自知乎专栏: 码洞](https://zhuanlan.zhihu.com/p/32671455)

## hashids介绍

Hashids是一个非常小巧的开源库，它用来把数字编码成一个随机字符串。
不同于md5这种算法这种单向映射，Hashids除了编码还会解码。

拿论坛来说，一般帖子在数据库里的id都是顺序递增的，但是你可能不想在url上直接把id暴露出来，以免爬虫直接遍历id爬取你的内容，给你带来损失。
那现在你就可以使用Hashids把这个id搞乱，让它失去顺序性，无法直接遍历，这样就可以直接提高了爬虫的门槛。

著名的Youtube网站就是这么做的。

## 安装

```
 pip install hashids
```

<!--more-->


## 具体使用

```
import hashids

hasher = hashids.Hashids(salt="yoursecretkey")

# encode
hasher.encode(123456)
# 输出: '3Pl8o'

# decode
hasher.decode('3Pl8o')
# 输出: (123456, )

# 多个数字同事编码
hasher.encode(1234546, 789012, 345678)
# 输出: '3Pl8oibxv5uNDoB'

# 解码
hasher.decode('3Pl8oibxv5uNDoB')
# 输出: (1234546, 789012, 345678)
```

## 缺点

```
对 salt 依赖太严重，通一salt下的encode结果必定相同，这是无法避免的
```
