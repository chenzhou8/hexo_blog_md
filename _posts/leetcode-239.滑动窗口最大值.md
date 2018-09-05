---
title: leetcode-239.滑动窗口最大值 
date: 2017-06-23 10:07:37
tags: 堆
---

# 描述
```
给定一个数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。
你只可以看到在滑动窗口 k 内的数字。滑动窗口每次只向右移动一位。

返回滑动窗口最大值。

示例:

输入: nums = [1, 3, -1, -3, 5, 3, 6, 7], 和 k = 3

输出: [3, 3, 5, 5, 6, 7] 

解释: 

  滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7

注意：
    你可以假设 k 总是有效的，1 ≤ k ≤ 输入数组的大小，且输入数组不为空。
```

# 解题
```
class Solution(object):
    def maxSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
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
```


# 时间较少的解法(参考)
```
class Solution(object):
	def maxSlidingWindow(self, nums, k):
		"""
		:type nums: List[int]
		:type k: int
		:rtype: List[int]
		"""
		if not nums or len(nums) == 0:
			return []

		if k == 1:
			return nums

		result = []
		max_idx = 0
		max_val = 0
		for start in xrange(0, len(nums)-k+1):
			if start == 0:
				max_idx, max_val = self.getMax(nums, start, k)
				result.append(max_val)
			else:
				if max_idx < start:
					# 刚划出去的是最大的, 那就需要重新找
					max_idx, max_val = self.getMax(nums, start, k)
				else:
					# 刚划出去的不是最大的，只需要对比划进来的就好
					if max_val < nums[start+k-1]:
						max_val = nums[start+k-1]
						max_idx = start+k-1

				result.append(max_val)

		return result


	def getMax(self, nums, start, k):

		max_idx = start
		max_val = nums[start]
		for i in xrange(start+1, start+k):
			if nums[i] > max_val:
				max_val = nums[i]
				max_idx = i
		return max_idx, max_val
```
