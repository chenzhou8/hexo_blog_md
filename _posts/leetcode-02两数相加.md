---
title: leetcode-02两数相加
date: 2017-02-23 21:37:54
categories: leetcode
tags: leetcode
---

## Description
```
给定两个非空链表来表示两个非负整数。位数按照逆序方式存储，它们的每个节点只存储单个数字。将两数相加返回一个新的链表。

你可以假设除了数字 0 之外，这两个数字都不会以零开头。

示例：

输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
输出：7 -> 0 -> 8
原因：342 + 465 = 807
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
