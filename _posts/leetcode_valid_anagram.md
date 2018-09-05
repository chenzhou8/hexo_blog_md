title: leetcode-'valid_anagram'
date: 2017-03-18 21:37:54
categories: leetcode
tags: leetcode
---

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
