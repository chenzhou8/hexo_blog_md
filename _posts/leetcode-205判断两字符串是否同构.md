---
title: leetcode-205.同构字符串
date: 2018-07-09 11:26:35
tags: leetcode
categories: leetcode
description: 给定两个字符串 s 和 t，判断它们是否是同构的。

---

# 题目
```
给定两个字符串 s 和 t，判断它们是否是同构的。

如果 s 中的字符可以被替换得到 t ，那么这两个字符串是同构的。

所有出现的字符都必须用另一个字符替换，同时保留字符的顺序。两个字符不能映射到同一个字符上，但字符可以映射自己本身。

示例 1:
    输入: s = "egg", t = "add"
    输出: true

示例 2:
    输入: s = "foo", t = "bar"
    输出: false

示例 3:
    输入: s = "paper", t = "title"
    输出: true

说明:
你可以假设 s 和 t 具有相同的长度。
```

# 解题
```
用字典(hashMap), 将字符串s与字符串t简历映射关系
```

```
#! /usr/bin/python3
# coding: utf-8

def is_isomorphic(str_s, str_t):
    print(str_s, str_t)

    len_s, len_t = len(str_s), len(str_t)
    if len_s != len_t:
        return False

    tmp_dict = dict()
    for inx in range(len_s):
        if str_s[inx] not in tmp_dict:
            tmp_dict[str_s[inx]] = str_t[inx]
        else:
            if tmp_dict[str_s[inx]] != str_t[inx]:
                return False
    return tmp_dict

def check_str(result, str_s, str_t):
    return len(result) == len(set(str_s)) and len(result) == len(set(str_t))

str_s = "aabbcc"
str_t = "ddeeff"

result = is_isomorphic(str_s, str_t)
print(check_str(result, str_s, str_t))

```
