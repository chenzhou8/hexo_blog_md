title: python-函数式编程
date: 2016-07-03 20:09:27
categories: python
tags: python
cover_img: http://qiniucdn.timilong.com/1543735415562.jpg
description: 函数式编程.
---

![tu](http://qiniucdn.timilong.com/1543735415562.jpg)

### 函数式编程综合概述
#### 什么是函数式编程？
函数式编程：使用一系列的函数解决实际问题。

函数仅接受输入并产生输出，不包含任何能影响产生输出的内部状态。

任何情况下，使用相同的参数调用函数始终恩那个产生同样的结果。

在一个函数式的程序中，输入的数据“流过”一系列的函数，每一个函数根据它的输入产生输出。

函数式风格避免编写有“边界效应”的函数： 修改内部状态，或者是其它无法反应在输出上的变化。

完全没有边界效应的函数被称为“纯函数式的”。

避免边界效应意味着不适用在程序运行时可变的数据结构， 输出只依赖输入。

可以认为函数式编程站在了面向对象编程的对立面。



对象通常包含内部状态（字段），和许多能修改这些状态的函数，程序则由不断修改状态构成；函数式编程则极力避免状态改动，并
通过在函数间传递数据流进行工作。

但这并不意味着说无法使用函数式编程和面向对象编程。

事实上，复杂的系统一般会采用面向对象技术建模，但混合使用函数式风格还能让我们额外享受函数式风格的优点。

#### 函数式编程的优点？
* 模块化
* 逻辑可证明
* 组件化
* 易于调试
* 易于测试
* 更高的生产率

### 高阶函数
* 变量可以指向函数
* 函数的参数可以接收变量
* 一个函数可以接收另外一个函数作为参数

例子：实现绝对值加法
```
def add(x, y, f):
    return f(x) + f(y)

add(-5, 9, abs)

result: 14
```

#### 内置高阶函数:map()
map函数有两个参数，一个是函数，另外一个是列表list，返回值为对传入的列表的每一个元素执行传入的函数操作得到的列表；
例子: 按照命名规范命名
```
def format_name(s):
    return s.title()

map(format_name, ['adam', 'LisA', 'asdT']
```

#### 内置的高阶函数:reduce()
reduce()函数也有两个参数，一个是函数，另外一个是列表list，返回值是对list的每一个元素反复调用函数f, 得到最终结果
例子：实现列表元素的连乘
```
def prod(x, y):
    return x * y

print reduce(prod, [2, 4, 5, 7, 12])
```

#### 内置高阶函数:filter()
filter()函数接受函数参数f和列表参数list，f对list元素进行判断，返回list的元素中调用f函数结果为true的元素组成的列表
例子：判断1~100中平方根是整数的数
```
import math

def is_sqr(x):
   a = int(math.sqrt(x))
   return a * a == x

print filter(is_sqr, range(1, 101))
```

#### 自定义函数:sorted()
sorted函数接受一个列表list和一个函数参数f, f为自定义的比较list元素的大小的函数，返回list中元素按照f函数排列的列表
例子：返回list中名字按照小写字母顺序排序的列表
```
def cmp_ignore_case(s1, s2):
    return cmp(s1.lower(), s2.lower())

print sorted(['bob', 'about', 'Zoo', 'Credit'], cmp_ignore_case)
```

#### 在函数中返回一个函数
例子：实现列表元素的阶乘
```
def calc_prod(lst):
    def prod(x, y):
       return x * y
    def g():
       return reduce(prod, lst)
    return g;

f = calc_prod([1, 2, 3, 4])
print f()
```

#### python闭包
内层函数使用外层函数的参数，然后返回内层函数
例子：计算1,2,3的平方结果，存入列表
```
def count():
    fs = []
    for i in range(1, 4):
        def f(j):
            def g():
                return j * j
            return g
        fs.append(f(i))
    return fs

f1, f2, f3 = count()
print f1(), f2(), f3()
```

#### 匿名函数
传入函数参数不需要显式定义函数，可以用lambda x: statement 其中，x为参数，statement为对参数执行的语句；
例子：删除列表中的空元素
```
def is_not_empty(s):
    return s and len(s.strip()) > 0

print filter(lambda s:s and len(s.strip()) > 0, ['test', None, '', 'str', '  ', 'END'])
```

#### 装饰器
给函数添加新功能，并简化函数的调用；
例子:无参数装饰器的示例，打印函数调用的日志
```
def log(f):
    def fn(*args, **kw)): #*args, **kw保证对任意个数参数都能正常调用
        print 'call' + f.__name__+ '()...'
        return f(*args, **kw)
    return fn

@log #调用日志装饰器
def factorial(n):
    return reduce(lambda x, y : x*y, range(1, n+1))
print factorial(10)
```

例子：带参数的装饰器示例，打印函数调用日志
```
def log(prefix):
   def log_decorator(f):
       def wrapper(*args, **kw):
           print '[%s] %s()...' % (prefix, f.__name__)
           return f(*args, **kw)
       return wrapper
    return log_decarator

@log('DEBUG') #DEBUG为给装饰器传入的参数
def test():
    pass
print test()

result:
[DEBUG] test()...
None
```

利用functool.wraps作用在返回的新函数上，使得调用装饰器以后不改变原函数的信息
```
import time, functools
def performance(unit):
    def perf_decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kw):
            t1 = time.time()
            r = f(*args, **kw)
            t2 = time.time()
            t = (t2-t1) * 1000 if unit == 'ms' else (t2 - t1)
            print 'call  %s() in %f %s' % (f.__name__, t, unit)
            return r
        return wrapper
    return perf_decorator

@performanced('ms')
def factorial(n):
   return reduce(lambda x, y: x*y, range(1, n+1))
print factorial.__name__
```


#### 偏函数
functools.partial(f, f的默认参数) 减少需要提供给f的参数






