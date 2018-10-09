---
title: leetcode-'Add Two Numbers'
date: 2017-02-23 21:37:54
categories: leetcode
tags: leetcode
---

## Description
```
Description:
    You are given two non-empty linked lists representing two non-negative integers. 
    The digits are stored in reverse order and each of their nodes contain a single digit. 
    Add the two numbers and return it as a linked list.
```

## Example
```
Note:
    You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example:
    Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
    Output: 7 -> 0 -> 8
```

## Solution
```
Explain:
    2->4->3: 243  reverse: 342
    5->6->4: 564  reverse: 465
    result: 807   return: 7->0->8
    直接相加不需要reverse

Solution:
    本题的思路很简单，按照小学数学中学习的加法原理从末尾到首位，对每一位对齐相加即可。
    技巧在于如何处理不同长度的数字，以及进位和最高位的判断。
    这里对于不同长度的数字，我们通过将较短的数字补0来保证每一位都能相加。
    递归写法的思路比较直接，即判断该轮递归中两个ListNode是否为null。

        全部为null时，返回进位值
        有一个为null时，返回不为null的那个ListNode和进位相加的值
        都不为null时，返回 两个ListNode和进位相加的值

    存储时是reverse方向, 个位数在前
"""
```

## Code
```
class Solution(object):
    def __init__(self, x):
        self.val = x
        self.next = None

    def addTwoNumbers(self, l1, l2):
        """
        l1: <ListNode>
        l2: <ListNode>
        return: <ListNode>
        """
        carray = 0  # 进位
        res = n = ListNode(0)
        while l1 or l2 or carray:
            val1 = val2 = 0
            if l1:
                val1 = l1.val
                l1 = l1.next  # 更改指针
            if l2:
                val2 = l2.val
                l2 = l2.next  # 更改指针
            # carry: 商, 进位:要么等于0要么等于1, val为余数，要么为余数，要么为val1+val2+carray
            carray, val = divmod(val1+val2+carray, 10)  
            n.next = ListNode(val)  # 存入val(reverse, 个位数在前)
            n = n.next  # 更改next指针
        return res.next
```
