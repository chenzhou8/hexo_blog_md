---
title: RPC-08单线程同步模型
date: 2018-09-13 10:50:06
tags: RPC
feature_img:
description: 单线程同步模型的服务器是最简单的服务器模型，每次只能处理一个客户端连接，其它连接必须等到前面的连接关闭了才能得到服务器的处理。否则发送过来的请求会悬挂住，没有任何响应，直到前面的连接处理完了才能继续。
keywords: RPC
categories: RPC
cover_img: http://qiniucdn.timilong.com/1543736719492.jpg
---

![tu](http://qiniucdn.timilong.com/1543736719492.jpg)

> 转载自: 掘金，[深入理解RPC: 基于Python自建分布式高并发RPC服务](https://juejin.im/book/5af56a3c518825426642e004)

### 简介

![RPC](https://user-gold-cdn.xitu.io/2018/6/11/163ef471eb6eaeba?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

如上图所示，现在我们开始使用代码来描述 RPC 的服务器模型，从简单变化到复杂，从经典变化到现代。考虑到教学上的简单性，我们使用 Python 语言进行描述，同时为了方便读者理解核心理念，代码不宜过长，对其中不少细节之处做了简化处理，还请读者理解。

另，如果读者缺少网络编程的基础知识，阅读后续代码可能会有障碍。建议读者先寻找相关的文章补充一下基础知识。

### 项目源代码地址

本小册的所有实战代码可以在 [Github](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fpyloque%2Fjuejin_rpc_py) 上直接下载运行使用。运行代码需要 Linux 或者 Mac 运行环境，如果读者使用的是 Windows，可以考虑使用虚拟机或者安装 Docker。

![RPC](https://user-gold-cdn.xitu.io/2018/6/3/163c484ed0ee0367?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

本节我们会主要讲解以下内容：
> 使用三个非常重要的 Python 内置的库，它们分别是 socket、struct 和 json，分别承担 RPC 服务的网络通信功能、字节转换功能和消息序列化功能。
> 网络通信的内容是字节序列，消息序列化的目标是将 Python 的数据结构转换成字节序列，而用于界定消息边界的消息长度也是消息的一部分，它需要将 Python 的整形转换成字节数组，这部分工作是由 struct 库来完成。

### socket

Python 有内置的网络编程类库，方便用户编写 tcp/udp 相关的代码。两个不同机器的进程需要通信时，可以通过 socket 来传输数据。
```
# 套接字客户端大致 API，参数略
sock = socket.socket()  # 创建一个套接字
sock.connect()  # 连接远程服务器
sock.recv() # 读
sock.send()  # 尽可能地写
sock.sendall()  # 完全写
sock.close()  # 关闭
```

注意send和sendall方法的区别，在网络状况良好的情况下，这两个方法几乎没有区别。但是需要特别注意的是send方法有可能只会发送了部分内容，它通过返回值来指示实际发出去了多少内容。而sendall方法是对send方法的封装，它考虑了这个情况，如果第一次send方法发送不完全，就会尝试第二次第三次循环发送直到全部内容都发送出去了或者中间出了错误才会返回。后续所有调用我们都会使用sendall方法。


```
# 套接字服务器大致 API，参数略
sock = socket.socket()  # 创建一个服务器套接字
sock.bind()  # 绑定端口
sock.listen()  # 监听连接
sock.accept()  # 接受新连接
sock.close()  # 关闭服务器套接字
```

### struct

Python 内置的二进制解码编码库，用于将各种不同的类型的字段编码成二进制字节串。类似于 java 语言的 bytebuffer 可以将各种不同类型的字段内容编码成 byte 数组。我们通过 struct 包将消息的长度整数编码成 byte 数组。
```
value_in_bytes = struct.pack("I", 1024)  # 将一个整数编码成 4 个字节的字符串
value, = struct.unpack("I", value_in_bytes)  # 将一个 4 字节的字符串解码成一个整数
# 注意等号前面有个逗号，这个非常重要，它不是笔误。
# 因为 unpack 返回的是一个列表，它可以将一个很长的字节串解码成一系列的对象。
# value 取这个列表的第一个对象。
```

### json
Python 内置的 json 序列化库。它可以将内存的对象序列化成 json 字符串，也可以将字符串反序列化成 Python 对象。它的序列化性能不高，但是使用方便直观。
```
raw = json.dumps({"hello": "world"})  # 序列化
po = json.loads(raw)  # 反序列化
```

### 消息协议
我们将使用长度前缀法来确定消息边界，消息体使用 json 序列化。

每个消息都有相应的名称，请求的名称使用 in 字段表示，请求的参数使用 params 字段表示，响应的名称是 out 字段表示，响应的结果用 result 字段表示。

我们将请求和响应使用 json 序列化成字符串作为消息体，然后通过 Python 内置的 struct 包将消息体的长度整数转成 4 个字节的长度前缀字符串。
```
// 输入
{
    in: "ping",
    params: "ireader 0"
}

// 输出
{
    out: "pong",
    result: "ireader 0"
}
```

### 客户端代码

后续使用的客户端代码是通用的，它适用于演示所有服务器模型。它的过程就是向服务器连续发送 10 个 RPC 请求，并输出服务器的响应结果。它使用约定的长度前缀法对请求消息进行编码，对响应消息进行解码。如果要演示多个并发客户端进行 RPC 请求，那就启动多个客户端进程。

```
# coding: utf-8
# client.py

import json
import time
import struct
import socket


def rpc(sock, in_, params):
    request = json.dumps({"in": in_, "params": params})  # 请求消息体
    length_prefix = struct.pack("I", len(request)) # 请求长度前缀
    sock.sendall(length_prefix)
    sock.sendall(request)
    length_prefix = sock.recv(4)  # 响应长度前缀
    length, = struct.unpack("I", length_prefix)
    body = sock.recv(length) # 响应消息体
    response = json.loads(body)
    return response["out"], response["result"]  # 返回响应类型和结果

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    for i in range(10): # 连续发送 10 个 rpc 请求
        out, result = rpc(s, "ping", "ireader %d" % i)
        print out, result
        time.sleep(1)  # 休眠 1s，便于观察
    s.close() # 关闭连接
```

![RPC](https://user-gold-cdn.xitu.io/2018/5/16/163680245ad03253?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

值得注意的是代码中有两个地方调用了socket.recv方法来读取期望的消息，通过传入一个长度值来获取想要的字节数组。实际上这样使用是不严谨的，甚至根本就是错误的。

socket.recv(int)默认是阻塞调用，不过这个阻塞也是有条件的。如果内核的套接字接收缓存是空的，它才会阻塞。只要里面有哪怕只有一个字节，这个方法就不会阻塞，它会尽可能将接受缓存中的内容带走指定的字节数，然后就立即返回，而不是非要等待期望的字节数全满足了才返回。这意味着我们需要尝试循环读取才能正确地读取到期望的字节数。
```
def receive(sock, n):
    rs = []  # 读取的结果
    while n > 0:
        r = sock.recv(n)
        if not r:  # EOF
            return rs
        rs.append(r)
        n -= len(r)
    return ''.join(rs)
```

但是为了简单起见，我们后面的章节代码都直接使用socket.recv，在开发环境中网络延迟的情况较少发生，一般来说很少会遇到recv方法一次读不全的情况发生。

### 单线程同步模型服务器代码
单线程同步模型的服务器是最简单的服务器模型，每次只能处理一个客户端连接，其它连接必须等到前面的连接关闭了才能得到服务器的处理。否则发送过来的请求会悬挂住，没有任何响应，直到前面的连接处理完了才能继续。

服务器根据 RPC 请求的 in 字段来查找相应的 RPC Handler 进行处理。例子中只展示了 ping 消息的处理器。如果你想支持多种消息，可以在代码中增加更多的处理器函数，并将处理器函数注册到全局的 handlers 字典中。
```
# coding: utf8
# blocking_single.py

import json
import struct
import socket


def handle_conn(conn, addr, handlers):
    print addr, "comes"
    while True:  # 循环读写
        length_prefix = conn.recv(4)  # 请求长度前缀
        if not length_prefix:  # 连接关闭了
            print addr, "bye"
            conn.close()
            break  # 退出循环，处理下一个连接
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
        conn, addr = sock.accept()  # 接收连接
        handle_conn(conn, addr, handlers)  # 处理连接


def ping(conn, params):
    send_result(conn, "pong", params)


def send_result(conn, out, result):
    response = json.dumps({"out": out, "result": result})  # 响应消息体
    length_prefix = struct.pack("I", len(response))  # 响应长度前缀
conn.sendall(length_prefix)
    conn.sendall(response)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个 TCP 套接字
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 打开 reuse addr 选项
    sock.bind(("localhost", 8080)) # 绑定端口
    sock.listen(1)  # 监听客户端连接
    handlers = {  # 注册请求处理器
        "ping": ping
    }
    loop(sock, handlers)  # 进入服务循环
```

服务器运行效果:
```
bash>  Python blocking_single.py
('127.0.0.1', 58417) comes
ping ireader 0
ping ireader 1
ping ireader 2
ping ireader 3
ping ireader 4
ping ireader 5
ping ireader 6
ping ireader 7
ping ireader 8
ping ireader 9
('127.0.0.1', 58417) bye
```

客户端运行效果
```
bash> Python client.py
pong ireader 0
pong ireader 1
pong ireader 2
pong ireader 3
pong ireader 4
pong ireader 5
pong ireader 6
pong ireader 7
pong ireader 8
pong ireader 9
```

如果在上一个客户端运行期间，再开一个新的客户端，会看到新的客户端没有任何输出。直到前一个客户端运行结束，输出才开始显示出来。因为服务器是串行地处理客户端连接。

这样的服务器毫无疑问肯定是不会有人用的，如果你家的服务器只能服务一个客户，其它人都得排队，这不是要把人家活活急死么。

所以，下一节我们将介绍服务器神奇的并发能力。

### 作业
本节布置一个难度系数较高的作业，请读者实现 Redis 协议的编码和解码。为了完成这个作业，建议读者先去温习一下前面章节学习的 Redis 协议格式。

不必惧怕困难，越是困难的事情，完成了就越有成就感。

