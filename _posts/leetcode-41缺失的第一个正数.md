---
title: leetcode-41缺失的第一个正数
date: 2018-09-22 22:36:17
tags: leetcode
cover_img: http://qiniucdn.timilong.com/1543387768401.jpg
feature_img:
description: 题目来源自https://leetcode-cn.com/problems/first-missing-positive/
keywords: leetcode
categories: leetcode
---

![tu](http://qiniucdn.timilong.com/1543387768401.jpg)

> 题目链接: [缺失的第一个正数](https://leetcode-cn.com/problems/first-missing-positive/)

## 题目描述

给定一个未排序的整数数组，找出其中没有出现的最小的正整数。

```
示例 1:
输入: [1,2,0]
输出: 3

---

示例 2:

输入: [3,4,-1,1]
输出: 2

---

示例 3:

输入: [7,8,9,11,12]
输出: 1
```

## 说明
你的算法的时间复杂度应为O(n)，并且只能使用常数级别的空间。

## 解题思路
先将数字都放到应该出现的位置，然后通过一次循环，可查看位置, 如果该位置没有对应对应的数字, 则返回

## python实现
```python
class Solution(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 1
        
        nums_len = len(nums)
        for i in range(nums_len):
            while nums[i] > 0 and nums[i] <= len(nums) and nums[nums[i]-1] != nums[i]:
                nums[nums[i]-1], nums[i] = nums[i], nums[nums[i]-1]

        for i in range(nums_len):
            if nums[i] != i + 1:
                return i + 1

        return nums_len + 1
```

## 题解中最快的解法
```python
class Solution:
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        '''
        for num in nums:
        	if num <= 0:
        		nums.remove(num)
        '''
        nums = [i for i in nums if i > 0]
        nums.sort() 
        
        if nums == []:
            return 1
        if nums[0] > 1:
            return 1
        elif len(nums) == 1:
            return 2
        elif len(nums) > 1:
            for i in range(1,len(nums)):
                if nums[i] - nums[i-1] > 1:
                    return nums[i-1]+1
                else:
                    pass
            return nums[len(nums)-1]+1
```
