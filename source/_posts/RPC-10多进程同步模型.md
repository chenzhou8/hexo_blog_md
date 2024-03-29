---
title: RPC-10多进程同步模型
date: 2018-09-13 10:52:37
tags: RPC
feature_img:
description: fork 调用将生成一个子进程，所以这个函数会在父子进程同时返回。在父进程的返回结果是一个整数值，这个值是子进程的进程号，父进程可以使用该进程号来控制子进程的运行。fork 在子进程的返回结果是零。如果 fork 返回值小于零，一般意味着操作系统资源不足，无法创建进程。
keywords: RPC
categories: RPC
cover_img: http://qiniucdn.timilong.com/1543735454132.jpg
---

![tu](http://qiniucdn.timilong.com/1543735454132.jpg)

> 转载自: 掘金，[深入理解RPC: 基于Python自建分布式高并发RPC服务](https://juejin.im/book/5af56a3c518825426642e004)

### 简介
上节我们完成了一个简单的多线程服务器，可以并发处理多个客户端连接。但是 Python 里多线程使用的并不常见，因为 Python 的 GIL 致使单个进程只能占满一个 CPU 核心，多线程并不能充分利用多核的优势。所以多数 Python 服务器推荐使用多进程模型。我们将使用 Python 内置的 os.fork() 创建子进程。

### os.fork()
Python 内置的子进程创建函数，它封装了 glibc 提供的 fork 函数。

fork 调用将生成一个子进程，所以这个函数会在父子进程同时返回。在父进程的返回结果是一个整数值，这个值是子进程的进程号，父进程可以使用该进程号来控制子进程的运行。fork 在子进程的返回结果是零。如果 fork 返回值小于零，一般意味着操作系统资源不足，无法创建进程。

我们可以通过 fork 调用的返回值来区分当前的进程是父进程还是子进程。
```
pid = os.fork()
if pid > 0:
    # in parent process
if pid == 0:
    # in child process
if pid < 0:
    # fork error
```

子进程创建后，父进程拥有的很多操作系统资源，子进程也会持有。比如套接字和文件描述符，它们本质上都是对操作系统内核对象的一个引用。如果子进程不需要某些引用，一定要即时关闭它，避免操作系统资源得不到释放导致资源泄露。

![RPC](https://user-gold-cdn.xitu.io/2018/5/16/163686aa96c93a39?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### 多进程同步模型
子进程创建容易，销毁难。当子进程退出后，父进程需要使用 waitpid 系统调用收割子进程，否则子进程将成为僵尸进程，僵尸进程会持续占据操作系统的资源直到父进程退出后被 init 进程接管收割后才会消失释放资源。收割子进程的逻辑处理有一定的复杂度，涉及到非常精细的信号控制逻辑。从理解核心重点角度出发，这部分本节就不做详细讲解。

```
# coding: utf8
# multiprocess.py

import os
import json
import struct
import socket
import multiprocessing


def handle_conn(conn, addr, handlers):
    print addr, "comes"
    while True:
        length_prefix = conn.recv(4)
        if not length_prefix:
            print addr, "bye"
            conn.close()
            break
        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length)
        request = json.loads(body)
        in_ = request['in']
        params = request['params']
        print in_, params
        handler = handlers[in_]
        handler(conn, params)

def loop(sock, handlers):
    while True:
        conn, addr = sock.accept()
        pid = os.fork()  # 好戏在这里，创建子进程处理新连接
        if pid < 0:  # fork error
            return
        if pid > 0:  # parent process
            conn.close()  # 关闭父进程的客户端套接字引用
            continue
        if pid == 0:
            sock.close()  # 关闭子进程的服务器套接字引用
            handle_conn(conn, addr, handlers)
            break  # 处理完后一定要退出循环，不然子进程也会继续去 accept 连接


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

注意，我们在子进程里关闭了服务器的套接字，同样在父进程里关闭了客户端的套接字。为什么要这么做呢？...
![RPC](https://user-gold-cdn.xitu.io/2018/7/10/16482e1557af155e?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

因为进程 fork 之后，套接字会复制一份到子进程，这时父子进程将会各有自己的套接字引用指向内核的同一份套接字对象，套接字的引用计数为2。

![RPC](https://user-gold-cdn.xitu.io/2018/7/10/16482e6f7ae7ce4e?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

对套接字进程 close，并不是说就是关闭套接字，其本质上只是将内核套接字对象的引用计数减一。只有当引用计数减为零时，才会关闭套接字。
如果没有上述逻辑就会导致服务器套接字引用计数不断增长，同时客户端套接字对象也得不到即时回收，这便是传说中的资源泄露。

### 多进程 vs 多线程
如果将 IT 服务比喻成工厂的话，多线程就好比同一个工厂的多名工人并行工作。而多进程则是多个工厂同时进行生产。同一个工厂内部的工人之间有很多的工具可以共享，但是跨越了工厂的工人之间就完全隔离了，它们都使用着各自独立的全套资源。

### 小结
也许很多读者看了这一节会很不适应，尼玛多进程编程第一次遇到啊，从来没见过啊，好神奇啊。

### 练习
多线程服务器见过了，多进程服务器也见过了，但是还没见过既是多进程又是多线程的服务器。

请读者稍加改造，将 RPC 服务改成高大上的「多进程嵌套多线程」服务。是不是更 6 了？

