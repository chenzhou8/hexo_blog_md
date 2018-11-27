title: leetcode-258各位相加
date: 2017-03-25 21:37:54
categories: leetcode
tags: leetcode
cover_img: http://qiniucdn.timilong.com/1543288403900.jpg
---

## Description
```
Description:
    Given a non-negative integer num, repeatedly add all its digits until the result has only one digit.
```

## Example
```
Example:
    Given num = 38, the process is like: 3 + 8 = 11, 1 + 1 = 2. Since 2 has only one digit, return it.
```

## Solution
```
class Solution(object):
    def addDigits(self, num):
        """
        num: <int>
        return: <int>
        """
        if num == 0:
            return 0
        else:
            return (num-1) % 9 + 1  # 9是区分最大的一位数


solution = Solution()
print(solution.addDigits(38))
```
