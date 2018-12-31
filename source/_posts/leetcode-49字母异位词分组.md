---
title: leetcode-49字母异位词分组
date: 2018-09-30 22:05:27
tags: leetcode
cover_img: http://qiniucdn.timilong.com/1543387773264.jpg
feature_img:
description: https://leetcode-cn.com/problems/group-anagrams/题解
keywords: leetcode
categories: leetcode
---

![tu](http://qiniucdn.timilong.com/1543387773264.jpg)

> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

## 题目描述
```
给定一个字符串数组，将字母异位词组合在一起。字母异位词指字母相同，但排列不同的字符串。

示例:

输入: ["eat", "tea", "tan", "ate", "nat", "bat"],
输出:
[
  ["ate","eat","tea"],
  ["nat","tan"],
  ["bat"]
]
说明：

所有输入均为小写字母。
不考虑答案输出的顺序。
```

## 题解
每一个字符串都先排个序看看是不是一样，这样更好判断
```
class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        mapx = {}
        for i in strs:
            tmp = ''.join(sorted(list(i)))
            if tmp in mapx:
                mapx[tmp].append(i)
            else:
                mapx[tmp] = [i]
        return mapx.values()
```

