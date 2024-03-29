---
title: Connection reset by peer的错误分析
date: 2018-10-16 10:33:31
tags: Socket
categories: Socket
description: 我在用Thrift进行Python后端服务开发时，在客户端并发量并不大的情况下，日志报警Connection reset by peer错误很频繁，经过大量google后，对此错误可能情况进行一个记录。
cover_img: http://qiniucdn.timilong.com/1543736774757.jpg
---

![tu](http://qiniucdn.timilong.com/1543736774757.jpg)

## Connection reset by peer出现的原因
该异常在客户端和服务器端均有可能发生，引起该异常的原因有两个，第一个就是如果一端的Socket被关闭（或主动关闭或者因为异常退出而引起的关闭），另一端仍发送数据，发送的第一个数据包引发该异常 (Connect reset by peer)。

另一个是一端退出，但退出时并未关闭该连接，另一端如果在从连接中读数据则抛出该异常（Connection reset）。简单的说就是在连接断开后的读和写操作引起的。 

### 服务器并发链接数超过其承载量
服务器的并发连接数超过了其承载量，服务器会将其中一些连接关闭； 如果知道实际连接服务器的并发客户数没有超过服务器的承载量，看下有没有网络流量异常。可以使用netstat -an查看网络连接情况。 

### 客户端关闭socket, 而服务端还在给客户端发送数据
由于某些原因，比如客户端设置了超时机制，提前关闭了tcp链接的socket，导致服务端在处理完请求，返回data时，找不到对应的socket，则会引起此错误。

### 网络防火墙的问题
 如果网络连接通过防火牆，而防火牆一般都会有超时的机制，在网络连接长时间不传输数据时，会关闭这个TCP的会话，关闭后在读写，就会导致异常。 如果关闭防火牆，解决了问题，需要重新配置防火牆，或者自己编写程序实现TCP的长连接。实现TCP的长连接，需要自己定义心跳协议，每隔一段时间，发送一次心跳协议，双方维持连接。

### errno 104:connetction reset by peer
> 转载自CSDN: https://blog.csdn.net/zjk2752/article/details/21236725

errno = 104错误表明你在对一个对端socket已经关闭的的连接调用write或send方法，在这种情况下，调用write或send方法后，对端socket便会向本端socket发送一个RESET信号，在此之后如果继续执行write或send操作，就会得到errno为104，错误描述为connection reset by peer。

出现这种问题的很大一部分原因，至少我遇到的几次全都是，发送端和接收端事先约定好的数据长度不一致导致的，接收端被通知要收的数据长度小于发送端实际要发送的数据长度。

比如接收端被通知要收1024个字节，但发送端却发了1025（可以是字符串末尾隐含的结束符），这样一来，接收端收完1024就执行了close操作，如果发送端再继续发送，接收端协议就会向发送端返回一个RESET信号，RESET信号可以抓包看到，如下所示：
![图](http://qiniucdn.timilong.com/20140314151927578.jpeg)

具体的分析可以结合TCP的"四次握手"关闭. TCP是全双工的信道, 可以看作两条单工信道, TCP连接两端的两个端点各负责一条。 

当对端调用close时, 虽然本意是关闭整个两条信道, 但本端只是收到FIN包. 按照TCP协议的语义, 表示对端只是关闭了其所负责的那一条单工信道, 仍然可以继续接收数据。

也就是说, 因为TCP协议的限制, 一个端点无法获知对端的socket是调用了close还是shutdown.

对于一个TCP连接，如果对端执行close操作，则会向本端发送一个FIN分节，这时候读本端socket会返回0，我们就知道对方已经关闭了连接，通常这时候我们会在本地调用close来主动关闭本端连接。

但如果对方socket已经执行了close的操作，本端socket还继续在这个连接上写数据，就会触发对端socket发送RST报文，按照TCP的四次握手原理，这时候本端socket应该也要开始执行close的操作流程了，而不是接着发数据.
