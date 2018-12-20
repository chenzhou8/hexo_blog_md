---
title: python-装饰器的典型实现
date: 2018-06-23 10:08:38
tags: python
categories: python
description: 装饰器本质上是一个 Python 函数或类，它可以让其他函数或类在不需要做任何代码修改的前提下增加额外功能，装饰器的返回值也是一个函数/类对象。它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景，装饰器是解决这类问题的绝佳设计。有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码到装饰器中并继续重用。概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。
cover_img: http://qiniucdn.timilong.com/1543735365191.jpg
---

![tu](http://qiniucdn.timilong.com/1543735365191.jpg)

## 题目1

请实现装饰器log，可以计算test函数的运行时间
```python
@log('excute')
def test():
    pass
```

## 解答

```python
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

```python
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
