---
title: leetcode-43字符串相乘
date: 2018-10-01 16:37:19
tags: leetcode
cover_img: http://qiniucdn.timilong.com/1543387770478.jpg
feature_img:
description: leetcode-43字符串相乘的题解.
keywords: leetcode
categories: leetcode
---

![tu](http://qiniucdn.timilong.com/1543387770478.jpg)

## 题目描述
给定两个以字符串形式表示的非负整数 num1 和 num2，返回 num1 和 num2 的乘积，它们的乘积也表示为字符串形式。

示例 1:
```
输入: num1 = "2", num2 = "3"
输出: "6"
示例 2:

输入: num1 = "123", num2 = "456"
输出: "56088"
说明：
```

num1 和 num2 的长度小于110。
num1 和 num2 只包含数字 0-9。
num1 和 num2 均不以零开头，除非是数字 0 本身。
不能使用任何标准库的大数类型（比如 BigInteger）或直接将输入转换为整数来处理。

## 解题方案


### 思路 1
直接一位一位的搞，最后转string, 但是考虑到这样kennel最后str2int(num1) * str2int(num2)是一个极大的数字可能会导致溢出，所以有了后面的思路2

```python
class Solution(object):
    def multiply(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        def str2int(num):
            res = 0
            for i in range(len(num)-1, -1, -1):
                res += int(num[i]) * pow(10, len(num)-1-i)
            return res
        return str(str2int(num1) * str2int(num2))
```

### 思路 2


参考了别人的思路：

1. m位的数字乘以n位的数字的结果最大为m+n位：
    * 999*99 < 1000*100 = 100000，最多为3+2 = 5位数。
2. 先将字符串逆序便于从最低位开始计算。


```python
class Solution(object):
    def multiply(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        lookup = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9} # 节省查找时间，避免无休止使用ord函数来得到数字
        if num1 == '0' or num2 == '0':
            return '0'
        num1, num2 = num1[::-1], num2[::-1]
        
        tmp_res = [0 for i in range(len(num1)+len(num2))]
        for i in range(len(num1)):
            for j in range(len(num2)):
                tmp_res[i+j] += lookup[num1[i]] * lookup[num2[j]]

        res = [0 for i in range(len(num1)+len(num2))]
        for i in range(len(num1)+len(num2)):
            res[i] = tmp_res[i] % 10
            if i < len(num1)+len(num2)-1:
                tmp_res[i+1] += tmp_res[i]/10 
        return ''.join(str(i) for i in res[::-1]).lstrip('0')  # 去掉最终结果头部可能存在的‘0’
```

觉得这样写才是最容易理解的，看一个具体的例子:
```
input: num1, num2 = '91', '91'
tmp_res = [1,18,81,0]
res = [1,8,2,8]

最终返回 "8281"

要注意最终返回头部可能会有‘0’，所以我们用lstrip去除一下
```


