---
title: RPC_03深入RPC消息协议
date: 2018-09-06 17:56:40
categories: RPC
tags: RPC
feature_img:
description: 对于一串消息流，我们必须能确定消息边界，提取出单条消息的字节流片段，然后对这个片段按照一定的规则进行反序列化来生成相应的消息对象。
keywords: RPC
cover_img: http://qiniucdn.timilong.com/1543735500548.jpg
---

![tu](http://qiniucdn.timilong.com/1543735500548.jpg)

> 转载自: 掘金，[深入理解RPC: 基于Python自建分布式高并发RPC服务](https://juejin.im/book/5af56a3c518825426642e004)

### 介绍

本节我们开始讲解 RPC 的消息协议设计背后的基本原理，了解 RPC 的协议开发背后有哪些需要考虑的基本点。在通晓原理之后，我们就可以自己设计一套协议来开发属于自己的 RPC 系统。

本节主要涉及的知识点和它们之见的关系如下图：

![rpc](https://user-gold-cdn.xitu.io/2018/5/31/163b506eba8a3aae?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

对于一串消息流，我们必须能确定消息边界，提取出单条消息的字节流片段，然后对这个片段按照一定的规则进行反序列化来生成相应的消息对象。

消息表示指的是序列化后的消息字节流在直观上的表现形式，它看起来是对人类友好还是对计算机友好。文本形式对人类友好，二进制形式对计算机友好。

每个消息都有其内部字段结构，结构构成了消息内部的逻辑规则，程序要按照结构规则来决定字段序列化的顺序。

接下来，我们初步详细拆解。

### 消息边界
RPC 需要在一条 TCP 链接上进行多次消息传递。在连续的两条消息之间必须有明确的分割规则，以便接收端可以将消息分割开来，这里的接收端可以是 RPC 服务器接收请求，也可以是 RPC 客户端接收响应。

基于 TCP 链接之上的单条消息如果过大，就会被网络协议栈拆分为多个数据包进行传送。如果消息过小，网络协议栈可能会将多个消息组合成一个数据包进行发送。对于接收端来说它看到的只是一串串的字节数组，如果没有明确的消息边界规则，接收端是无从知道这一串字节数组究竟是包含多条消息还是只是某条消息的一部分。

比较常用的两种分割方式是特殊分割符法和长度前缀法。

![rpc](https://user-gold-cdn.xitu.io/2018/5/10/16347e7b909be082?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

消息发送端在每条消息的末尾追加一个特殊的分割符，并且保证消息中间的数据不能包含特殊分割符。比如最为常见的分割符是<code>\r\n</code>。

当接收端遍历字节数组时发现了<code>\r\n</code>，就立即可以断定<code>\r\n</code>之前的字节数组是一条完整的消息，可以传递到上层逻辑继续进行处理。

HTTP 和 Redis 协议就大量使用了<code>\r\n</code>分割符。此种消息一般要求消息体的内容是文本消息。

![rpc](https://user-gold-cdn.xitu.io/2018/5/10/16347e89710eb4da?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

消息发送端在每条消息的开头增加一个 4 字节长度的整数值，标记消息体的长度。这样消息接受者首先读取到长度信息，然后再读取相应长度的字节数组就可以将一个完整的消息分离出来。此种消息比较常用于二进制消息。

基于特殊分割符法的优点在于消息的可读性比较强，可以直接看到消息的文本内容，缺点是不适合传递二进制消息，因为二进制的字节数组里面很容易就冒出连续的两个字节内容正好就是<code>\r\n</code>分割符的 ascii 值。如果需要传递的话，一般是对二进制进行 base64 编码转变成普通文本消息再进行传送。

基于长度前缀法的优点和缺点同特殊分割符法正好是相反的。长度前缀法因为适用于二进制协议，所以可读性很差。但是对传递的内容本身没有特殊限制，文本和内容皆可以传输，不需要进行特殊处理。HTTP 协议的 Content-Length 头信息用来标记消息体的长度，这个也可以看成是长度前缀法的一种应用。

```
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/2.7.13
Date: Thu, 10 May 2018 02:38:03 GMT
Content-type: text/html; charset=utf-8
Content-Length: 10393
# 此处省略 10393 字节消息体数据
```

HTTP 协议是一种基于特殊分割符和长度前缀法的混合型协议。比如 HTTP 的消息头采用的是纯文本外加,<code>\r\n</code>分割符，而消息体则是通过消息头中的 Content-Type 的值来决定长度。HTTP 协议虽然被称之为文本传输协议，但是也可以在消息体中传输二进制数据数据的，例如音视频图像，所以 HTTP 协议被称之为「超文本」传输协议。

### 消息的结构
每条消息都有它包含的语义结构信息，有些消息协议的结构信息是显式的，还有些是隐式的。比如 json 消息，它的结构就可以直接通过它的内容体现出来，所以它是一种显式结构的消息协议。

```
{
     "firstName": "John",
     "lastName": "Smith",
     "gender": "male",
     "age": 25,
     "address": 
     {
         "streetAddress": "21 2nd Street",
         "city": "New York",
         "state": "NY",
         "postalCode": "10021"
     },
     "phoneNumber": 
     [
         {
           "type": "home",
           "number": "212 555-1234"
         },
         {
           "type": "fax",
           "number": "646 555-4567"
         }
     ]
 }
```

json 这种直观的消息协议的可读性非常棒，但是它的缺点也很明显，有太多的冗余信息。比如每个字符串都使用双引号来界定边界，key/value 之间必须有冒号分割，对象之间必须使用大括号分割等等。这些还只是冗余的小头，最大的冗余还在于连续的多条 json 消息即使结构完全一样，仅仅只是 value 的值不一样，也需要发送同样的 key 字符串信息。

消息的结构在同一条消息通道上是可以复用的，比如在建立链接的开始 RPC 客户端和服务器之间先交流协商一下消息的结构，后续发送消息时只需要发送一系列消息的 value 值，接收端会自动将 value 值和相应位置的 key 关联起来，形成一个完成的结构消息。在 Hadoop 系统中广泛使用的 avro 消息协议就是通过这种方式实现的，在 RPC 链接建立之处就开始交流消息的结构，后续消息的传递就可以节省很多流量。

消息的隐式结构一般是指那些结构信息由代码来约定的消息协议，在 RPC 交互的消息数据中只是纯粹的二进制数据，由代码来确定相应位置的二进制是属于哪个字段。比如下面的这段代码。

```
// 发送端写消息
class AuthUserOutput {
    int platformId;
    long deviceId;
    String productId;
    String channelId;
    String versionId;
    String phoneModel;
    	
    @Override
    public void writeImpl() {
        writeByte((byte) this.platformId);
        writeLong(deviceId);
        writeStr(productId);
        writeStr(channelId);
        writeStr(versionId);
        writeStr(phoneModel);
    }
}

// 接收端读取消息
class AuthorizeInput {
    int platformId;
    long deviceId;
    String productId;
    String channelId;
    String versionId;
    String phoneModel;
    	
    @Override
    public void readImpl() {
        this.platformId = readByte();
        this.deviceId = readLong();
        this.productId = readStr();
        this.channelId = readStr();
        this.versionId = readStr();
        this.phoneModel = readStr();
    }
}

```
如果纯粹看消息内容是无法知道节点消息内容中的哪些字节的含义，它的消息结构是通过代码的结构顺序来确定的。这种隐式的消息的优点就在于节省传输流量，它完全不需要传输结构信息。

### 消息压缩
如果消息的内容太大，就要考虑对消息进行压缩处理，这可以减轻网络带宽压力。但是这同时也会加重 CPU 的负担，因为压缩算法是 CPU 计算密集型操作，会导致操作系统的负载加重。所以，最终是否进行消息压缩，一定要根据业务情况加以权衡。

如果确定压缩，那么在选择压缩算法包时，务必挑选那些底层用 C 语言实现的算法库，因为 Python 的字节码执行起来太慢了。比较流行的消息压缩算法有 Google 的 snappy 算法，它的运行性能非常好，压缩比例虽然不是最优的，但是离最优的差距已经不是很大。阿里的 SOFA RPC 就使用了 snappy 作为协议层压缩算法。

### 流量的极致优化

开源的流行 RPC 消息协议往往对消息流量优化到了极致，它们通过这种方式来打动用户，吸引用户来使用它们。比如对于一个整形数字，一般使用 4 个字节来表示一个整数值。

但是经过研究发现，消息传递中大部分使用的整数值都是很小的非负整数，如果全部使用 4 个字节来表示一个整数会很浪费。所以就发明了一个类型叫变长整数varint。数值非常小时，只需要使用一个字节来存储，数值稍微大一点可以使用 2 个字节，再大一点就是 3 个字节，它还可以超过 4 个字节用来表达长整形数字。

其原理也很简单，就是保留每个字节的最高位的 bit 来标识是否后面还有字节，1 表示还有字节需要继续读，0 表示到读到当前字节就结束。

![rpc](https://user-gold-cdn.xitu.io/2018/5/10/163483000fcef1a5?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

那如果是负数该怎么办呢？-1 的 16 进制数是 0xFFFFFFFF，如果要按照这个编码那岂不是要 6 个字节才能存的下。-1 也是非常常见的整数啊。

于是 zigzag 编码来了，专门用来解决负数问题。zigzag 编码将整数范围一一映射到自然数范围，然后再进行 varint 编码。
```
0 => 0
-1 => 1
1 => 2
-2 => 3
2 => 4
-3 => 5
3 => 6
```

zigzag 将负数编码成正奇数，正数编码成偶数。解码的时候遇到偶数直接除 2 就是原值，遇到奇数就加 1 除 2 再取负就是原值。

### 小结
现在我们知道了 RPC 消息结构的设计原理，遵循这些基本方法，就可以创造出一个又一个不同的消息协议。

下一节我们将讲一个具体的实例，拿市场上应用最广的开源存储中间件 Redis 的消息协议为例进行详细分析。

### 练习题
请读者自己实现一下 varint 和 zigzag 编码转换器，不要求读者实现的特别高效，但应当实现基本的输入输出。

另，这个作业的代码实现会涉及到不少 Python 的位操作知识，可以温故而知新。

### 解答
```
# zigzag
def zigzag_encode(x):
    return x * 2 if x >= 0 else -2 * x - 1


def zigzag_decode(x):
    return x >> 1 if not x & 1 else -1 * (x+1) >> 1

# varint
def varint_encode(x):

    result = 0
    tail = x & 0x7f

    i = 1
    r = x >> 7
    while r > 0:
        n = (r & 0x7f) | 0x80
        result |= n << (8 * i)
        r = r >> 7
        i += 1

    return result | tail


def varint_decode(x):

    result = 0
    tail = x & 0xff

    i = 1
    r = x >> 8
    while r > 0:
        n = r & 0x7f
        result |= n << (7 * i)
        r = r >> 8
        i += 1

    return result | tail


assert varint_encode(100) == 100
assert varint_encode(300) == 0b1000001000101100
assert varint_encode(65546) == 0b100001001000000000001010
assert varint_decode(0b100001001000000000001010) == 65546...

```
