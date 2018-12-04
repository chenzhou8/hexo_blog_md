---
title: leetcode-240搜索二维矩阵2
date: 2017-04-18 21:37:54
categories: leetcode
tags: leetcode
cover_img: http://qiniucdn.timilong.com/1543288437866.jpg
description: leetcode上第240题搜索二维矩阵2的题解。
---

![tu](http://qiniucdn.timilong.com/1543288437866.jpg)

## search_a_2d_matrix_1

```python

#! /usr/bin/python3
# coding: utf-8

"""
Descript:
    Write an efficient algorithm that searches for a value in an m * n matrix. This matrix has the following properties:
    Integers in each row are sorted from left to right.
    The first integer of each row is greater than the last integer of the previous row.

Example:
    
    Consider the following matrix:
        [
          [1,   3,  5,  7],
          [10, 11, 16, 20],
          [23, 30, 34, 50]
        ]
    Given target = 3, return true.

"""
class Solution(object):
    def searchMatrix(self, matrix, target):
        """
        matrix: <List[List[int]]>
        target: <int>
        solution: 二分查找
        """
        if not matrix or target is None:
            return False

        m, n = len(matrix), len(matrix[0])  # m行n列
        low, high = 0, m * n - 1
        
        while low <= high:
            mid = (low + high) / 2  
            num = matrix[mid / n][mid % n]

            if num == target:
                return True
            elif num < target:
                low = mid + 1
            else:
                high = mid - 1
        
        return False
```

## search_a_2d_matrix_2

```python

#! /usr/bin/python3
# coding: utf-8

"""
Descript:
    Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:
        Integers in each row are sorted in ascending from left to right.
        Integers in each column are sorted in ascending from top to bottom.

Example:
    Consider the following matrix:
    [
      [1,   4,  7, 11, 15],
      [2,   5,  8, 12, 19],
      [3,   6,  9, 16, 22],
      [10, 13, 14, 17, 24],
      [18, 21, 23, 26, 30]
    ]

    Given target = 5, return true.
    Given target = 20, return false.
"""

class Solution(object):
    def searchMatrix(self, matrix, target):
        """
        matrix: <List[List[int]]>
        target: <int>
        solution: 复杂度: O(m+n)
        """
        if not matrix or not target:
            return False

        i, j = 0, len(matrix[0]) - 1
        while i < len(matrix) and j >= 0:
            if matrix[i][j] == target:
                return True
            if matrix[i][j] < target:
                i += 1
            else:
                j -= 1
        return False
```
