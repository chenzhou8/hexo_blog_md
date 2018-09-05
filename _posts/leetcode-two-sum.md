---
title: leetcode-'two-sum'
date: 2017-04-10 21:37:54
categories: leetcode
tags: leetcode
---

## Description
```
Description:
   Given an array of integers, return indices of the two numbers such that they add up to a specific target.
   You may assume that each input would have exactly one solution, and you may not use the same element twice.

```

## Example
```
Example:
    Given nums = [2, 7, 11, 15], target = 9,
    Because nums[0] + nums[1] = 2 + 7 = 9,
    return [0, 1].

```

## Solution
```
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
            时间复杂度: O(n)
            target - nums[i] = i
            将当前target-num的差值作为key, 当前i作为value, 存储为字典
            循环遍历一次
            如果nums[i] in dict则返回[dict[nums[i]], i]
            否则继续循环, 直到结束返回None
        """
        length = len(nums)
        if length <=1: 
            return False
        buff_dict = {}
        for i in range(length):
            if nums[i] in buff_dict:
                print(i, nums[i], buff_dict)
                return [buff_dict[nums[i]], i]
            else:
                buff_dict[target - nums[i]] = i
                print(i, nums[i], buff_dict)

        pass

solution = Solution()
nums = [2, 7, 9, 11]
target = 9
print(solution.twoSum(nums, target))
```
