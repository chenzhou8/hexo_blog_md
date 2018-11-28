---
title: leetcode-04两个排序数组的中位数
date: 2017-06-23 10:07:11
tags: leetcode
categories: leetcode
cover_img: http://qiniucdn.timilong.com/1543387765563.jpg
description: 给定两个大小为 m 和 n 的有序数组 nums1 和 nums2 。 请找出这两个有序数组的中位数。要求算法的时间复杂度为 O(log (m+n)) 。
---

## 题目
```
给定两个大小为 m 和 n 的有序数组 nums1 和 nums2 。

请找出这两个有序数组的中位数。要求算法的时间复杂度为 O(log (m+n)) 。

示例 1:

    nums1 = [1, 3]
    nums2 = [2]

    中位数是 2.0

示例 2:
    nums1 = [1, 2]
    nums2 = [3, 4]

    中位数是 (2 + 3)/2 = 2.5
```

## 题解
```python
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        nums = sorted(nums1 + nums2)
        length = len(nums)
        mid = length // 2
        if length == 0:
            return 0
        if length % 2 != 0:
            return nums[mid]
        else:
            return (nums[mid] + nums[mid-1]) / 2.0
```
