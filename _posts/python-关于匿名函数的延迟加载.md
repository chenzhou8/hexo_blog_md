---
title: python-关于匿名函数的延迟加载
date: 2018-09-18 11:35:19
tags: python
cover_img:
feature_img:
description: Python里面的延迟加载用得非常多，其主要思想是延迟所要引入类的实例化，节省一些初始化所需要的时间和空间。
keywords: python
categories: python
---

> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

### 题目
执行下面一段代码，输出结果是什么?

```
f = [lambda x: x * i for i in range(7)]

for item in f[:-1]:
    print(item(1), end=" ")

```

### 输出结果
```
6 6 6 6 6 6
```

### 解析f
当我们打印f时，我们在打印什么?
```
>>> f
[<function <listcomp>.<lambda> at 0x10176d048>, <function <listcomp>.<lambda> at 0x10176d0d0>, <function <listcomp>.<lambda> at 0x10176d158>, <function <listcomp>.<lambda> at 0x10176d1e0>, <function <listcomp>.<lambda> at 0x10176d268>, <function <listcomp>.<lambda> at 0x10176d2f0>, <function <listcomp>.<lambda> at 0x10176d378>]

>>> len(f)
7
```
可以看到，返回的是长度为7，元素为匿名函数的list , 到这里没什么问题（通过列表生成式[x for x in range(n)], 只不过这里的x换成了一个lambda匿名函数，n=7）。

### 解析结果
lambda表达式当中绑定的i变量是外层的i变量，循环结束之后，这个变量变成了6([i for i in range(7)] i的最后一个取值是6)，所以所有的lambda表达式当中都引用的是这个6，而不是创建lambda表达式时当时的值。

单从实现的结果看, `f = [lambda x: x * i for i in range(7)]`的结果是和`f = [lambda x: x * 6] * 7 `产生的结果是等同的。但是在内存地址引用上，完成不是一回事情，这点需要注意.
```
>>> f = [lambda x: x * 6] * 7
>>> f
[<function <lambda> at 0x10c88e578>, <function <lambda> at 0x10c88e578>, <function <lambda> at 0x10c88e578>, <function <lambda> at 0x10c88e578>, <function <lambda> at 0x10c88e578>, <function <lambda> at 0x10c88e578>, <function <lambda> at 0x10c88e578>]

>>> for item in f[:-1]:
...     print(item(1))
...
6
6
6
6
6
6
>>>
```
可见是同一个内存地址，引用了7次。

### 拓展
下面一段代码会输出什么?
```
>>> f = [lambda x, i = i: x * i for i in range(7)]
>>> for item in f:
...     print(item(0), item(1), item(2), item(3), item(4), item(5), item(6), item(7), item(8))
...
```

结果输出:        
```
>>> f
[<function <listcomp>.<lambda> at 0x101a0c048>, <function <listcomp>.<lambda> at 0x101a0c0d0>, <function <listcomp>.<lambda> at 0x101a0c158>, <function <listcomp>.<lambda> at 0x101a0c1e0>, <function <listcomp>.<lambda> at 0x101a0c268>, <function <listcomp>.<lambda> at 0x101a0c2f0>, <function <listcomp>.<lambda> at 0x101a0c378>]

>>> for item in f:
...     print(item(0), item(1), item(2), item(3), item(4), item(5), item(6), item(7), item(8))
...
0 0 0 0 0 0 0 0 0
0 1 2 3 4 5 6 7 8
0 2 4 6 8 10 12 14 16
0 3 6 9 12 15 18 21 24
0 4 8 12 16 20 24 28 32
0 5 10 15 20 25 30 35 40
0 6 12 18 24 30 36 42 48
>>>
```
可以看到，使用此方法，可以有效解决延迟绑定的问题。

> 参考: CSDN: [浅析Python的闭包和延迟绑定](https://blog.csdn.net/LeVoleurDombres/article/details/69681063)
