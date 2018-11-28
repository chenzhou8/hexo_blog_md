---
title: leetcode-93复原IP地址
date: 2018-07-09 11:26:14
tags: leetcode
categories: leetcode
cover_img: http://qiniucdn.timilong.com/1543387776398.png
description: 给定一个只包含数字的字符串，复原它并返回所有可能的 IP 地址格式。
---

## 题目
```
给定一个只包含数字的字符串，复原它并返回所有可能的 IP 地址格式。

示例:

输入: "25525511135"
输出: ["255.255.11.135", "255.255.111.35"]
```

## 解题
```
# 解题思路:
   回溯法: 看到所有的组合相关的题目，一般都是用回溯。 

   回溯 + 深度优先搜索 + 剪枝
```
## 代码
```python
class Solution(object):
    def restoreIpAddresses(self, s):
        """
        :type s: str
        :rtype: List[str]
        """
        res = list()
        self.dfs(s, list(), res)
        return res

    def dfs(self, s, path, res):
        if len(s) > (4 - len(path)) * 3:
            return
        if not s and len(path) == 4:
            res.append('.'.join(path))
            return
        for i in range(min(3, len(s))):
            curr = s[:i+1]
            if (curr[0] == '0' and len(curr) >= 2) or int(curr) > 255:
                continue
            self.dfs(s[i+1:], path + [s[:i+1]], res)
```

