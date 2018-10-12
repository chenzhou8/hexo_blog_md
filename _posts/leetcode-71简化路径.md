---
title: leetcode-71简化路径
date: 2018-10-09 09:26:21
tags: leetcode
cover_img:
feature_img:
description: 给定一个文档 (Unix-style) 的完全路径，请进行路径简化。
keywords: leetcode
categories: leetcode
---

## 题目描述
```
给定一个文档 (Unix-style) 的完全路径，请进行路径简化。

例如，
path = "/home/", => "/home"
path = "/a/./b/../../c/", => "/c"

边界情况:

你是否考虑了 路径 = "/../" 的情况？
在这种情况下，你需返回 "/" 。
此外，路径中也可能包含多个斜杠 '/' ，如 "/home//foo/" 。
在这种情况下，你可忽略多余的斜杠，返回 "/home/foo" 。
```

## 解题方案
时间复杂度: O(N^2)
空间复杂度: O(1)

非常简单的模拟题，利用一个栈来储存当前的路径。

用 "/" 将输入的全路径分割成多个部分，对于每一个部分循环处理：
如果为空或者 "." 则忽略，如果是 "..", 则出栈顶部元素（如果栈为空则忽略），其他情况直接压入栈即可。

```
class Solution(object):
    def simplifyPath(self, path):
        """
        :type path: str
        :rtype: str
        """
        stack = []
        for part in path.split("/"):
            if part and part != ".": # 如果为空或者 "." 则忽略
                if part == "..":
                    if stack:
                        stack.pop()
                else:
                    stack.append(part)
        if not stack:
            return "/"
        else:
            return "/" + "/".join(stack)
```
