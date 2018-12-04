title: python-网络服务器
date: 2016-07-05 15:05:42
categories: python
tags: python
cover_img: http://qiniucdn.timilong.com/1543735249651.jpg
description: 本文介绍python的网络服务器。
---

![tu](http://qiniucdn.timilong.com/1543735249651.jpg)

### Python网络服务器
Python 的网络服务器有
* TCPServer 
* UDPServer
* UnixStreamServer
* UnixDatagramServer

### 服务器运行模式
* 多进程ForkingMixin
* 多线程ThreadingMixin

### 创建多进程模式的TCPServer
```python
class MyTCPServer(TCPServer, ForkingMixin):
    pass

```

### 创建多线程模式的UDPServer:
```python
class MyUDPServer(UDPServer, ThreadingMixin):
    pass

```
