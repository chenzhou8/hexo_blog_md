title: leetcode-242有效的字母异位词
date: 2017-03-18 21:37:54
categories: leetcode
tags: leetcode
cover_img: http://qiniucdn.timilong.com/1543288440507.jpg
---
## 描述
```
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的一个字母异位词。

示例 1:

输入: s = "anagram", t = "nagaram"
输出: true
示例 2:

输入: s = "rat", t = "car"
输出: false
说明:
你可以假设字符串只包含小写字母。

进阶:
如果输入字符串包含 unicode 字符怎么办？你能否调整你的解法来应对这种情况？
```

## different_ways_to_add_parentheses

```

#! /usr/bin/python3
# coding: utf-8

"""
Descriptions:
    Given two strings s and t, write a function to determine if t is an anagram of s.  

Example: 
    s = "anagram", t = "nagaram", return true.  
    s = "rat", t = "car", return false.  

Note: 
    You may assume the string contains only lowercase alphabets.

Follow up:
    What if the inputs contain unicode characters? How would you adapt your solution to such case?

"""

class Solution(object):
    def isAnagram(self, s, t):
        """
        s: <str>
        t: <str>
        return: <bool>
        """
        res_s = {}
        res_t = {}

        for item in s:
            res_s[item] = res_s.get(item, 0) + 1

        for item in t:
            res_t[item] = res_t.get(item, 0) + 1

        return res_s == res_t

    def isAnagram1(self, s, t):
        return sorted(s) == sorted(t)

solution = Solution()

s = "anagram"

t = "ganaamr"
print(solution.isAnagram(s, t))

```
