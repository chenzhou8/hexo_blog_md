---
title: python-微信红包算法
cover_img: http://qiniucdn.timilong.com/1544683532603.jpg
date: 2019-02-13 11:07:14
tags: python
feature_img:
description: 如何设计抢红包系统?
keywords: python
categories: python
---

![cover_img](http://qiniucdn.timilong.com/1544683532603.jpg)

> 参考: http://www.open-open.com/lib/view/open1430729729960.html

## 要求
- 所有抢到红包的金额等于红包金额；
- 每个人至少抢到0.01元；
- 保证所有人抢到金额的几率相等；

## 红包分配算法代码实现

```python
"""
随机，额度在0.01和剩余平均值*2之间。
"""
import random
def send_money(total_yuan, num):
    """send_money

    :param total_yuan: 元为单位，转成分
    :param num: 人数
    """
    total = total_yuan * 100  # 分为单位
    cur_total = 0
    for i in range(num - 1):
        remain = total - cur_total
        money = random.randint(1, int(remain / (num - i) * 2))
        cur_total += money
        yield round(money / 100.0, 2)
    yield round((total - cur_total) /100.0, 2)


def test():
    t = 0
    for i in send_money(100, 10):
        t += i
        print(i)
    print('sum:', t)


if __name__ == '__main__':
    test()

```
