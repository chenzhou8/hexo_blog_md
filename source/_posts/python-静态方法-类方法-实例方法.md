---
title: python-静态方法-类方法-实例方法
cover_img: http://qiniucdn.timilong.com/1544683266425.jpg
date: 2019-02-11 18:00:25
tags: python
feature_img:
description: Python 类方法、实例方法、静态方法.
keywords: python
categories: python
---

![cover_img](http://qiniucdn.timilong.com/1544683266425.jpg)


## 代码

```python

class A(object):
    """ 类属性 """
    NAME = "Timilong"
    SCORE = 100

    def __init__(self, name, score):
        """ 实例属性 """
        self.name = name
        self.score = score

    def foo(self, x):
        # 类实例方法
        print("executing foo(%s, %s)" % (self, x))

    @classmethod
    def class_foo(cls, x):
        # 类方法
        print("executing class_foo(%s, %s)" % (cls, x))

    @staticmethod
    def static_foo(x):
        # 静态方法
        print("executing static_foo(%s)" % x)

```

## 调用方式

```python

a = A()
a.foo(1)          # executing foo(<main.A object at 0xb77d67ec>, 1)
a.class_foo(1)    # executing class_foo(<class 'main.A'>, 1)
A.class_foo(1)    # executing class_foo(<class 'main.A'>, 1)
a.static_foo(1)   # executing static_foo(1)
A.static_foo(1)   # executing static_foo(1)
```

## 说明

类方法和静态方法都可以被类和类实例调用
类实例方法仅可以被类实例调用

类方法的隐含调用参数是类，而类实例方法的隐含调用参数是类的实例，静态方法没有隐含调用参数
