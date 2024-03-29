---
title: leetcode-85最大矩形
date: 2018-10-04 21:46:00
tags: leetcode
cover_img: http://qiniucdn.timilong.com/1543288414205.jpg
feature_img:
description: leetcode85最大矩形题解.
keywords: leetcode
categories: leetcode
---

![tu](http://qiniucdn.timilong.com/1543288414205.jpg)

## 题目描述

给定一个仅包含 0 和 1 的二维二进制矩阵，找出只包含 1 的最大矩形，并返回其面积。

示例:

输入:
[
  ["1", "0", "1", "0", "0"],
  ["1", "0", "1", "1", "1"],
  ["1", "1", "1", "1", "1"],
  ["1", "0", "0", "1", "0"]
]
输出: 6

## 解题代码
> 思路 1

参考大神[sikp](https://leetcode.com/problems/maximal-rectangle/discuss/122456/Easiest-solution-build-on-top-of-leetcode84)的解法

首先我们可以看看 leetcode 第84题，然后你就会发现，这道题可以直接使用84题的解法来做。

我们可以从matrix的第一行开始往下进行，然后每次都做出一个heights列表，找出当前的最大area，最终找到最后一行，可以得到最终的最大area。

伪代码可以这样写：
```python
class Solution(object):
    def maximalRectangle(self, matrix):
        """
        :type matrix: List[List[str]]
        :rtype: int
        """
        if not matrix or not matrix[0]:
            return 0

        # for each cell with value=1, we look upward (north), the number of continuous '1' is the height of cell
        heights = [0] * len(matrix[0])
        res, cur_max_area = -1
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    heights[j] = 0
                else:
                    heights[j] += 1

            cur_max_area = yourLeetCode84Funtion(heights)
            res = max(cur_max_area, res)

        return res
```

最终代码就是：

```python
class Solution(object):
    def maximalRectangle(self, matrix):
        """
        :type matrix: List[List[str]]
        :rtype: int
        """
        if not matrix or not matrix[0]:
            return 0
        heights = [0] * len(matrix[0])
        area = 0
        for row in matrix:
            for col_num, item in enumerate(row):
                # for each cell with value=1, we look upward (north), the number of continuous '1' is the height of cell
                heights[col_num] = heights[col_num] + 1 if item == '1' else 0
            area = max(area, self.largestRectangleArea(heights))
        print(heights)
        return area
    
    
    def largestRectangleArea(self, heights):
        left_stack, right_stack = [], []
        left_indexes, right_indexes = [-1] * len(heights), [len(heights)] * len(heights)
        
        for i in range(len(heights)):
            while left_stack and heights[i] < heights[left_stack[-1]]:
                right_indexes[left_stack.pop()] = i 
            left_stack.append(i)
        
        for i in range(len(heights)-1, -1, -1):
            while right_stack and heights[i] < heights[right_stack[-1]]:
                left_indexes[right_stack.pop()] = i
            right_stack.append(i)
            
        res = 0
        for i in range(len(heights)):
            area = heights[i] * (right_indexes[i] - left_indexes[i] - 1)
            res = max(res, area)
        return res
```

