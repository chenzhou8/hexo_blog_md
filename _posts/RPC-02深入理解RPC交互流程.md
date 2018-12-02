---
title: RPC_02深入理解RPC交互流程
date: 2018-09-05 09:48:04
categories: RPC
tags: RPC
feature_img:
description: RPC 是两个子系统之间进行的直接消息交互，它使用操作系统提供的套接字来作为消息的载体，以特定的消息格式来定义消息内容和边界。 RPC 的客户端通过文件描述符的读写 API (read & write) 来访问操作系统内核中的网络模块为当前套接字分配的发送 (send buffer) 和接收 (recv buffer) 缓存。
keywords: RPC
cover_img: http://qiniucdn.timilong.com/154373677120.jpg

---

> 转载自: 掘金，[深入理解RPC: 基于Python自建分布式高并发RPC服务](https://juejin.im/book/5af56a3c518825426642e004)

### RPC本质

本节我们开始讲解 RPC 的消息交互流程，目的是搞清楚一个简单的 RPC 方法调用背后究竟发生了怎样复杂曲折的故事，以看透 RPC 的本质。

![RPC](https://user-gold-cdn.xitu.io/2018/6/5/163cf789da84cb53?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
上图是信息系统交互模型宏观示意图，RPC 的消息交互则会深入到底层。

RPC 是两个子系统之间进行的直接消息交互，它使用操作系统提供的套接字来作为消息的载体，以特定的消息格式来定义消息内容和边界。

RPC 的客户端通过文件描述符的读写 API (read & write) 来访问操作系统内核中的网络模块为当前套接字分配的发送 (send buffer) 和接收 (recv buffer) 缓存。


### RPC消息流程

![RPC](https://user-gold-cdn.xitu.io/2018/5/31/163b4dcf06e0a780?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

如上图所示，左边的客户端进程写 RPC 指令消息到内核的发送缓存中，内核将发送缓存中的数据传送到物理硬件 NIC，也就是网络接口芯片 (Network Interface Circuit)。NIC 负责将翻译出来的模拟信号通过网络硬件传递到服务器硬件的 NIC。服务器的 NIC 再将模拟信号转成字节数据存放到内核为套接字分配的接收缓存中，最终服务器进程从接收缓存中读取数据即为源客户端进程传递过来的 RPC 指令消息。

消息从用户进程流向物理硬件，又从物理硬件流向用户进程，中间还经过了一系列的路由网关节点。

上图呈现的只是 RPC 一次消息交互的上半场，下半场是一个逆向的过程，从服务器进程向客户端进程返回响应数据。完整的一次 RPC 过程如下图所示：

![RPC](https://user-gold-cdn.xitu.io/2018/5/31/163b4e1f464cbdc2?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### Python 代码描述

下面用 Python 代码来描述上述过程。

- Server 端死循环监听本地 8080 端口，等待客户端的连接。
- 客户端启动时连接本地 8080 端口，紧接着发送词一个字符串 hello，然后等待服务器响应。
- 服务器接收到客户端连接后立即收取客户端发送过来的字符串，也就是 hello，打印出来。然后立即给对方回复一个字符串 world。
- 客户端接收到服务器发送过来的 world，马上打印出来。
- 关闭连接，结束。

```
# coding: utf-8
# server

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8080))
sock.listen(1)  # 监听客户端连接
while True:
    conn, addr = sock.accept()  # 接收一个客户端连接
    print conn.recv(1024)  # 从接收缓冲读消息 recv buffer
    conn.sendall("world")  # 将响应发送到发送缓冲 send buffer
    conn.close() # 关闭连接

# coding: utf-8
# client

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8080))  # 连接服务器
sock.sendall("hello")  # 将消息输出到发送缓冲 send buffer
print sock.recv(1024)  # 从接收缓冲 recv buffer 中读响应
sock.close() # 关闭套接字
```

如果从上面代码上观察，我们其实很难看出上图所示的复杂过程。浮现在多数人脑海中往往是下面的这幅简约模型图。相比之下它要简单很多，这也正是操作系统设计的魅力所在，让你时时刻刻都在使用它却感受不到它的存在。

![RPC](https://user-gold-cdn.xitu.io/2018/5/31/163b4e36daa5cc79?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### 小结

通过本节内容，读者们对 RPC 的交互流程应该有了大致了解，但是还并不知道 RPC 之间到底交互了什么。就好比你能看到远方有几个人在说话，但是不知道他们在说啥。


下一节我们将放大细节，仔细观察 RPC 客户端服务器之间窃窃私语了什么，它们究竟是在用什么外星语言交流。

### 练习题

一个很有趣的小测试实验 , 请读者编写代码实现以下情景:

客户端疯狂发送请求，但是服务器不读不处理，会发生什么？

> BrokenPipeError: [Errno 32] Broken pipe 这个错误不是表示客户端阻塞了。这个是因为服务器调用了conn.close()然后，服务器返回了reset，但是客户端没有去做处理（关闭连接），而是继续往服务器写入数据，导致了Broken pipe这个异常

> 答案: socket缓冲区堆满 一直阻塞下去

>  1. 如果接收和发送队列没有设置大小，服务器处理能力弱，tcp会动态调整直至耗尽整个内存。2. 设置了大小，那么socket会出现阻塞，不接受发送端的消息。3. 如果发送的请求size大于发送和接收队列之和，那么会一直阻塞下去


