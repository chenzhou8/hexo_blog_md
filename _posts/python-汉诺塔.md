title: python-汉诺塔
date: 2016-07-02 20:18:33
categories: python
tags: python
---

```python
def moveHanii(n, a, b, c):
    if n == 1:
        print a, "-->", c
        return
    moveHanii(n-1, a, c, b)
    print a, "-->", c
    moveHanii(n-1, b, a, c)

moveHanii(5, 'A', 'B', 'C')
```
