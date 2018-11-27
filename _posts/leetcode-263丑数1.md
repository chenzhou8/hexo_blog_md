---
title: leetcode-263丑数1
date: 2017-05-30 21:37:54
categories: leetcode
tags: leetcode
cover_img: http://qiniucdn.timilong.com/154328843058.jpg
---

## Description
```
Description:
    Write a program to check whether a given number is an ugly number.
    Ugly numbers are positive numbers whose prime factors only include 2, 3, 5

```

## Example
```
Example:
    6, 8 are ugly while 14 is not ugly since it includes another prime factor 7.
    Note that 1 is typically treated as an ugly number.

```

## Solution
```
class Solution(object):
    def isUgly(self, num):
        """
        :type num: int
        :rtype: bool
        """
        # 方法1
        if num <= 0:
            return False
        for x in [2, 3, 5]:
            while num % x == 0:
                num /= x
        return num == 1
        """ 方法2
        const_ugly = [2, 3, 5]
        if num == 1:
            return True
        result = []
        def prime(num):
            start = 2
            while start**2 <= num:
                while not num % start:
                    yield start 
                    num = num // start
                start += 1
            if num > 1:
                yield num
        result = list(prime(num))
        print(result)
        if result:
            for item in result:
                if item not in const_ugly:
                    return False
            if result.pop() in const_ugly:
                return True
        return False
        """

        """ 方法3: 笨方法, 会超时
        if num == 1 or num == 2 or num == 3 or num == 4 or num == 5:
            return True
        result = []
        for j in range(int(num/2)+1):
            for i in range(2, num):
                temp = num % i
                if temp == 0:
                    result.append(i)
                    num = num // i
                    break
        if len(result) == 0:
            return False
        else:
            result.append(num)

        for item in result:
            if item not in const_ugly:
                return False
        if result[-1] in const_ugly:
            return True
        # 判断质因数是否仅仅包含2,3,5中的一部分或者所有
        """
solution = Solution()
print(solution.isUgly(214797179))
print(solution.isUgly(14))
print(solution.isUgly(-2147483648))

```
