---
title: leetcode-'h-index1'
date: 2017-03-10 21:37:54
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
    从低到高进行排列，如果(某篇论文的引用次数) >= (论文总数 - 当前论文序号)，则(总长度-当前序号)就是h指数
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
        """
        citations.sort()
        length = len(citations)

        for i in range(length):
            if citations[i] >= length - i:
                return length - i
        return 0
        """ 方法2
        citations.sort(reverse=True)
        for i in range(len(citations)):
            if i >= citations[i]:
            return i
        return len(citations)
        """

```
