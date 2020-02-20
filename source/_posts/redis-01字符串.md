---
title: redis-01字符串
cover_img: 'http://qiniucdn.timilong.com/ChMkJlbKy1uIKb8ZABC2Xa8CNA8AALIpwEBS5EAELZ1100.jpg'
date: 2020-02-20 15:35:24
tags: Redis
feature_img: 
description: Redis字符串基础使用
keywords: Redis
categories: Redis
---

![cover_img](http://qiniucdn.timilong.com/ChMkJlbKy1uIKb8ZABC2Xa8CNA8AALIpwEBS5EAELZ1100.jpg)


## 字符串
### string (字符串)
字符串 string 是 Redis 最简单的数据结构。Redis 所有的数据结构都是以唯一的 key 字符串作为名称，然后通过这个唯一 key 值来获取相应的 value 数据。不同类型的数据结构的差异就在于 value 的结构不一样。


字符串结构使用非常广泛，一个常见的用途就是缓存用户信息。我们将用户信息结构体使用 JSON 序列化成字符串，然后将序列化后的字符串塞进 Redis 来缓存。同样，取用户信息会经过一次反序列化的过程。


Redis 的字符串是动态字符串，是可以修改的字符串，内部结构实现上类似于 Java 的 ArrayList，采用预分配冗余空间的方式来减少内存的频繁分配，如图中所示，内部为当前字符串实际分配的空间 capacity 一般要高于实际字符串长度 len。当字符串长度小于 1M 时，扩容都是加倍现有的空间，如果超过 1M，扩容时一次只会多扩 1M 的空间。需要注意的是字符串最大长度为 512M。

### 键值对
```
> set name codehole
OK

> get name
"codehole"

> exists name
(integer) 1

> del name
(integer) 1

> get name
(nil)
```

### 批量键值对

可以批量对多个字符串进行读写，节省网络耗时开销。
```
> set name1 codehole
OK

> set name2 holycoder
OK

> mget name1 name2 name3 # 返回一个列表
1) "codehole"
2) "holycoder"
3) (nil)

> mset name1 boy name2 girl name3 unknown

> mget name1 name2 name3
1) "boy"
2) "girl"
3) "unknown"
```

### 过期和 set 命令扩展

可以对 key 设置过期时间，到点自动删除，这个功能常用来控制缓存的失效时间。
```
> set name codehole
> get name
"codehole"

> expire name 5  # 5s 后过期
...  # wait for 5s

> get name
(nil)

> setex name 5 codehole  # 5s 后过期，等价于 set+expire  语法: setex [键名] [过期时间] [键值]

> get name
"codehole"
... # wait for 5s

> get name
(nil)

> setnx name codehole  # 如果 name 不存在就执行 set 创建
(integer) 1

> get name
"codehole"

> setnx name holycoder
(integer) 0  # 因为 name 已经存在，所以 set 创建不成功

> get name
"codehole"  # 没有改变
```

### 计数

如果 value 值是一个整数，还可以对它进行自增操作。自增是有范围的，它的范围是 signed long 的最大最小值，超过了这个值，Redis 会报错。
```
> set age 30
OK

> incr age  # 自增+1
(integer) 31

> incrby age 5  # 自增+n
(integer) 36

> incrby age -5  # 自增-N
(integer) 31

> set codehole 9223372036854775807  # Long.Max
OK

> incr codehole
(error) ERR increment or decrement would overflow
```

字符串是由多个字节组成，每个字节又是由 8 个 bit 组成，如此便可以将一个字符串看成很多 bit 的组合，这便是 bitmap「位图」数据结构。
