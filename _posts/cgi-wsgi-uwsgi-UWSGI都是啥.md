---
title: cgi_wsgi_uwsgi_UWSGI都是啥
cover_img: http://qiniucdn.timilong.com/1544683269405.jpg
date: 2018-12-25 10:26:29
tags: 网络
feature_img:
description: 浅谈CGI, WSGI, uwsgi, uWSGI
keywords: 网络
categories: 网络
---

![cover_img](http://qiniucdn.timilong.com/1544683269405.jpg)

## 介绍
CGI(Common Gateway Inteface): 字面意思就是`通用网关接口`，我觉得之所以看字面意思跟没看一样是因为这个称呼本身很学术，所以对于通俗的理解就存在一定困难，这里我觉得直接把 Gateway 当作 server 理解就好。

<b>它是外部应用程序与Web服务器之间的接口标准</b>

意思就是它用来<b>规定一个程序该如何与web服务器程序之间通信</b>从而可以让这个程序跑在web服务器上。

当然，CGI 只是一个很基本的协议，在现代常见的服务器结构中基本已经没有了它的身影，更多的则是它的扩展和更新。

在讲更进一步之前首先我们要了解目前比较常见的服务端结构：

假设我们使用 python 的 Django 框架写了一个网站，现在要将它挂在网上运行，我们一般需要：
```
nginx 做为代理服务器：负责静态资源发送（js、css、图片等）、动态请求转发以及结果的回复；
uWSGI 做为后端服务器：负责接收 nginx 请求转发并处理后发给 Django 应用以及接收 Django 应用返回信息转发给 nginx；
Django 应用收到请求后处理数据并渲染相应的返回页面给 uWSGI 服务器。
```

## 接下来的协议及接口就是应用在以上三者之间:

FastCGI: `CGI的一个扩展， 提升了性能，废除了 CGI fork-and-execute （来一个请求 fork 一个新进程处理，处理完再把进程 kill 掉）的工作方式，转而使用一种长生存期的方法，减少了进程消耗，提升了性能。`

这里 FastCGI 就应用于前端 server（nginx）与后端 server（uWSGI）的通信中，制定规范等等，让前后端服务器可以顺利理解双方都在说什么（当然 uWSGI 本身并不用 FastCGI, 它有另外的协议）


WSGI（Python Web Server GateWay Interface）: `它是用在 python web 框架编写的应用程序与后端服务器之间的规范（本例就是 Django 和 uWSGI 之间），让你写的应用程序可以与后端服务器顺利通信。`

在 WSGI 出现之前你不得不专门为某个后端服务器而写特定的 API，并且无法更换后端服务器，而 WSGI 就是一种统一规范， 所有使用 WSGI 的服务器都可以运行使用 WSGI 规范的 web 框架，反之亦然。


uWSGI: `是一个Web服务器，它实现了WSGI协议、uwsgi、http等协议。用于接收前端服务器转发的动态请求并处理后发给 web 应用程序。`

uwsgi: `是uWSGI服务器实现的独有的协议， 网上没有明确的说明这个协议是用在哪里的，我个人认为它是用于前端服务器与 uwsgi 的通信规范，相当于 FastCGI的作用。当然这只是个人见解，我在知乎进行了相关提问，欢迎共同讨论。`

简单来讲，这些名词的关系就是下图：

![cgi_wsgi_uwsgi_uWSGI](http://qiniucdn.timilong.com/cgi_wsgi_uwsgi_uWSGI.JPEG)

对于 CGI ，我认为在 CGI 制定的时候也许没有考虑到现代的架构，所以他只是一个通用的规范，而后来的 WSGI 也好 Fastcgi 也好等等这些都是在 CGI 的基础上扩展并应用于现代Web Server 不同地方的通信规范， 所以我在图中将 CGI 标注在整个流程之上。

做为一个 Python Web 开发者，相信以上流程我们最关注的莫过于 WSGI 这里所做的事，了解熟悉这里的规范不仅可以让我们更快速的开发 Web 应用同时我们也可以自己实现一个后端 Server 。
