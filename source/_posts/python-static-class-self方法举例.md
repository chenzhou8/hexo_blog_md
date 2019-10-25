---
title: python_static_class_self方法举例
cover_img: 'http://qiniucdn.timilong.com/ChMkJ1bKy1uIPW3MABfM2owFPrIAALIpwESAgYAF8zy703.jpg'
date: 2019-10-25 12:15:10
tags: Python
feature_img:
description: Python 类方法、成员方法、静态方法的一个例子
keywords: Python
categories: Python
---

![cover_img](http://qiniucdn.timilong.com/ChMkJ1bKy1uIPW3MABfM2owFPrIAALIpwESAgYAF8zy703.jpg)

> 转载自: 微信公众号，[架构师之路]()
> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

## 距离如下
```python
# coding: utf-8
from timi_uuid import timi_uuid


class BaseMqttHandler(object):

    def __init__(self, sn=None, token=None):
        self.sn = sn
        self.token = token

    @staticmethod
    def generate_string_with_length(length=16):
        assert length in (16, 32), 'The String Length Error, Only support (16, 32)'
        _string = timi_uuid.get_hex_id()
        return _string[:length]

    @staticmethod
    def generate_message_id():
        msg_id = timi_uuid.get_hex_id()
        return msg_id

    @classmethod
    def print_staticmethod(cls):
        print(cls.generate_message_id())
        print("\n############类方法##############")
        print("不能调用: cls.sn")
        print("不同调用: cls.token")
        print("##########################\n")
        print(cls.generate_string_with_length())

    def print(self):
        print("\n############成员方法##############")
        print(self.generate_string_with_length())
        print(self.generate_message_id())
        print("##########################\n")


print("#" * 10, "类方法，不需要实例化")
BaseMqttHandler().print_staticmethod()

BaseMqttHandler().print()

print(BaseMqttHandler().generate_message_id())

```
