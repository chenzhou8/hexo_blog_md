---
title: RPC-12单进程异步模型
date: 2018-09-13 10:53:21
tags: RPC
feature_img:
description: 本小节我们开始讲 RPC 的异步模型。异步模型是现代服务器的通用模型，它比古典的同步模型在效率上要高出一大截，但是编程难度上也要加大不少，需要程序员有较高的编程素养。关于如何应用异步模型，我们 需要要先从非阻塞 IO 开始讲起，逐步理解基本原理和必备的工具和库之后，再用代码实现。
keywords: RPC
categories: RPC
cover_img: http://qiniucdn.timilong.com/1543736749689.jpg
---

![tu](http://qiniucdn.timilong.com/1543736749689.jpg)

> 转载自: 掘金，[深入理解RPC: 基于Python自建分布式高并发RPC服务](https://juejin.im/book/5af56a3c518825426642e004)

### 简介
本小节我们开始讲 RPC 的异步模型。异步模型是现代服务器的通用模型，它比古典的同步模型在效率上要高出一大截，但是编程难度上也要加大不少，需要程序员有较高的编程素养。关于如何应用异步模型，我们需要要先从非阻塞 IO 开始讲起，逐步理解基本原理和必备的工具和库之后，再用代码实现。


### 非阻塞 IO

操作系统提供的文件读写操作默认都是同步的，它必须等到数据就绪后才能返回，如果数据没有就绪，它就会阻塞当前的线程，其它的事什么都干不了，这是对操作系统线程资源的一种浪费。

为了解决这个问题，操作系统给文件读写提供了非阻塞选项。当我们读写文件时，提供一个 O_NONBLOCK 选项，读写操作就不会阻塞。

内核套接字的 ReadBuffer 有多少字节，read 操作就返回多少字节。内核套接字的 WriteBuffer 有多少剩余字节空间，write 操作就写多少字节。我们通过读写的返回值就可以知道读写了多少数据。接下来线程就可以继续干别的事去了，稍后再继续进行读写。
```
socket = socket.socket()
socket.setblocking(0)  # 开启非阻塞模式
socket.read()  # 有多少读多少
socket.write()  # 能写多少是多少
```

### 事件轮询
非阻塞 IO 看起来很有用，但是有个问题，我们该如何知道某个套接字可读可写呢？如果我们反复去使用 read 和 write 去轮询 IO，这似乎挺费劲的，假设一个套接字长期闲置没有消息到来，结果还要调用成千上万次的 read，这是明显的在浪费 CPU 嘛。

#### 如何应对这种困境呢？

操作系统提供了事件轮询的 API。我们使用这个 API 来查询相关套接字是否有相应的读写事件，如果有的话该 API 会立即携带事件列表返回，如果没有事件，该 API 会阻塞，阻塞多长时间可以通过参数设置。阻塞看起来似乎不太好，但是如果服务器没什么事可以干，那睡大觉就是节省资源的最佳方式。

调用事件轮询 API 拿到读写事件后，就可以接着对事件相关的套接字进行读写操作了，这个时候读写操作都是正常进行的，而不会浪费 CPU 空读空写。
```
read_events, write_events = select.select(read_fds, write_fds, timeout)
for event in read_events:
    handle_read(event)
for event in write_events:
    handle_write(event)
```

现代操作系统往往都提供了多种事件轮询 API，从古典的 select 和 poll 系统调用进化到如今的 epoll 和 kqueue 系统调用。古典的使用简单，性能差，现代的使用复杂，性能超好。
![RPC](https://user-gold-cdn.xitu.io/2018/5/11/1634e0e657a73708?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

我们看到轮询 API 的参数是文件描述符列表。网络套接字的 socket 对象如何跟轮询 API 产生关联的呢？这个要归功于操作系统的抽象能力，操作系统将所有的 IO 操作都抽象成了文件操作，网络套接字的 socket 对象提供了 makefile 函数，可以获取对应的文件描述符对象。

一个完整的事件循环除了要处理 IO 相关的事件外，还有一些内部的事件需要处理，比如定时任务。

Nginx/Redis/Java NIO 和各种 Web 服务器都使用了事件轮询 API，它是高性能高并发的关键技术之一。

### 用户进程读写缓冲区
因为读是非阻塞的，意味着当我们想要读取 100 个字节时，我们可能经历了多次 read 调用，第一次读了 10 个字节，第二次读了 30 个字节，然后又读了 80 个字节。凑够了 100 个字节时，我们就可以解码出一个完整的请求对象进行处理了，还剩余的 20 个字节又是后面请求消息的一部分。这就是所谓的半包问题。

非阻塞 IO 要求用户程序为每个套接字维持一个 ReadBuffer，它和操作系统内核区的 ReadBuffer 不是同一个东西。用户态的 ReadBuffer 是由用户代码来进行控制。它的作用就是保留当前的半包消息，如果消息的内容完整了，就可以从 ReadBuffer 中取出来进行处理。

因为写是非阻塞的，意味着当我们想要写 100 个字节时，我们可能经历了多次 write 调用，第一次 write 了 10 个字节，第二次 write 了 30 个字节，最后才把剩余的 40 个字节写出去了。这就要求用户程序为每个套接字维护一个写缓冲区，把剩下的没写完的字节都放在里面，以便后续可写事件到来时，能继续把没写完的写下去。

### StringIO
Python 内置的类库，类似于 Java 的 ByteArrayInputStream 和 ByteArrayOutputStream 的合体，将字符串当成一个文件一样使用，具备和文件一样的 read 和 write 操作。Python 提供了两个实现，一个是纯 Python 实现 StringIO，一个是底层 C 的实现 cStringIO。毫无疑问，C 的实现要快很多。用户进程读写缓冲区使用 StringIO 实现。
```
from StringIO import StringIO  # 纯 python 的实现
from cStringIO import StringIO  # C 实现

s = StringIO()
s.write("hello, ireader")
s.seek(0)
s.read(1024)
```

###  asyncore
Python 内置的异步 IO 库。考虑到编写原生的事件轮询和异步读写的逻辑比较复杂，要考虑的细节非常多。所以 Python 对这一块的逻辑代码做了一层封装，简化了异步逻辑的处理，使用起来非常方便。asyncore负责socket事件轮询，用户编写代码时只需要提供回调方法即可，asyncore会在相应的事件到来时，调用用户提供的回调方法。比如当serversocket的read事件到来时，会自动调用handle_accept方法， 当socket的read事件到来时，调用handle_read方法。

### 实现单进程异步模型
接下来我们使用 Python 内置的 asyncore 模块，实现一个异步模型的 RPC 服务器。

```
# coding: utf8

import json
import struct
import socket
import asyncore
from cStringIO import StringIO


class RPCHandler(asyncore.dispatcher_with_send):  # 客户套接字处理器必须继承 dispatcher_with_send

    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock=sock)
        self.addr = addr
        self.handlers = {
            "ping": self.ping
        }
        self.rbuf = StringIO()  # 读缓冲区由用户代码维护，写缓冲区由 asyncore 内部提供

    def handle_connect(self):  # 新的连接被 accept 后回调方法
        print self.addr, 'comes'

    def handle_close(self):  # 连接关闭之前回调方法
        print self.addr, 'bye'
        self.close()

    def handle_read(self):  # 有读事件到来时回调方法
        while True:
            content = self.recv(1024)
            if content:
                self.rbuf.write(content)
            if len(content) < 1024:
                break
        self.handle_rpc()

    def handle_rpc(self):  # 将读到的消息解包并处理
        while True:  # 可能一次性收到了多个请求消息，所以需要循环处理
            self.rbuf.seek(0)
            length_prefix = self.rbuf.read(4)
            if len(length_prefix) < 4:  # 不足一个消息
                break
            length, = struct.unpack("I", length_prefix)
            body = self.rbuf.read(length)
            if len(body) < length:  # 不足一个消息
                break
            request = json.loads(body)
            in_ = request['in']
            params = request['params']
            print in_, params
            handler = self.handlers[in_]
            handler(params)  # 处理消息
            left = self.rbuf.getvalue()[length + 4:]  # 消息处理完了，缓冲区要截断
            self.rbuf = StringIO()
            self.rbuf.write(left)
        self.rbuf.seek(0, 2)  # 将游标挪到文件结尾，以便后续读到的内容直接追加

    def ping(self, params):
        self.send_result("pong", params)

    def send_result(self, out, result):
        response = {"out": out, "result": result}
        body = json.dumps(response)
        length_prefix = struct.pack("I", len(body))
        self.send(length_prefix)  # 写入缓冲区
        self.send(body) # 写入缓冲区


class RPCServer(asyncore.dispatcher):  # 服务器套接字处理器必须继承 dispatcher

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            RPCHandler(sock, addr)


if __name__ == '__main__':
    RPCServer("localhost", 8080)
    asyncore.loop()

```

最后一行代码`asyncore.loop()` 启动事件循环，所谓事件循环就是轮询事件并处理，处理完了再继续轮询，没完没了，天荒地老。

reuse_addr 选项如此常见，所以 asyncore 单独为它提供了一个方法便于用户使用。

我们使用了 StringIO 作为读缓冲，用于缓存半包消息和刚刚从套接字那里读取到的字节数据。消息处理完毕之后要对读缓冲进行截断处理，将已经处理的字节数据砍掉。StringIO 的读写游标要小心使用，读的时候游标从头开始，写的时候游标从尾部开始追加，seek 函数用来移动游标。

服务器套接字不同于客户套接字，服务套接字的可读事件是指有新连接来了，它没有相应的可写事件。服务器套接字的读操作就是调用 accept 获取新连接。...

### 小结
这一节你们见识到的异步模型就是现代的模型，你们所听说的 Nginx/Nodejs/Redis 就是基于异步模型构建出来的。只不过人家用的是 C 语言，性能上高出了几个数量级。
异步模型的性能要比同步好太多，但是也有缺点，就是会增加编程难度，理解起来也不及同步模型来的直观，对程序员的要求会比较高。

所以，在公司的业务流程代码中，多半采用同步模型，仅仅是在特别讲究高并发高性能的场合才会用到异步模型。异步模型编码成本高，容易出错，一定慎用！

本节讲的单进程异步模型，最多只能榨干一个 CPU。下节我们使用多进程异步模型，这个模型可以将所有的 CPU 统统榨干，就问你怕不怕？

