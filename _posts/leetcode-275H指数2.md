---
title: leetcode-275H指数2
date: 2017-04-30 21:37:54
categories: leetcode
tags: leetcode
---

## Description
```
Description:
    h-index ，又称为h指数或h因子（h-factor），是一种评价学术成就的新方法。
    h代表“高引用次数”（high citations），一名科研人员的h指数是指他至多有h篇论文分别被引用了至少h次。
    要确定一个人的h指数非常容易，到SCI网站，查出某个人发表的所有SCI论文，让其按被引次数从高到低排列，
    往下核对，直到某篇论文的序号大于该论文被引次数，那个序号减去1就是h指数。
    or
    从低到高进行排列，如果(某篇论文的引用次数) >= (总长度 - 当前论文序号)，则(总长度-当前序号)就是h指数
    其中, citations是已升序排列的
    总结: 目标 = 引用次数 >= 序号 则length-序号即为结果
```

## Example
```
Example:
    Given citations = [3, 0, 6, 1, 5]
    which means the researcher has 5 papers in total 
        and each of them had received 3, 0, 6, 1, 5 citations respectively. 
    Since the researcher has 3 papers with at least 3 citations each 
        and the remaining two with no more than 3 citations each, his h-index is 3.
```

## Solution
```
class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        二分法
        """
        length = len(citations)
        left, right = 0, length-1
        while left <= right:
            mid = int((left+right)/2)
            if citations[mid] >= length - mid:
                right = mid - 1
            else:
                left = mid + 1
        return length - left
```
