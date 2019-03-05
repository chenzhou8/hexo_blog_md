---
title: python-实例方法-静态方法-类方法2
cover_img: 'http://qiniucdn.timilong.com/1551521120991.jpg'
date: 2019-03-04 14:49:56
tags: python
feature_img:
description: 通过举例，详细说明@classmethod, @staticmethod, 实例方法的用法
keywords: python
categories: python
---

![cover_img](http://qiniucdn.timilong.com/1551521120991.jpg)

## 介绍
Python 中，实例方法（instance method），类方法（class method）与静态方法（static method）经常容易混淆。本文通过代码例子来说明它们的区别。

## 实例方法
Python 的实例方法用得最多，也最常见。我们先来看 Python 的实例方法。
```python
class Kls(object):
    def __init__(self, data):
        self.data = data

    def printd(self):
        print(self.data)


ik1 = Kls('leo')
ik2 = Kls('lee')

ik1.printd()
ik2.printd()
```
输出：
```python
leo
lee
```

上述例子中，`printd`为一个实例方法。实例方法第一个参数为`self`，当使用`ik1.printd()`调用实例方法时，实例`ik1`会传递给`self`参数，这样`self`参数就可以引用当前正在调用实例方法的实例。利用实例方法的这个特性，上述代码正确输出了两个实例的成员数据。

## 类方法
Python 的类方法采用装饰器@classmethod来定义，我们直接看例子。

```python
class Kls(object):
    num_inst = 0

    def __init__(self):
        Kls.num_inst = Kls.num_inst + 1

    @classmethod
    def get_no_of_instance(cls):
        return cls.num_inst


ik1 = Kls()
ik2 = Kls()

print(ik1.get_no_of_instance())
print(Kls.get_no_of_instance())
```

输出：
```
2
2
```

在上述例子中，我们需要统计类`Kls`实例的个数，因此定义了一个类变量`num_inst`来存放实例个数。通过装饰器`@classmethod`的使用，方法`get_no_of_instance`被定义成一个类方法。在调用类方法时，Python
会将类（class Kls）传递给`cls`，这样在`get_no_of_instance`内部就可以引用类变量`num_inst`。
由于在调用类方法时，只需要将类型本身传递给类方法，因此，既可以通过类也可以通过实例来调用类方法。

## 静态方法
在开发中，我们常常需要定义一些方法，这些方法跟类有关，但在实现时并不需要引用类或者实例，例如，设置环境变量，修改另一个类的变量，等。这个时候，我们可以使用静态方法。
Python 使用装饰器@staticmethod来定义一个静态方法。

```python
IND = 'ON'


class Kls(object):
    def __init__(self, data):
        self.data = data

    @staticmethod
    def checkind():
        return IND == 'ON'

    def do_reset(self):
        if self.checkind():
            print('Reset done for: %s' % self.data)

    def set_db(self):
        if self.checkind():
            print('DB connection made for: %s' % self.data)


ik1 = Kls(24)
ik1.do_reset()
ik1.set_db()
```

输出：
```python
Reset done for: 24
DB connection made for: 24
```

在代码中，我们定义了一个全局变量`IND`，由于`IND`跟类`Kls`相关，所以我们将方法`checkind`放置在类`Kls`中定义。方法`checkind`只需检查`IND`的值，而不需要引用类或者实例，因此，我们将方法`checkind`定义为静态方法。
对于静态方法，Python 并不需要传递类或者实例，因此，既可以使用类也可以使用实例来调用静态方法。

## 实例方法，类方法与静态方法的区别
我们用代码说明实例方法，类方法，静态方法的区别。注意下述代码中方法foo，class_foo，static_foo的定义以及使用。

```python
class Kls(object):
    def foo(self, x):
        print('executing foo(%s,%s)' % (self, x))

    @classmethod
    def class_foo(cls,x):
        print('executing class_foo(%s,%s)' % (cls,x))

    @staticmethod
    def static_foo(x):
        print('executing static_foo(%s)' % x)


ik = Kls()

# 实例方法
ik.foo(1)
print(ik.foo)
print('==========================================')

# 类方法
ik.class_foo(1)
Kls.class_foo(1)
print(ik.class_foo)
print('==========================================')

# 静态方法
ik.static_foo(1)
Kls.static_foo('hi')
print(ik.static_foo)
```

输出：
```
executing foo(<__main__.Kls object at 0x0551E190>,1)
<bound method Kls.foo of <__main__.Kls object at 0x0551E190>>
==========================================
executing class_foo(<class '__main__.Kls'>,1)
executing class_foo(<class '__main__.Kls'>,1)
<bound method type.class_foo of <class '__main__.Kls'>>
==========================================
executing static_foo(1)
executing static_foo(hi)
<function static_foo at 0x055238B0>
```

对于实例方法，调用时会把实例`ik`作为第一个参数传递给`self`参数。因此，调用`ik.foo(1)`时输出了实例ik的地址。

对于类方法，调用时会把类`Kls`作为第一个参数传递给`cls`参数。因此，调用`ik.class_foo(1)`时输出了Kls类型信息。
前面提到，可以通过类也可以通过实例来调用类方法，在上述代码中，我们再一次进行了验证。

对于静态方法，调用时并不需要传递类或者实例。其实，静态方法很像我们在类外定义的函数，只不过静态方法可以通过类或者实例来调用而已。

值得注意的是，在上述例子中，`foo`只是个函数，但当调用`ik.foo`的时候我们得到的是一个已经跟实例`ik`绑定的函数。调用`foo`时需要两个参数，但调用`ik.foo`时只需要一个参数。`foo`跟`ik`进行了绑定，因此，当我们打印`ik.foo`时，会看到以下输出:
```
<bound method Kls.foo of <__main__.Kls object at 0x0551E190>>
```
当调用ik.class_foo时，由于class_foo是类方法，因此，class_foo跟Kls进行了绑定（而不是跟ik绑定）。当我们打印ik.class_foo时，输出：
```
<bound method type.class_foo of <class '__main__.Kls'>>
```

当调用ik.static_foo时，静态方法并不会与类或者实例绑定，因此，打印ik.static_foo（或者Kls.static_foo）时输出：
```
<function static_foo at 0x055238B0>
```

概括来说，是否与类或者实例进行绑定，这就是实例方法，类方法，静态方法的区别。
