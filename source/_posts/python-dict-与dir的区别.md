---
title: python-__dict__与dir的区别
cover_img: 'http://qiniucdn.timilong.com/1551521146198.jpg'
date: 2019-08-20 11:14:33
tags: Python
feature_img:
description: Python中的__dict__属性和dir()方法的区别
keywords: Python
categories: Python
---

![cover_img](http://qiniucdn.timilong.com/1551521146198.jpg)

## 说明
Python下一切皆对象，每个对象都有多个属性(attribute)，Python对属性有一套统一的管理方案。

## 区别
- `__dict__`是一个字典，键为属性名，值为属性值

- `dir()`是一个函数，返回的是`list`

- `dir()`用来寻找一个对象的所有属性，包括`__dict__`中的属性，`__dict__是dir()`的子集

- 并不是所有的对象都拥有`__dict__`属性，许多内建类型就没有__dict__属性，如list，此时就需要用dir()来列出对象的所有属性。
 
## __dict__属性

__dict__是用来存储对象属性的一个字典，其键为属性名，值为属性的值。
```python
# coding: utf-8

class A(object):
    class_var = 1
    def __init__(self):
        self.name = 'xy'
        self.age = 2

    @property
    def num(self):
        return self.age + 10

    def fun(self): pass
    def static_f(self): pass
    @classmethod
    def class_f(cls): pass

if __name__ == '__main__':#主程序
    a = A()
    print a.__dict__   #{'age': 2, 'name': 'xy'}   实例中的__dict__属性
    print A.__dict__   
    '''
    类A的__dict__属性
    {
    '__dict__': <attribute '__dict__' of 'A' objects>, #这里如果想深究的话查看参考链接5
    '__module__': '__main__',               #所处模块
    'num': <property object>,               #特性对象 
    'class_f': <function class_f>,          #类方法
    'static_f': <function static_f>,        #静态方法
    'class_var': 1, 'fun': <function fun >, #类变量
    '__weakref__': <attribute '__weakref__' of 'A' objects>, 
    '__doc__': None,                        #class说明字符串
    '__init__': <function __init__ at 0x0000000003451AC8>}
    '''

    a.level1 = 3
    a.fun = lambda :x
    print a.__dict__  #{'level1': 3, 'age': 2, 'name': 'xy','fun': <function <lambda> at 0x>}
    print A.__dict__  #与上述结果相同

    A.level2 = 4
    print a.__dict__  #{'level1': 3, 'age': 2, 'name': 'xy'}
    print A.__dict__  #增加了level2属性

    print object.__dict__
    '''
    {'__setattr__': <slot wrapper '__setattr__' of 'object' objects>, 
    '__reduce_ex__': <method '__reduce_ex__' of 'object' objects>, 
    '__new__': <built-in method __new__ of type object at>, 
    等.....
    '''
 
```

从上述代码可知: 

- 实例的__dict__仅存储与该实例相关的实例属性，

- 正是因为实例的__dict__属性，每个实例的实例属性才会互不影响。

- 类的__dict__存储所有实例共享的变量和函数(类属性，方法等)，类的__dict__并不包含其父类的属性。

 
## dir()函数
​`dir()`是Python提供的一个API函数，`dir()`函数会自动寻找一个对象的所有属性(包括从父类中继承的属性)。

​一个实例的`__dict__`属性仅仅是那个实例的实例属性的集合，并不包含该实例的所有有效属性。

所以如果想获取一个对象所有有效属性，应使用`dir()`。
```python
print dir(A)
"""
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__',\
 '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'age', 'class_f', \
'class_var', 'fun', 'level1', 'level2', 'name', 'num', 'static_f']
"""


a_dict = a.__dict__.keys()
A_dict = A.__dict__.keys()
object_dict = object.__dict__.keys()
print a_dict  
print A_dict  
print object_dict 

"""
['fun', 'level1', 'age', 'name']

['__module__', 'level2', 'num', 'static_f', '__dict__', '__weakref__', '__init__', 'class_f', 'class_var', 'fun', '__doc__']

['__setattr__', '__reduce_ex__', '__new__', '__reduce__', '__str__', '__format__', '__getattribute__', '__class__', '__delattr__',\
 '__subclasshook__', '__repr__', '__hash__', '__sizeof__', '__doc__', '__init__']
"""

# 因为每个类都有一个__doc__属性，所以需要去重，去重后然后比较
print set(dir(a)) == set(a_dict + A_dict + object_dict)  # True
```

 
## 结论

`dir()`函数会自动寻找一个对象的所有属性，包括`__dict__`中的属性。

`__dict__`是`dir()`的子集，`dir()`包含`__dict__`中的属性。
