title: RPC-04Redis文本协议结构
date: 2018-09-07 09:59:53
tags: RPC
feature_img:
description: Redis 在互联网存储技术上使用非常普遍，它以高性能高并发、易于理解和易于使用而广泛应用于互联网服务的存储系统上。 Redis 要对外提供存储服务，客户端和服务器之间免不了也要进行 RPC 通信，Redis 作者 Antirez 为 Redis 设计了一套专用的文本通讯协议 RESP。
keywords: RPC
categories: RPC
cover_img: http://qiniucdn.timilong.com/154373698287.jpg
---

![tu](http://qiniucdn.timilong.com/154373698287.jpg)

> 转载自: 掘金，[深入理解RPC: 基于Python自建分布式高并发RPC服务](https://juejin.im/book/5af56a3c518825426642e004)

### 简介

![RPC](https://user-gold-cdn.xitu.io/2018/5/19/1637757f34821de2?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

Redis 在互联网存储技术上使用非常普遍，它以高性能高并发、易于理解和易于使用而广泛应用于互联网服务的存储系统上。

Redis 要对外提供存储服务，客户端和服务器之间免不了也要进行 RPC 通信，Redis 作者 Antirez 为 Redis 设计了一套专用的文本通讯协议 RESP。

![RPC](https://user-gold-cdn.xitu.io/2018/6/9/163e3f79f3ac85fd?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

Antirez 认为数据库系统的瓶颈一般不在于网络流量，而是数据库自身内部逻辑处理上。所以即使 Redis 使用了浪费流量的文本协议，依然可以取得极高的访问性能。Redis 将所有数据都放在内存，用一个单线程对外提供服务，单个节点在跑满一个 CPU 核心的情况下可以达到了 10w/s 的超高 QPS。

### 深入理解 RESP (Redis Serialization Protocol)

![RPC](https://user-gold-cdn.xitu.io/2018/5/31/163b4ebb8d0eda9b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

RESP 是 Redis 序列化协议的简写。它是一种直观的文本协议，优势在于实现异常简单，解析性能极好。

Redis 协议将传输的结构数据分为 5 种最小单元类型，单元结束时统一加上回车换行符号 <code>\r\n</code>。
```
1. 单行字符串 以+符号开头；
2. 多行字符串 以$符号开头，后跟字符串长度；
3. 整数值 以:符号开头，后跟整数的字符串形式；
4. 错误消息 以-符号开头；
5. 数组 以*号开头，后跟数组的长度;
```

#### 单行字符串 hello world
```
+hello world\r\n
```

直观打印如下：
```
+hello world
```

#### 多行字符串 第一行是长度，剩下的是内容，表示字符串 hello world 如下：
```
$11\r\nhello world\r\n
```

直观打印如下：
```
$11
hello world
```

多行字符串当然也可以表示单行字符串。

#### 整数 冒号开头 表示整数 1024 如下：
```
:1024\r\n
```

直观打印如下：
```
:1024
```

#### 错误 减号开头后跟错误名称和详细错误解释 表示「参数类型错误」如下：
```
-WRONGTYPE Operation against a key holding the wrong kind of value\r\n
```

直观打印如下：
```
-WRONGTYPE Operation against a key holding the wrong kind of value
```

数组 第一行是长度，后面依次是每个内容，表示数组 [1,2,3] 如下：
```
*3\r\n:1\r\n:2\r\n:3\r\n
```

直观打印如下：
```
*3
:1
:2
:3
```

数组里面可以嵌套其它类型，甚至可以嵌套另外一个数组，如此就可以形成复杂的数据结构。

NULL 用多行字符串表示，不过长度要写成-1。
```
$-1\r\n
```

直观打印如下：
```
$-1
```

#### 空串 用多行字符串表示，长度填 0。
```
$0\r\n\r\n
```

直观打印如下：
```
$0
```

注意这里有两个<code>\r\n</code>，为什么是两个，因为两个<code>\r\n</code>之间隔的是空串。...

### 发送指令：客户端 -> 服务器

客户端向服务器发送的指令只有一种格式，多行字符串数组。比如一个简单的 set 指令<code>set author codehole</code>会被序列化成下面的字符串。
```
*3\r\n$3\r\nset\r\n$6\r\nauthor\r\n$8\r\ncodehole\r\n
```

在控制台输出这个字符串如下，可以看出这是很好阅读的一种格式。
```
*3
$3
set
$6
author
$8
codehole...
```

### 发送指令：服务器 -> 客户端
服务器向客户端回复的响应要支持多种数据结构，所以消息响应在结构上要复杂不少。不过再复杂的响应消息也是以上 5 中基本类型的组合。

#### 单行字符串响应
```
127.0.0.1:6379> set author codehole
OK
```

这里的 OK 就是单行响应，没有使用引号括起来。
```
+OK
```

#### 错误响应
```
127.0.0.1:6379> incr author
(error) ERR value is not an integer or out of range
```

试图对一个字符串进行自增，服务器抛出一个通用的错误。
```
-ERR value is not an integer or out of range
```

#### 整数响应
```
127.0.0.1:6379> incr books
(integer) 1
```

这里的1就是整数响应。
```
:1
```

#### 多行字符串响应
```
127.0.0.1:6379> get author
"codehole"
```

这里使用双引号括起来的字符串就是多行字符串响应。
```
$8
codehole
```

#### 数组响应
```
127.0.0.1:6379> hset info name laoqian
(integer) 1
127.0.0.1:6379> hset info age 30
(integer) 1
127.0.0.1:6379> hset info sex male
(integer) 1
127.0.0.1:6379> hgetall info
1) "name"
2) "laoqian"
3) "age"
4) "30"
5) "sex"
6) "male"
```

这里的 hgetall 命令返回的就是一个数值，第 0|2|4 位置的字符串是 hash 表的 key，第 1|3|5 位置的字符串是 value，客户端负责将数组组装成字典再返回。
```
*6
$4
name
$6
laoqian
$3
age
$2
30
$3
sex
$4
male
```

#### 嵌套
```
127.0.0.1:6379> scan 0
1) "0"
2) 1) "info"
   2) "books"
   3) "author"
```

scan 命令用来扫描服务器包含的所有 key 列表，它是以游标的形式获取，一次只获取一部分。

scan 命令返回的是一个嵌套数组。数组的第一个值表示游标的值，如果这个值为零，说明已经遍历完毕。如果不为零，使用这个值作为 scan 命令的参数进行下一次遍历。数组的第二个值又是一个数组，这个数组就是 key 列表。
```
*2
$1
0
*3
$4
info
$5
books
$6
author
```

### 小结
虽然 Redis 协议里有大量冗余的回车换行符，但是这并不影响它成为互联网技术领域非常受欢迎的一个文本协议。有很多开源项目使用 RESP 作为它的通讯协议。因为在技术领域，性能并不总是代表一切，有时还要考虑简单性、易理解性和易实现性，这些都需要进行适当权衡。

Redis 协议作为开源协议中的一朵奇葩，它并没有向网络流量倾斜进行极致优化，而是选择了照顾协议的直观性、可理解性。

下一节我们拿另一个广为使用的协议 Protobuf 作为样本做介绍。相对于 Redis，Protobuf 在流量上做到了极致优化，并且是一个二进制的协议，所以注定对人类不太友好，但是它的使用真的是太太广泛啦，读者们必须耐心掌握。

### 练习
请读者尝试修改一下 redis-py 的源码，在里面增加输入输出消息的打印。然后观察 Redis 常用指令对应的输入输出消息的具体格式。

### 扩展阅读
最近，Redis 作者对 RESP 协议进行了升级，又增加了好多数据类型。这些新内容似乎让本来很简单的文本协议在升级之后变得复杂，感兴趣的读者可以点击下面链接阅读。

[RESP3 协议草稿](https://link.juejin.im/?target=https%3A%2F%2Fgist.github.com%2Fantirez%2F2bc68a9e9e45395e297d288453d5d54c)


