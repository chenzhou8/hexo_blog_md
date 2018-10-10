---
title: leetcode-273整数转换成英文表示
date: 2017-02-03 21:37:54
categories: leetcode
description: leetcode-273整数转换成英文表示题解
tags: leetcode
---

## Description
```
将非负整数转换为其对应的英文表示。可以保证给定输入小于 231 - 1 。

示例 1:

输入: 123
输出: "One Hundred Twenty Three"
示例 2:

输入: 12345
输出: "Twelve Thousand Three Hundred Forty Five"
示例 3:

输入: 1234567
输出: "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
示例 4:

输入: 1234567891
输出: "One Billion Two Hundred Thirty Four Million Five Hundred Sixty Seven Thousand Eight Hundred Ninety One"

```

## Solution
```
class Solution(object):
    def numberToWords(self, num):
        """
        :type num: int
        :rtype: str
        """
        num1_dict = {
            0: 'Zero', 1: 'One', 2: 'Two',
            3: 'Three', 4: 'Four', 5: 'Five',
            6: 'Six', 7: 'Seven', 8: 'Eight',
            8: 'Eight', 9: 'Nine', 10: 'Ten',
            11: 'Eleven', 12: 'Twelve', 13: 'Thirteen',
            14: 'Fourteen', 15: 'Fifteen', 16: 'Sixteen',
            17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen',
            20: 'Twenty', 30: 'Thirty', 40: 'Forty',
            50: 'Fifty', 60: 'Sixty', 70: 'Seventy',
            80: 'Eighty', 90: 'Ninety',
        }
        def int2Str(num):
            if num >= 1000000000:
                int_n = num // 1000000000
                return int2Str(int_n) + " Billion" + int2Str(num - int_n * 1000000000)
            elif num >= 1000000:
                int_n = num // 1000000
                return " " + int2Str(int_n) + " Million" + int2Str(num - int_n * 1000000)
            elif num >= 1000:
                int_n = num // 1000
                return " " + int2Str(int_n) + " Thousand" + int2Str(num - int_n * 1000)
            elif num >= 100:
                int_n = num // 100
                return " " + num1_dict[int_n] + " Hundred" + int2Str(num - int_n * 100)
            elif num >= 20:
                int_n = num // 10 
                return " " + num1_dict[int_n * 10] + int2Str(num - int_n*10)
            elif num >= 1:
                return " " + num1_dict[num] 
            else:
                return ""
        if num in num1_dict: 
            return num1_dict[num]
        else:
            return int2Str(num).lstrip().replace('  ', ' ') 
solution = Solution()
print(solution.numberToWords(1))
print(solution.numberToWords(12))
print(solution.numberToWords(123))
print(solution.numberToWords(1234))
print(solution.numberToWords(12345))
print(solution.numberToWords(123456))
print(solution.numberToWords(1234567))
print(solution.numberToWords(12345678))
print(solution.numberToWords(123456789))
print(solution.numberToWords(1234567890))
```
