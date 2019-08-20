---
title: Tornado-多进程-异步web框架
cover_img: 'http://qiniucdn.timilong.com/ChMkJ1whnwWIOBg1AAICFoTnWfMAAt-BwKiLK4AAgIu691.jpg'
date: 2019-08-20 10:40:47
tags: Tornado
feature_img:
description: Tornado多种Server模式的启动Demo.
keywords: Tornado
categories: Tornado
---

![cover_img](http://qiniucdn.timilong.com/ChMkJ1whnwWIOBg1AAICFoTnWfMAAt-BwKiLK4AAgIu691.jpg)

## 单进程同步Server
```python
# coding: utf-8
 
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
 
from tornado.options import options , define
define("port",default=8001,help="跑在8001",type=int)
 
import time
class SleepHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(5)
        self.write("this is SleepHandler...")
 
class DirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("this is DirectHandler...")
 
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [
            (r"/d",DirectHandler),
            (r"/s",SleepHandler),
        ],
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
```

## 多进程同步Server
> 注意一定要关闭debug功能！！！否则：Cannot run in multiple processes: IOLoop instance

```python
#coding:utf-8
 
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
 
from tornado.options import options , define
define("port",default=8001,help="跑在8001",type=int)
 
import time
class SleepHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(10)
        self.write("this is SleepHandler...")
 
class DirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("this is DirectHandler...")
 
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [
            (r"/d",DirectHandler),
            (r"/s",SleepHandler),
        ],
        debug = False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(0)
    # [I 150610 10:42:05 process:115] Starting 4 processes
    tornado.ioloop.IOLoop.instance().start()
```

## 高级多进程同步Server
> 注意一定要关闭debug功能！！！否则：Cannot run in multiple processes: IOLoop instance
```python
#coding:utf-8
 
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
 
from tornado.options import options , define
define("port",default=8001,help="跑在8001",type=int)
 
import time
class SleepHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(10)
        self.write("this is SleepHandler...")
 
class DirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("this is DirectHandler...")
 
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [
            (r"/d",DirectHandler),
            (r"/s",SleepHandler),
        ],
        debug = False
    )
    sockets = tornado.netutil.bind_sockets(port)
    tornado.process.fork_processes(0)
    server = HTTPServer(app)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()
```

## bind()
```python
def bind(self, port, address=None, family=socket.AF_UNSPEC, backlog=128):
    """
    绑定server到指定地址的端口上。
    调用start来启动server。如果想把这个server跑在单线程上，可以调用listen方法，listen是bind和start方法的单进程模式的“快捷键”。
    地址可能是ip地址或者hostname。如果是hostname，server将监听其所有关联ip。
    地址若是空字符串将监听不到任何可用接口。family参数可设置为socket.AF_INET或socket.AF_INET6来约定ipv4或者是ipv6地址，缺省情况下会启用所有可用的。
    backlog参数与socket.listen同义。
    bind方法会多次在start方法前调用来监听多个端口或者接口。
    """
    sockets = bind_sockets(port, address=address, family=family,
                           backlog=backlog)
    if self._started:
        self.add_sockets(sockets)
    else:
        self._pending_sockets.extend(sockets)
```

## start()
```python
def start(self, num_processes=1):
    """
    默认情况下，但进程运行server，不会fork任何额外的子进程。
    如果num_processes为None或<=0 ，会根据机器的cpu核数fork子进程。若num_processes>=1，就fork这个数目的子进程。
    因为我们使用的是进程而不是线程,所以不会在server code之间共享内存。
    特别注意，多进程与自动装载模型不兼容。在调用TCPServer.start(n)前，任何IOLoop都不能创建和引用。
    """
    assert not self._started
    self._started = True
    if num_processes != 1:
        process.fork_processes(num_processes)
    sockets = self._pending_sockets
    self._pending_sockets = []
    self.add_sockets(sockets)
```

## 异步Server版本1
```python
#coding:utf-8
 
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
 
from tornado.options import options , define
define("port",default=8001,help="跑在8001",type=int)
 
import time
class SleepHandler(tornado.web.RequestHandler):
    """
        将sleep.py的代码如上述一样改造，即在get()方法前面增加了装饰器@tornado.web.asynchronous，它的作用在于将tornado服务器本身默认的设置_auto_fininsh值修改为false。如果不用这个装饰器，客户端访问服务器的get()方法并得到返回值之后，两只之间的连接就断开了，但是用了@tornado.web.asynchronous之后，这个连接就不关闭，直到执行了self.finish()才关闭这个连接。
        tornado.ioloop.IOLoop.instance().add_timeout()也是一个实现异步的函数，time.time()+17是给前面函数提供一个参数，这样实现了相当于time.sleep(17)的功能，不过，还没有完成，当这个操作完成之后，就执行回调函数on_response()中的self.render(“sleep.html”)，并关闭连接self.finish()。 
        https://github.com/qiwsir/StarterLearningPython/blob/master/309.md
    """
    @tornado.web.asynchronous
    def get(self):
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 5, callback=self.on_response)
 
    def on_response(self):
        self.write("this is SleepHandler...")
        self.finish()
 
 
class DirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("this is DirectHandler...")
 
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [
            (r"/d",DirectHandler),
            (r"/s",SleepHandler),
        ],
        debug = False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()
```

## 异步Server版本2
```python
#coding:utf-8
 
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.gen
 
from tornado.options import options , define
define("port",default=8001,help="跑在8001",type=int)
 
import time
class SleepHandler(tornado.web.RequestHandler):
    """
        使用yield得到了一个生成器，先把流程挂起，等完全完毕，再唤醒继续执行。另，生成器都是异步的。
    """
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 5)
        self.write("this is SleepHandler...")
 
 
class DirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("this is DirectHandler...")
 
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [
            (r"/d",DirectHandler),
            (r"/s",SleepHandler),
        ],
        debug = False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()
```
