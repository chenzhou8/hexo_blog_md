---
title: mysql-MySQL 各种超时参数的含义
cover_img: http://qiniucdn.timilong.com/1544683290775.jpg
date: 2019-01-03 12:23:57
tags: MySQL
feature_img:
description: MySQL 各种超时参数的含义.
keywords: MySQL
categories: MySQL
---

![cover_img](http://qiniucdn.timilong.com/1544683290775.jpg)

## 说明

`connect_timeout`：默认为10S, 该参数没有session级别，是一个global级别变量.
`wait_timeout`：默认是8小时，即28800秒, MySQL命令行客户端, 分为session级别和global级别.
`interactive_timeout`：默认是8小时，即28800秒, MySQL命令行客户端超时时间, 分为session级别和global级别.
`net_read_timeout`：默认是30S, mysql服务端从客户端读取（接收）数据时，服务端等待客户端响应的超时时间，当服务端正在从客户端读取数据时，net_read_timeout控制何时超时, 对于这个参数，session和global级别并没有什么特别，session级别只对当前连接生效，global级别只对新的连接生效。
`net_write_timeout`：默认是60S, mysql服务端向客户端写(发送)数据时，服务端等待客户端响应的超时时间，当服务端正在写数据到客户端时，net_write_timeout控制何时超时 对于这个参数，session和global级别并没有什么特别，session级别只对当前连接生效，global级别只对新的连接生效。

### connect_timeout：在获取连接阶段（authenticate）起作用

获取MySQL连接是多次握手的结果，除了用户名和密码的匹配校验外，还有IP->HOST->DNS->IP验证，任何一步都可能因为网络问题导致线程阻塞。为了防止线程浪费在不必要的校验等待上，超过connect_timeout的连接请求将会被拒绝。

官方描述：
```
connect_timeout(The number of seconds that the mysqld server waits for a connect packet before responding with Bad handshake. The default value is 10 seconds)
```

### interactive_timeout和wait_timeout：在连接空闲阶段（sleep）起作用

即使没有网络问题，也不能允许客户端一直占用连接。对于保持sleep状态超过了wait_timeout（或interactive_timeout，取决于client_interactive标志）的客户端，MySQL会主动断开连接。

官方描述：
```
wait_timeout：The number of seconds the server waits for activity on a noninteractive connection before closing it. On thread startup, the session wait_timeout value is initialized from the global wait_timeout value or from the global interactive_timeoutvalue, depending on the type of client (as defined by the CLIENT_INTERACTIVE connect option to mysql_real_connect()).

interactive_timeout：The number of seconds the server waits for activity on an interactive connection before closing it. An interactive client is defined as a client that uses the CLIENT_INTERACTIVE option to mysql_real_connect()
```

### net_read_timeout和net_write_timeout：则是在连接繁忙阶段（query）起作用。

即使连接没有处于sleep状态，即客户端忙于计算或者存储数据，MySQL也选择了有条件的等待。在数据包的分发过程中，客户端可能来不及响应（发送、接收、或者处理数据包太慢）。
为了保证连接不被浪费在无尽的等待中，MySQL也会选择有条件（net_read_timeout和net_write_timeout）地主动断开连接。
这个参数只对TCP/IP链接有效，只针对在Activity状态下的线程有效

官方描述：
```
net_read_timeout：The number of seconds to wait for more data from a connection before aborting the read. When the server is reading from the client,net_read_timeout is the timeout value controlling when to abort. When the server is writing to the client, net_write_timeout is the timeout value controlling when to abort
net_write_timeout：The number of seconds to wait for a block to be written to a connection before aborting the write. See also net_read_timeout.
```

### handshake流程

在TCP三次握手的基础之上，简历MySQL通讯协议的连接，这个连接建立过程受connect_timeout参数控制
```
--------------------TCP established--------------------
MySQL Server(10.10.20.96)------->Client(10.10.20.51)
Client(10.10.20.51)------->MySQL Server(10.10.20.96)
MySQL Server(10.10.20.96)------->Client(10.10.20.51)
--------------------established--------------------
```

在MySQL通讯协议建立连接之后，此时客户端连接的超时受wait_timeout和interactive_timeout参数控制

建立连接后无交互：MySQL server ---wait_timeout--- Client
建立连接交互后：MySQL server ---interactive_timeout--- Client

在如果客户端有数据包传输，那么这个数据包的传输超时由net_read_timeout和net_write_timeout参数控制
```
-------------------client与server端有数据传输时-------------------
client ----->MySQL Server(net_read_timeout)
client <-----MySQL Server(net_write_timeout)
```

## 设置超时
```
mysql> set global interactive_timeout=81600;
Query OK, 0 rows affected (0.07 sec)

mysql> set global wait_timeout=81600;
Query OK, 0 rows affected (0.00 sec)

mysql> show session variables like '%timeout%';show global variables like '%timeout%';
+-----------------------------+----------+
| Variable_name               | Value    |
+-----------------------------+----------+
| connect_timeout             | 10       |
| delayed_insert_timeout      | 300      |
| have_statement_timeout      | YES      |
| innodb_flush_log_at_timeout | 1        |
| innodb_lock_wait_timeout    | 50       |
| innodb_rollback_on_timeout  | OFF      |
| interactive_timeout         | 28800    |
| lock_wait_timeout           | 31536000 |
| net_read_timeout            | 30       |
| net_write_timeout           | 60       |
| rpl_stop_slave_timeout      | 31536000 |
| slave_net_timeout           | 60       |
| wait_timeout                | 81600    |
+-----------------------------+----------+
13 rows in set (0.01 sec)

+-----------------------------+----------+
| Variable_name               | Value    |
+-----------------------------+----------+
| connect_timeout             | 10       |
| delayed_insert_timeout      | 300      |
| have_statement_timeout      | YES      |
| innodb_flush_log_at_timeout | 1        |
| innodb_lock_wait_timeout    | 50       |
| innodb_rollback_on_timeout  | OFF      |
| interactive_timeout         | 81600    |
| lock_wait_timeout           | 31536000 |
| net_read_timeout            | 30       |
| net_write_timeout           | 60       |
| rpl_stop_slave_timeout      | 31536000 |
| slave_net_timeout           | 60       |
| wait_timeout                | 81600    |
+-----------------------------+----------+
13 rows in set (0.02 sec)

mysql>
```
