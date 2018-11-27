---
title: leetcode-18四数之和1
date: 2018-07-06 08:05:31
tags: leetcode
categories: leetcode
cover_img: http://qiniucdn.timilong.com/1543288400281.jpg
---

# 题目描述
```
给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，
使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。

注意：

    答案中不可以包含重复的四元组。

示例：

    给定数组 nums = [1, 0, -1, 0, -2, 2]，和 target = 0。

满足要求的四元组集合为：
    [
      [-1,  0, 0, 1],
      [-2, -1, 1, 2],
      [-2,  0, 0, 2]
    ]
```

<!--more-->

# 解答
```
class Solution(object):
    def fourSum(self, num, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        numLen, res, d = len(num), set(), {}
        if numLen < 4: 
            return []
        
        num.sort()
        for p in range(numLen):
            for q in range(p+1, numLen): 
                if num[p]+num[q] not in d:
                    d[num[p] + num[q]] = [(p,q)]
                else:
                    d[num[p] + num[q]].append((p, q))
                    
        for i in xrange(numLen):
            for j in xrange(i+1, numLen - 2):
                T = target - num[i] - num[j]
                if T in d:
                    for k in d[T]:
                        if k[0] > j: 
                            res.add((num[i], num[j], num[k[0]], num[k[1]]))
        return [list(i) for i in res]
```
