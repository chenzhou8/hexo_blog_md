---
title: Thrift-工作流程
date: 2018-10-17 17:45:12
tags: RPC
cover_img: http://qiniucdn.timilong.com/1542968639754.jpg
feature_img:
description: 简单介绍下Thrift RPC的工作过程。
keywords: RPC 
categories: RPC
---

![tu](http://qiniucdn.timilong.com/1542968639754.jpg)

## 工作流程

Thrift框架的远程过程调用的工作过程如下：

(1) 通过IDL定义一个接口的thrift文件，然后通过thrift的多语言编译功能，将接口定义的thrift文件翻译成对应的语言版本的接口文件；

(2) Thrift生成的特定语言的接口文件中包括客户端部分和服务器部分；

(3) 客户端通过接口文件中的客户端部分生成一个Client对象，这个客户端对象中包含所有接口函数的存根实现，然后用户代码就可以通过这个Client对象来调用thrift文件中的那些接口函数了，但是，客户端调用接口函数时实际上调用的是接口函数的本地存根实现;

(4) 接口函数的存根实现将调用请求发送给thrift服务器端，然后thrift服务器根据调用的函数名和函数参数，调用实际的实现函数来完成具体的操作;

(5) Thrift服务器在完成处理之后，将函数的返回值发送给调用的Client对象；

(6) Thrift的Client对象将函数的返回值再交付给用户的调用函数。

## 说明
(1) 本地函数的调用方和被调方在同一进程的地址空间内部，因此在调用时cpu还是由当前的进程所持有，只是在调用期间，cpu去执行被调用函数，从而导致调用方被卡在那里，直到cpu执行完被调用函数之后，才能切换回来继续执行调用之后的代码；

(2) RPC在调用方和被调用方一般不在一台机子上，它们之间通过网络传输进行通信，一般的RPC都是采用tcp连接，如果同一条tcp连接同一时间段只能被一个调用所独占，这种情况与[1]中的本地过程更为相似，这种情况是同步调用，很显然，这种方式通信的效率比较低，因为服务函数执行期间，tcp连接上没有数据传输还依然被本次调用所霸占；另外，这种方式也有优点：实现简单。

(3) 在一些的RPC服务框架中，为了提升网络通信的效率，客户端发起调用之后不被阻塞，这种情况是异步调用，它的通信效率比同步调用高，但是实现起来比较复杂。

