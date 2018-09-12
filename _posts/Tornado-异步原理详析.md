---
title: Tornado-异步原理详析
date: 2018-09-12 12:32:34
tags: Tronado
cover_img:
feature_img:
description: Tornado是一个用Python编写的异步HTTP服务器，同时也是一个web开发框架。 Tornado 优秀的大并发处理能力得益于它的 web server 从底层开始就自己实现了一整套基于 epoll 的单线程异步架构。
keywords: Tornado
categories: Tornado
---

> 转载自: 简书，[Tornado-异步原理详析](https://www.jianshu.com/p/de7f04e65618)

### Tornado是什么？
Tornado是一个用Python编写的异步HTTP服务器，同时也是一个web开发框架。
Tornado 优秀的大并发处理能力得益于它的 web server 从底层开始就自己实现了一整套基于 epoll 的单线程异步架构。

### 同步、异步编程差异
> 1. 对于同步阻塞型Web服务器，我们来打个比方，将它比作一间饭馆，而Web请求就是来这家饭馆里吃饭的客人。假设饭馆店里只有20个座位，那么同时能够就餐的客人数也就是20，剩下的客人被迫就在店门外等，如果客人们吃的太慢了，那么外面的客人等得不耐烦了，就会走掉（timeout）。

> 2. 对于异步非阻塞型服务器，我们打另一个比方，将它比作一家超市，客人们想进就能进，前往货架拿他们想要的货物，然后再去收银台结账（callback），假设，这家超市只有20个收银台，却可以同时满足成百上千人的购物需求。和购物的时间长度比起来，结账的时间基本可以忽略不计。

大部分Web应用都是阻塞性质的，也就是说当一个请求被处理时，这个进程就会被挂起直至请求完成。

假设你正在写一个需要请求一些来自其他服务器上的数据（比如数据库服务，调用其他http 接口获取数据）的应用程序，这几个请求假设需要花费5秒钟，大多数的web开发框架中处理请求的代码：
```
def handler_request(self, request):
    answ = self.remote_server.query(request) # 耗时5秒
    request.write_response(answ)
```

如果这些代码运行在单个线程中，你的服务器只能每5秒接收一个客户端的请求。在这5秒钟的时间里，服务器不能干其他任何事情，所以，你的服务效率是每秒0.2个请求， 这样的效率时不能接受。

大部分服务器会使用多线程技术来让服务器一次接收多个客户端的请求，我们假设你有20个线程，你将在性能上获得20倍的提高，所以现在你的服务器效率是每秒接受4个请求，但这还是太低了。
当然，你可以通过不断地提高线程的数量来解决这个问题，但是，线程在内存和调度方面的开销是昂贵的，大多数Linux发布版中都是默认线程堆大小为8MB。为每个打开的连接维护一个大的线程池等待数据极易迅速耗光服务器的内存资源。可能这种提高线程数量的方式将永远不可能达到每秒100个请求的效率。

如果使用异步IO(asynchronous IO AIO)，达到每秒上千个请求的效率是非常轻松的事情。服务器请求处理的代码将被改成这样：
```
def handler_request(self, request):
   self.remote_server.query_async(request, self.response_received)     
def response_received(self, request, answ):    #回调函数 耗时5秒
   request.write(answ)
```

AIO的思想是当我们在等待结果的时候不阻塞，转而我们给框架一个回调函数作为参数，让框架在收到结果的时候通过回调函数继续操作。这样，服务器就可以被解放去接受其他客户端的请求了。

### IO复用 Epoll
tornado.ioloop 就是 tornado web server 异步最底层的实现。
看 ioloop 之前，我们需要了解一些预备知识，有助于我们理解 ioloop。

ioloop 的实现基于 epoll ，那么什么是 epoll？ epoll 是Linux内核为处理大批量文件描述符而作了改进的 poll 。
那么什么又是 poll ？ 首先，我们回顾一下， socket 通信时的服务端，当它接受（ accept ）一个连接并建立通信后（ connection ）就进行通信，而此时我们并不知道连接的客户端有没有信息发完。 这时候我们有两种选择：

> 1. 一直在这里等着直到收发数据结束；
> 2. 每隔一定时间来看看这里有没有数据；

第一种办法虽然可以解决问题，但我们要注意的是对于一个线程\进程同时只能处理一个 socket 通信，其他连接只能被阻塞，显然这种方式在单进程情况下不现实。

第二种办法要比第一种好一些，多个连接可以统一在一定时间内轮流看一遍里面有没有数据要读写，看上去我们可以处理多个连接了，这个方式就是 poll / select 的解决方案。 看起来似乎解决了问题，但实际上，随着连接越来越多，轮询所花费的时间将越来越长，而服务器连接的 socket 大多不是活跃的，所以轮询所花费的大部分时间将是无用的。

为了解决这个问题， epoll 被创造出来，它的概念和 poll 类似，不过每次轮询时，他只会把有数据活跃的 socket 挑出来轮询，这样在有大量连接时轮询就节省了大量时间。

对于 epoll 的操作，其实也很简单，只要 4 个 API 就可以完全操作它。

#### epoll_create
用来创建一个 epoll 描述符（ 就是创建了一个 epoll ）

#### epoll_ctl
对epoll 事件操作，包括以下操作：
EPOLL_CTL_ADD 添加一个新的epoll事件
EPOLL_CTL_DEL 删除一个epoll事件
EPOLL_CTL_MOD 改变一个事件的监听方式

epoll监听的事件七种，而我们只需要关心其中的三种：
EPOLLIN 缓冲区满，有数据可读（read）
EPOLLOUT 缓冲区空，可写数据 （write）
EPOLLERR 发生错误 （error）

#### epoll_wait
就是让 epoll 开始工作，里面有个参数 timeout，当设置为非 0 正整数时，会监听（阻塞） timeout 秒；设置为 0 时立即返回，设置为 -1 时一直监听。
在监听时有数据活跃的连接时其返回活跃的文件句柄列表（此处为 socket 文件句柄）。

#### close
关闭 epoll


### IOLoop模块
让我们通过查看ioloop.py文件直接进入服务器的核心。这个模块是异步机制的核心。它包含了一系列已经打开的文件描述符（文件指针）和每个描述符的处理器（handlers）。它的功能是选择那些已经准备好读写的文件描述符，然后调用它们各自的处理器（一种IO多路复用的实现，select / epoll）。

可以通过调用add_handler()方法将一个socket加入IO循环中：
```
"""为文件描述符注册指定处理器(callback)，当文件描述指定的事件发生"""    
def add_handler(self, fd, handler, events):    
   self._handlers[fd] = handler   
   self._impl.register(fd, events | self.ERROR)
```

_handlers这个字典类型的变量保存着文件描述符（其实就是socket）到当该文件描述符准备好时需要调用的方法的映射（在Tornado中，该方法被称为处理器）。然后，文件描述符被注册到epoll列表中。Tornado关心三种类型的事件（指发生在文件描述上的事件）：READ，WRITE 和 ERROR。正如你所见，ERROR是默认为你自动添加的。

self._impl是select.epoll()和selet.select()两者中的一个

现在让我们来看看实际的主循环，这段代码被放在了start()方法中：
```
def start(self):
    """Starts the I/O loop.
    The loop will run until one of the I/O handlers calls stop(), which
    will make the loop stop after the current event iteration completes.
    """
    self._running = True
    while True: # 开始事件循环 Event Loop 
        [ ... ]
        if not self._running:
            break
        [ ... ]
        try:
            event_pairs = self._impl.poll(poll_timeout)  # 通过epoll/select机制返回有事件返回的(fd: events)的键值对
        except Exception, e:
            if e.args == (4, "Interrupted system call"):
                logging.warning("Interrupted system call", exc_info=1)
                continue
            else:
                raise
        # Pop one fd at a time from the set of pending fds and run
        # its handler. Since that handler may perform actions on
        # other file descriptors, there may be reentrant calls to
        # this IOLoop that update self._events
        self._events.update(event_pairs) # 更新所有准备好的事件列表
        while self._events:
            fd, events = self._events.popitem() # 循环逐个弹出可以待执行的socket和事件
            try:
                self._handlers[fd](fd, events) # 之前通过add_handler注册的fd和回调函数， 到这里就可以执行相对应的回调函数了
            except KeyboardInterrupt:
                raise
            except OSError, e:
                if e[0] == errno.EPIPE:
                    # Happens when the client closes the connection
                    pass
                else:
                    logging.error("Exception in I/O handler for fd %d",
                                  fd, exc_info=True)
            except:
                logging.error("Exception in I/O handler for fd %d",
                              fd, exc_info=True)
```

这就是异步的核心组件IOLoop 的核心工作，我们来看看它的工作流程：
> 1. 开始一个事件循环 Event Loop ，用于监测被注册到这里的fd（非阻塞socket）, 如果有执行事件发生，就执行相应回调函数
> 2. event_pairs = self._impl.poll(poll_timeout) 通过epoll/select机制返回有事件返回的(fd: events)的键值对
> 3. self._events.update(event_pairs) # 更新所有准备好的事件列表
> 4. while self._events: 循环这个事件列表，循环逐个弹出可以待执行的socket和事件
> 5. self._handlers[fd](fd, events) 之前通过add_handler注册的fd和回调函数， 到这里就可以执行相对应的回调函数了

通过上面介绍的add_handler注册socket->callback，这个start()功能就是tornado开启的一个单线程事件IO循环，用于监测所有非阻塞socket的事件，只要被注册的socket事件发生了，就执行注册时的回调函数。
具体到实际就是可以分为这两种情况：

监听连接: 
> 一开始创建的一个服务器端socket监听端口，等待客户端连接，这时通过setblocking(0)设置这个socket 非阻塞，然后add_handler(socket, handler_connection, READ) 注册这个socket的可读事件，只有要新连接过来，就会触发读事件，handler_connection这个回调函数就执行。

请求其他数据时: 
> 比如http_client.fetch()的connected，recvfrom的socket都会设置成nonblocking非阻塞，同时add_hanndler注册，等待事件发生，并调用回调函数。

例子：一个建议的服务器监听：
```
def connection_ready(sock, fd, events):
    while True:
        try:
            connection, address = sock.accept()
        except socket.error as e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        connection.setblocking(0)
        handle_connection(connection, address)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0) # 把监听的socket设置成非阻塞
    sock.bind(("", port))
    sock.listen(128)

    io_loop = tornado.ioloop.IOLoop.current()
    callback = functools.partial(connection_ready, sock)
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ) # 注册这个服务器端监听socket可读事件，同时注册这个回调函数
    io_loop.start()
```

![Tornado](https://upload-images.jianshu.io/upload_images/1446087-70a2fac40573eee3.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/802/format/webp)

### 效率对比实例代码
```
"""异步抓取网页"""
class AsyncHandler(RequestHandler):
    @asynchronous
    def get(self):
        http_client = AsyncHTTPClient()
        http_client.fetch("http://www.163.com",
                          callback=self.on_fetch)

    def on_fetch(self, response):
        print response
        self.write('done')
        self.finish()
```

```
"""同步抓取网页"""
class SyncHandler(RequestHandler):
    def get(self):
        http_client = HTTPClient()
        response = http_client.fetch("http://www.163.com")
        print response
        self.write('done')
```

### 进行压测测试
```
# 异步代码压测结果
Document Path:          /async_fetch/
Document Length:        4 bytes

Concurrency Level:      5
Time taken for tests:   1.945 seconds
Complete requests:      50
Requests per second:    25.71 [#/sec] (mean)
Time per request:       194.488 [ms] (mean)
Time per request:       38.898 [ms] (mean, across all concurrent requests)
```

```
# 同步代码压测结果
Document Path:          /sync_fetch/
Concurrency Level:      5
Time taken for tests:   5.423 seconds
Complete requests:      50
Requests per second:    9.22 [#/sec] (mean)
Time per request:       542.251 [ms] (mean)
Time per request:       108.450 [ms] (mean, across all concurrent requests)
```
可以看出异步比同步的性能高很多

### 总结
Tornado的异步条件：要使用到异步，就必须把IO操作变成非阻塞的IO。
Tornado的异步原理：单线程的tornado打开一个IO事件循环， 当碰到IO请求（新链接进来 或者 调用api获取数据），由于这些IO请求都是非阻塞的IO，都会把这些非阻塞的IO socket 扔到一个socket管理器，所以，这里单线程的CPU只要发起一个网络IO请求，就不用挂起线程等待IO结果，这个单线程的事件继续循环，接受其他请求或者IO操作，如此循环。

### 参考
> http://www.cnblogs.com/yiwenshengmei/archive/2011/06/08/understanding_tornado.html
> https://github.com/tornadoweb/tornado/blob/master/tornado/ioloop.py#L928
> http://blog.csdn.net/wyx819/article/details/45420017
> https://www.rapospectre.com/blog/34
> http://golubenco.org/understanding-the-code-inside-tornado-the-asynchronous-web-server-powering-friendfeed.html
> https://www.futures.moe/writings/introduction-for-tornado-async-programming.htm

