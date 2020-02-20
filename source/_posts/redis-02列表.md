---
title: redis-02列表
cover_img: 'http://qiniucdn.timilong.com/ChMkJ1bKy1-IMCuXAObR3XZD4CsAALIqAB4C8cA5tH1028.jpg'
date: 2020-02-20 15:45:33
tags: Redis
feature_img:
description: Redis列表
keywords: Redis
categories: Redis
---

![cover_img](http://qiniucdn.timilong.com/ChMkJ1bKy1-IMCuXAObR3XZD4CsAALIqAB4C8cA5tH1028.jpg)


## 列表

Redis 的列表相当于 Java 语言里面的 LinkedList，注意它是链表而不是数组。这意味着 list 的插入和删除操作非常快，时间复杂度为 O(1)，但是索引定位很慢，时间复杂度为 O(n)，这点让人非常意外。

当列表弹出了最后一个元素之后，该数据结构自动被删除，内存被回收。

Redis 的列表结构常用来做异步队列使用。将需要延后处理的任务结构体序列化成字符串塞进 Redis 的列表，另一个线程从这个列表中轮询数据进行处理。

### 右边进(rpush), 左边出(lpop)：队列
```
> rpush books python java golang
(integer) 3

> llen books
(integer) 3

> lpop books
"python"

> lpop books
"java"

> lpop books
"golang"

> lpop books
(nil)
```

### 右边进右边出：栈
```
> rpush books python java golang
(integer) 3

> rpop books
"golang"

> rpop books
"java"

> rpop books
"python"

> rpop books
(nil)
```

### 慢操作

`lindex` 相当于 Java 链表的get(int index)方法，它需要对链表进行遍历，性能随着参数index增大而变差。

`ltrim` 和字面上的含义不太一样，个人觉得它叫 `lretain(保留)` 更合适一些，因为 ltrim 跟的两个参数start_index和end_index定义了一个区间，在这个区间内的值，ltrim 要保留，区间之外统统砍掉。我们可以通过ltrim来实现一个定长的链表，这一点非常有用。

index 可以为负数，index=-1表示倒数第一个元素，同样index=-2表示倒数第二个元素。

`lrange` 获取指定index范围的元素`lrange books 0 -1` 表示获取所有元素。

```
> rpush books python java golang
(integer) 3

> lindex books 1  # O(n) 慎用
"java"

> lrange books 0 -1  # 获取所有元素，O(n) 慎用
1) "python"
2) "java"
3) "golang"

> ltrim books 1 -1 # O(n) 慎用
OK

> lrange books 0 -1
1) "java"
2) "golang"

> ltrim books 1 0 # 这其实是清空了整个列表，因为区间范围长度为负
OK

> llen books
(integer) 0
```

### 快速列表

如果再深入一点，你会发现 Redis 底层存储的还不是一个简单的 `linkedlist`，而是称之为快速链表 `quicklist` 的一个结构。

首先在列表元素较少的情况下会使用一块连续的内存存储，这个结构是 ziplist，也即是压缩列表。它将所有的元素紧挨着一起存储，分配的是一块连续的内存。当数据量比较多的时候才会改成 quicklist。因为普通的链表需要的附加指针空间太大，会比较浪费空间，而且会加重内存的碎片化。比如这个列表里存的只是 int 类型的数据，结构上还需要两个额外的指针 prev 和 next 。所以 Redis 将链表和 ziplist 结合起来组成了 quicklist。也就是将多个 ziplist 使用双向指针串起来使用。这样既满足了快速的插入删除性能，又不会出现太大的空间冗余。

