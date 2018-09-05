---
title: leetcode-'first-bad-version'
date: 2017-03-20 21:37:54
categories: leetcode
tags: leetcode
---

## Description
```
Description:
    给定一个API: isBadVersion()
    要求: 在需要编写的firstBadVersion()中最少次数调用该API得到第一个bad version

```

## Example
```
Example:
    Suppose you have n versions [1, 2, ..., n] 
    and you want to find out the first bad one, which causes all the following ones to be bad.

```

## Solution
```
"""
Solution:
    时间复杂度: O(log(n))
    空间复杂度: O(1)
    二分查找到最先被坏掉的版本号
"""


"""
# The isBadVersion API is already defined for you.
# @param version, an integer
# @return a bool
# def isBadVersion(version):
"""


class Solution(object):
    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """
        left, right = n, 1 
        while left < right:
            mid = int(left + (right - left)/2)
            if isBadVersion(mid):
                right = mid  # mid是，表示目标值在mid左侧，则更新right=mid，继续
            else:
                left = mid + 1  # mid不是，表示目标值在mid右侧，更新left=mid+1，继续
        return left  # 返回左侧较小值

```
