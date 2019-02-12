---
title: python3-枚举类型
cover_img: http://qiniucdn.timilong.com/1544683429223.jpg
date: 2019-02-12 10:21:48
tags: python
feature_img:
description: 枚举类型本身是一个类，枚举类型由单例模式实现，实例化无意义.
keywords: python
categories: python
---

![cover_img](http://qiniucdn.timilong.com/1544683429223.jpg)

## 枚举类型

> 枚举类型本身是一个类，枚举类型由单例模式实现，实例化无意义

## 注意
> 不允许两个标签的名称相同
> 若两个标签的对应值相同，则第二个标签为第一个标签的别名

## 使用方法

```python
from enum import Enum


class VIP(Enum):
    # 继承于Enum
    YELLOW = 1
    GREEN = 2
    BLACK = 3
    RED = 4


class VIP1(Enum):
    YELLOW = 1
    GREEN = 2
    BLACK = 3
    RED = 4


# 获取枚举类型
print(VIP['GREEN'])  # VIP.GREEN

# 获取枚举的值
print(VIP.YELLOW.value)  # 1

# 获取枚举的名字
print(VIP.YELLOW.name)  # YELLOW

# 枚举类型的比较 不可进行大小比较，可进行等值比较和is身份比较
result = VIP.GREEN == VIP.BLACK
print(result)  # False

# 进行is比较
result = VIP.GREEN is VIP.GREEN
print(result)  # True

# 进行等值比较
result = VIP.GREEN == VIP1.GREEN
print(result)  # False

# 使用数值访问枚举类型
a = 1
print(VIP(a))  # VIP.YELLOW

# 枚举的遍历1
for v in VIP:
    print(v)

# VIP.YELLOW
# VIP.GREEN
# VIP.BLACK
# VIP.RED


# 枚举的遍历2
for v in VIP.__members__:
    print(v)

# YELLOW
# GREEN
# BLACK
# RED

```
