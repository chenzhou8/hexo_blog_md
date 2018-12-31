---
title: leetcode-46全排列
date: 2018-10-02 22:54:32
tags: leetcode
cover_img: http://qiniucdn.timilong.com/1543387773264.jpg
feature_img:
description: 给定一个没有重复数字的序列，返回其所有可能的全排列。
keywords: leetcode
categories: leetcode
---

![tu](http://qiniucdn.timilong.com/1543387773264.jpg)

## 题目描述

```
给定一个没有重复数字的序列，返回其所有可能的全排列。

示例:

输入: [1,2,3]
输出:
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]
```

## 题解

```python
# 每次取一个作为prefix, 剩下的继续做permutation，然后连接起来加入res中

class Solution(object):
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if len(nums) == 0:
            return []
        if len(nums) == 1:
            return [nums]
        res = []
        for i in range(len(nums)):
            prefix = nums[i]
            rest = nums[:i] + nums[i+1:]
            for j in self.permute(rest):
                res.append([prefix]+j)
        return res
```
