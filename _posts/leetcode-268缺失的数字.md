---
title: leetcode-268缺失的数字
date: 2017-01-03 21:37:54
categories: leetcode
tags: leetcode
cover_img: http://qiniucdn.timilong.com/154328840886.jpg
---

## Description
```
Description:
    Given an array containing n distinct numbers taken from 0, 1, 2, ..., n, 
    find the one that is missing from the array.
```

## Example
```
Example:
    Given nums = [0, 1, 3] return 2.
```

## Solution
```
class Solution(object):
    def missingNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # 方法1: 利用前n项和公式  n*(n+1)/2 减去sum(nums)
        return len(nums)*(len(nums)+1) // 2 - sum(nums)
        """ 方法2: 利用两集合的差值极为所求结果
        length = len(nums)
        temp_set = set([i for i in range(length+1)])
        nums_set = set(nums)
        res = list(temp_set - nums_set)
        return res[0]
        """
solution = Solution()
nums = [0, 1, 3]
print(solution.missingNumber(nums))
# output: 2
```
