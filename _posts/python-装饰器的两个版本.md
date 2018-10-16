---
title: python-装饰器的典型实现
date: 2018-06-23 10:08:38
tags: python
categories: python
---

## 题目

请实现装饰器log，可以计算test函数的运行时间
```
@log('excute')
def test():
    pass
```

<!--more-->

## 解答

```
import time
import functools

# 可接受参数的高阶函数
def log(test):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            _res = func(*args, **kwargs)
            end = time.time()

            print(func.__name__, text, ": ", end - start, " ms")
            return _res
        return wrapper
    return decorator
```

这里一般会考察 <code>functools.wraps</code> 的作用
(如果没有 <code>@functools.wraps(func)</code> , 则 <code>print(func.__name__)</code> 输出 <code>'wrapper'</code> 而非 <code>'test'</code>)


## 题目

设计一个decorator，它可作用于任何函数上，并打印该函数的执行时间

## 解答

```
import time
import functools

def metric(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        _res = func(*args, **kwargs)
        end = time.time()
        
        print(func.__name__, "运行了: ", end - start, " ms")
        return _res
    return wrapper
```
