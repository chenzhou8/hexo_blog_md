---
title: RPC-09多线程同步模型
date: 2018-09-13 10:50:30
tags: RPC
feature_img:
description: 多线程同步模型, 服务器可以并行处理多个客户端，每来一个新连接，则开启一个新的线程单独进行处理。每个线程都是同步读写客户端连接。
keywords: RPC
categories: RPC
cover_img: http://qiniucdn.timilong.com/1543735240334.jpg
---

![tu](http://qiniucdn.timilong.com/1543735240334.jpg)

> 转载自: 掘金，[深入理解RPC: 基于Python自建分布式高并发RPC服务](https://juejin.im/book/5af56a3c518825426642e004)

### 简介
上节我们编写了一个最简单的 RPC 服务器模型，简单到同时只能处理单个连接。本节我们为服务器增加多线程并发处理能力，同时可以处理多个客户端连接。后来的客户端连接再也不用排队了。这也是古典 RPC 服务最常见的处理模型。

既然要使用多线程，自然离不开 Python 内置的多线程编程库。我们在上节引出的 socket、struct 和 json 三个库的基础上再增加第四个内置库 thread，本节程序的多线程功能将由它来打开。

### thread
thread 是 Python 内置的线程库，用户可以使用 thread 库创建原生的线程。
```
def something_heavy(params):
    pass
    
thread.start_new_thread(something_heavy, (params,))
```

如果需要对线程进行更加精细的控制，那就需要使用到内置的 threading 类库，它是对线程更高级的抽象，类似于 Java 语言提供的 Thread 类。不过本节不需要使用。
![RPC](https://user-gold-cdn.xitu.io/2018/5/16/163686a461346432?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### 多进程同步模型
服务器可以并行处理多个客户端，每来一个新连接，则开启一个新的线程单独进行处理。每个线程都是同步读写客户端连接。

下面的代码同上节单线程同步模型代码的差别只有一行代码。为了更好的阅读体验，我们将完整的代码直接贴在下来。
```
# coding: utf8
# multithread.py

import json
import struct
import socket
import thread


def handle_conn(conn, addr, handlers):
    print addr, "comes"
    while True:  # 循环读写
        length_prefix = conn.recv(4)  # 请求长度前缀
        if not length_prefix:  # 连接关闭了
            print addr, "bye"
            conn.close()
            break  # 退出循环，退出线程
        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length)  # 请求消息体  
        request = json.loads(body)
        in_ = request['in']
        params = request['params']
        print in_, params
        handler = handlers[in_]  # 查找请求处理器
        handler(conn, params)  # 处理请求


def loop(sock, handlers):
    while True:
        conn, addr = sock.accept()
        thread.start_new_thread(handle_conn, (conn, addr, handlers))  # 开启新线程进行处理，就这行代码不一样


def ping(conn, params):
    send_result(conn, "pong", params)


def send_result(conn, out, result):
    response = json.dumps({"out": out, "result": result})
length_prefix = struct.pack("I", len(response))
    conn.sendall(length_prefix)
    conn.sendall(response)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(1)
    handlers = {
        "ping": ping
    }
    loop(sock, handlers)
```

当我们同时开启 2 个客户端时，从下面服务器的输出可以看出服务器确实是在并行处理多个连接：
```
bash>  python multithread.py
('127.0.0.1', 60181) comes
ping ireader 0
ping ireader 1
ping ireader 2
ping ireader 3
('127.0.0.1', 60188) comes
ping ireader 0
ping ireader 4
ping ireader 1
ping ireader 5
ping ireader 2
ping ireader 6
ping ireader 3
ping ireader 7
ping ireader 4
ping ireader 8
ping ireader 5
ping ireader 9
ping ireader 6
('127.0.0.1', 60181) bye
ping ireader 7
ping ireader 8
ping ireader 9
('127.0.0.1', 60188) bye
```

看到这里，读者们，你们应该感到激动，因为并发的潘多拉魔盒已经被你们打开了。并发的世界里丰富多彩，无数的高手在里面流连忘返。此刻，你们与编程高手的距离具体还差。。。。其实还是很远。

下一节我们要开始讲解多进程并发，哇哇，酷毙了，有没有。

多进程的魅力，Java 语言开发者多数是没有机会体验到的，他们通常只会使用多线程。

### 练习题
增加一个新的 RPC 服务，计算斐波那契级数。
增加一个新的 RPC 服务，提供 Redis 的缓存服务 API，可以在客户端使用 RPC 调用来进行缓存 key/value 的增删改操作。

