title: python-汉诺塔
date: 2016-07-02 20:18:33
categories: python
tags: python
cover_img: http://qiniucdn.timilong.com/1543736717464.jpg
description: 汉诺塔
---

![tu](http://qiniucdn.timilong.com/1543736717464.jpg)

## python 实现
```python
def move_hanii(n, a, b, c):
    if n == 1:
        print(a, "-->", c)
        return

    move_hanii(n-1, a, c, b)
    print(a, "-->", c)
    move_hanii(n-1, b, a, c)

move_hanii(5, 'A', 'B', 'C')
```
