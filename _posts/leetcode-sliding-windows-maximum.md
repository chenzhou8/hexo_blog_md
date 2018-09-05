---
title: leetcode-'missing-number'
date: 2017-02-13 21:37:54
categories: leetcode
tags: leetcode
---

## Description
```
Description:
    Given an array nums, 
    there is a sliding window of size k which is moving from the very left of the array to the very right. 
    You can only see the k numbers in the window. 
    Each time the sliding window moves right by one position.
```

## Example
```
Example:
    Given nums = [1,3,-1,-3,5,3,6,7], and k = 3.

        Window position                Max
        ---------------               -----
        [1  3  -1] -3  5  3  6  7       3
         1 [3  -1  -3] 5  3  6  7       3
         1  3 [-1  -3  5] 3  6  7       5
         1  3  -1 [-3  5  3] 6  7       5
         1  3  -1  -3 [5  3  6] 7       6
         1  3  -1  -3  5 [3  6  7]      7

    Therefore, return the max sliding window as [3,3,5,5,6,7].
```

## Solution
```
class Solution(object):
    def maxSlidingWindow(self, nums, k):
        """
        nums: <List[int]>
        k: <int>
        return: <List[int]>
        """
        nums_length = len(nums)
        count = nums_length - k + 1
        res = []
        if nums_length == 0:
            return res
        
        for i in range(count):
            tmp_list = nums[i:i+k]
            res.append(max(tmp_list))
        return res

solution = Solution()
nums = [1, 3, -1, -3, 5, 3, 6, 7]
print(solution.maxSlidingWindow(nums, k=3))
nums = [1, 2]
print(solution.maxSlidingWindow(nums, k=1))
```
