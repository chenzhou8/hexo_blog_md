title: python-函数作用域
date: 2016-07-07 18:51:32
categories: python
tags: python
cover_img: http://qiniucdn.timilong.com/1543735486652.jpg
description: 函数作用域.

---

### 函数的实质与属性
* 函数是一个对象
* 函数执行完成后内部变量回收（变量被返回，那么改变量的内存空间没有被回收，即该变量的引用计数不为0）
* 函数属性
* 函数的返回值

### 函数作用域LEGB
LEGB: L > E > G > B
例子：
```
passline = 60 #全局变量global

def func(val):
    passline = 90 #局部local
    if val >= passline:
        print ('pass')
    else:
        print ('failed')

    in_func():
        print (val) #val为enclosing
    return in_func()

def Max(val1, val2):
    return max(val1, val2)

func(89)
print (Max(90, 100))

```

* L: local函数内部作用域
* E: enclosing函数内部与内嵌函数之间
* G: global全局作用域
* B: build—in内置作用域

### 闭包理解与使用
概念：
Closure: 内部函数中对enclosing作用域的变量进行引用。
在通过Python的语言介绍一下，一个闭包就是你调用了一个函数A，这个函数A返回了一个函数B给你。这个返回的函数B就叫做闭包。你在调用函数A的时候传递的参数就是自由变量。
例子1：闭包中的参数
```
#! /usr/bin/python
#-*- coding: utf-8 -*-

def func_150(val):
    passline = 90
    if val >= passline:
        print ('pass')
    else:
        print ('failed')

def func_100(val):
    passline = 60
    if val >= passline:
        print ('pass')
    else:
        print ('failed')
    def in_func():
        print (val)
    
def set_passline(passline):
    def cmp(val):#闭包
        if val >= passline:
            print ('Pass')
        else:
            print ('failed')
    return cmp

f_100 = set_passline(60)
f_150 = set_passline(90)

print (type(f_100))
print (f_100.__closure)
func_150(89)
func_100(89)
func_150(89) 

result:

```
闭包的作用：
* 封装
* 代码复用

例子2：闭包中的函数
```
def my_sum(*arg):
    print ('in my_sum')
    return sum(arg)

def my_average(*arg):
    print ('in my_average')
    return sum(arg)/len(arg)

def dec(func):
    def in_dec(*arg): 
        print ('in dec arg = ', arg)
        if len(arg) == 0:
            return 0
        for val in arg：
            if not isinstance(val, int):
                return 0
        return func(*arg)
    return in_dec

# my_sum = dec(my_sum) -> in_dec(*arg)
my_sum = dec(my_sum) #dec(func) -> dec(my_sum)
my_average = dec(my_average) 

print (my_sum(1, 2, 3, 4, 5))
print (my_sum(1, 2, 3, 4, 5, '6'))
print (my_average(1, 2, 3, 4, 5))
print (my_average(1, 2, 3, 4, '6'))
print my_sum()
print my_average()

#result:
#in dec arg = (1, 2, 3, 4, 5)
#in my_sum
#15
#in dec arg = (1, 2, 3, 4, 5, '6')
#0

#...

```

### 装饰器
* 装饰器装饰函数
* 返回一个函数对象
* 被装饰函数标识符指向返回函数对象
* 语法糖： @deco

```
def deco(func):
    def in_deco(x, y):
        print ('in deco')
        func(x, y)
    print ('call deco')
    return in_deco
#deco(bar) -> in_deco
#bar = in_deco
#bar() in_deco() bar()

@deco
def bar(x, y):
    print ('in bar', x+y)
print (type(bar))
bar(1, 2)

#result:
#call deco
#<class 'function'>
#in deco
#in bar 3
```
