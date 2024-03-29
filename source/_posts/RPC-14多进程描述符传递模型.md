---
title: RPC-14多进程描述符传递模型
date: 2018-09-13 10:54:00
tags: RPC
feature_img:
description: Node Cluster 为了解决负载均衡问题，它采用了不同的策略。它也是多进程并发模型，Master 进程会 fork 出多个子进程来处理客户端套接字。但是不存在竞争问题，因为负责 accept 套接字的只能是 Master 进程，Slave 进程只负责处理客户端套接字请求。那就存在一个问题，Master 进程拿到的客户端套接字如何传递给 Slave 进程。
keywords: RPC
categories: RPC
cover_img: http://qiniucdn.timilong.com/1543736975596.jpg
---

![tu](http://qiniucdn.timilong.com/1543736975596.jpg)

> 转载自: 掘金，[深入理解RPC: 基于Python自建分布式高并发RPC服务](https://juejin.im/book/5af56a3c518825426642e004)

### 简介
本节是补充内容，老师要给大家介绍一个比较特别的 RPC 服务器模型，这个模型不同于 Nginx、不同于 Redis、不同于 Apache、不同于 Tornado、不同于 Netty，它的原型是 Node Cluster 的多进程并发模型。

### Nginx 并发模型
我们知道 Nginx 的并发模型是一个多进程并发模型，它的 Master 进程在绑定监听地址端口后 fork 出了多个 Slave 进程共同竞争处理这个服务端套接字接收到的很多客户端连接。
![RPC](https://user-gold-cdn.xitu.io/2018/9/2/16599c91138fd139?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

这多个 Slave 进程会共享同一个处于操作系统内核态的套接字队列，操作系统的网络模块在处理完三次握手后就会将套接字塞进这个队列。这是一个生产者消费者模型，生产者是操作系统的网络模块，消费者是多个 Slave 进程，队列中的对象是客户端套接字。

这种模型在负载均衡上有一个缺点，那就是套接字分配不均匀，形成了类似于贫富分化的局面，也就是「闲者愈闲，忙者愈忙」的状态。这是因为当多个进程竞争同一个套接字队列时，操作系统采用了 LIFO 的策略，最后一个来 accept 的进程最优先拿到 套接字。越是繁忙的进程越是有更多的机会调用 accept，它能拿到的套接字也就越多。
![RPC](https://user-gold-cdn.xitu.io/2018/9/2/16599caa54c9cf6a?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### Node Cluster 并发模型
Node Cluster 为了解决负载均衡问题，它采用了不同的策略。它也是多进程并发模型，Master 进程会 fork 出多个子进程来处理客户端套接字。但是不存在竞争问题，因为负责 accept 套接字的只能是 Master 进程，Slave 进程只负责处理客户端套接字请求。那就存在一个问题，Master 进程拿到的客户端套接字如何传递给 Slave 进程。
![RPC](https://user-gold-cdn.xitu.io/2018/9/2/16599c93d60337bf?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

这时，神奇的 sendmsg 登场了。它是操作系统提供的系统调用，可以在不同的进程之间传递文件描述符。sendmsg 会搭乘一个特殊的「管道」将 Master 进程的套接字描述符传递到 Slave 进程，Slave 进程通过 recvmsg 系统调用从这个「管道」中将描述符取出来。这个「管道」比较特殊，它是 Unix 域套接字。普通的套接字可以跨机器传输消息，Unix 域套接字只能在同一个机器的不同进程之间传递消息。同管道一样，Unix 域套接字也分为有名套接字和无名套接字，有名套接字会在文件系统指定一个路径名，无关进程之间都可以通过这个路径来访问 Unix 域套接字。而无名套接字一般用于父子进程之间，父进程会通过 socketpair 调用来创建套接字，然后 fork 出来子进程，这样子进程也会同时持有这个套接字的引用。后续父子进程就可以通过这个套接字互相通信。

![RPC](https://user-gold-cdn.xitu.io/2018/9/2/16599c9ecb300f2d?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

注意这里的传递描述符，本质上不是传递，而是复制。父进程的描述符并不会在 sendmsg 自动关闭自动消失，子进程收到的描述符和父进程的描述符也不是同一个整数值。但是父子进程的描述符都会指向同一个内核套接字对象。

有了描述符的传递能力，父进程就可以将 accept 到的客户端套接字轮流传递给多个 Slave 进程，负载均衡的目标就可以顺利实现了。

接下来我们就是用 Python 代码来撸一遍 Node Cluster 的并发模型。因为 sendmsg 和 recvmsg 方法到了 Python3.5 才内置进来，所以下面的代码需要使用 Python3.5+才可以运行。

我们看 sendmsg 方法的定义：
```
socket.sendmsg(buffers[, ancdata[, flags[, address]]])
```

我们只需要关心第二个参数 ancdata，描述符是通过ancdata 参数传递的，它的意思是 「辅助数据」，而 buffers 表示需要传递的消息内容，因为消息内容这里没有意义，所以这个字段可以任意填写，但是必须要有内容，如果没有内容，sendmsg 方法就是一个空调用。

```
import socket, struct

def send_fds(sock, fd):
    return sock.sendmsg([b'x'], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack("i", fd))])
    
# ancdata 参数是一个三元组的列表，三元组的第一个参数表示网络协议栈级别 level，第二个参数表示辅助数据的类型 type，第三个参数才是携带的数据，level=SOL_SOCKET 表示传递的数据处于 TCP 协议层级，type=SCM_RIGHTS 就表示携带的数据是文件描述符。我们传递的描述符 fd 是一个整数，需要使用 struct 包将它序列化成二进制。
```

再看 recvmsg 方法的定义：
```
msg, ancdata, flags, addr = socket.recvmsg(bufsize[, ancbufsize[, flags]])...
```

同样，我们只需要关心返回的 ancdata 数据，它里面包含了我们需要的文件描述符。但是需要提供消息体的长度和辅助数据的长度参数。辅助数据的长度比较特殊，需要使用 CMSG_LEN 方法来计算，因为辅助数据里面还有我们看不到的额外的头部信息。
```
bufsize = 1  # 消息内容的长度
ancbufsize = socket.CMSG_LEN(struct.calcsize('i'))  # 辅助数据的长度
msg, ancdata, flags, addr = socket.recvmsg(bufsize, ancbufsize) # 收取消息
level, type, fd_bytes = ancdata[0] # 取第一个元祖，注意发送消息时我们传递的是一个三元组的列表
fd = struct.unpack('i', fd_bytes) # 反序列化...
```

### 代码实现
下面我来献上完整的服务器代码，为了简单起见，我们在 Slave 进程中处理 RPC 请求使用同步模型。
```
# coding: utf
# sendmsg recvmsg python3.5+才可以支持

import os
import json
import struct
import socket


def handle_conn(conn, addr, handlers):
    print(addr, "comes")
    while True:
        # 简单起见，这里就没有使用循环读取了
        length_prefix = conn.recv(4)
        if not length_prefix:
            print(addr, "bye")
            conn.close()
            break  # 关闭连接，继续处理下一个连接
        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length)
        request = json.loads(body)
        in_ = request['in']
        params = request['params']
        print(in_, params)
        handler = handlers[in_]
        handler(conn, params)

def loop_slave(pr, handlers):
    while True:
        bufsize = 1
        ancsize = socket.CMSG_LEN(struct.calcsize('i'))
        msg, ancdata, flags, addr = pr.recvmsg(bufsize, ancsize)
        cmsg_level, cmsg_type, cmsg_data = ancdata[0]
        fd = struct.unpack('i', cmsg_data)[0]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd)
        handle_conn(sock, sock.getpeername(), handlers)


def ping(conn, params):
    send_result(conn, "pong", params)


def send_result(conn, out, result):
    response = json.dumps({"out": out, "result": result}).encode('utf-8')
    length_prefix = struct.pack("I", len(response))
    conn.sendall(length_prefix)
    conn.sendall(response)

def loop_master(serv_sock, pws):
    idx = 0
    while True:
        sock, addr = serv_sock.accept()
        pw = pws[idx % len(pws)]
        # 消息数据，whatever
        msg = [b'x']
        # 辅助数据，携带描述符
        ancdata = [(
            socket.SOL_SOCKET,
            socket.SCM_RIGHTS,
            struct.pack('i', sock.fileno()))]
        pw.sendmsg(msg, ancdata)
        sock.close()  # 关闭引用
        idx += 1

def prefork(serv_sock, n):
    pws = []
    for i in range(n):
        # 开辟父子进程通信「管道」
        pr, pw = socket.socketpair()
        pid = os.fork()
        if pid < 0:  # fork error
            return pws
        if pid > 0:
            # 父进程
            pr.close()  # 父进程不用读
            pws.append(pw)
            continue
        if pid == 0:
            # 子进程
            serv_sock.close()  # 关闭引用
            pw.close()  # 子进程不用写
            return pr
    return pws

if __name__ == '__main__':
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind(("localhost", 8080))
    serv_sock.listen(1)
    pws_or_pr = prefork(serv_sock, 10)
    if hasattr(pws_or_pr, '__len__'):
        if pws_or_pr:
            loop_master(serv_sock, pws_or_pr)
        else:
            # fork 全部失败，没有子进程，Game Over
            serv_sock.close()
    else:
        handlers = {
            "ping": ping
        }
        loop_slave(pws_or_pr, handlers)

```

父进程使用 fork 调用创建了多个子进程，然后又使用 socketpair 调用为每一个子进程都创建一个无名套接字用来传递描述符。父进程使用 roundrobin 策略平均分配接收到的客户端套接字。子进程接收到的是一个描述符整数，需要将描述符包装成套接字对象后方可读写。打印对比发送和接收到的描述符，你会发现它们俩的值并不相同，这是因为 sendmsg 将描述符发送到内核后，内核给描述符指向的内核套接字又重新分配了一个新的描述符对象。

### 思考题

sendmsg/recvmsg 除了可以发送描述符外还可以用来干什么？
sendmsg/recvmsg 发送接收描述符在内核态具体是如何工作的?


