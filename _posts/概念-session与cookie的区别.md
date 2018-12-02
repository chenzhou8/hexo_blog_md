---
title: 后端-session与cookie的区别
date: 2018-09-29 21:04:48
tags: 后端
feature_img:
description: 概念性了解Cookie和Session的区别
keywords: 后端
categories: 后端
cover_img: http://qiniucdn.timilong.com/154373673961.jpg

---

# 概念: 什么是Cookie和Session
## 协议角度理解
1. Http协议是无状态的协议, 每一次请求都是独立的. 服务端无法区分不同浏览器, 不同客户端的请求有什么不同.

2. 实际B/S架构中, 是需要区别不同访客和请求的. 这就需要保存"状态".

3. Cookie和Session机制就是为了解决和弥补Http协议无状态问题而生.

4. Cookie是一种在客户端(浏览器端)保存状态的方案.

5. Session是一种在服务端保存状态的方案.

## 通俗流程理解
1. 浏览器请求服务端时, 服务端先检查该请求有没有"临时身份ID/暗号"/`session_id`, 如果有, 就从服务器中调取该id对应的`session`中的各项信息, 每个session中都保存了当前客户端的特征信息, 比如该请求的`user_id`之类. 这样就能够区别该请求来自于谁. 就能维护客户端请求上下文的状态了.

2. 如果该请求没有"临时身份ID/暗号"/`session_id`, 服务端就创建一个(今晚的口令是"鸡肋"), 并在响应中, 将`session_id`回传给客户端. 目的就是告诉客户端(浏览器): 你丫现在有临时身份了, 保存好, 下次再来访问的时候记得出示临时身份证(记得对暗号).

3. 客户在请求的时候, 无论以什么方式, 把`session_id`/暗号告诉服务端即可.

4. Cookie就是客户端(浏览器)保存`session_id`/暗号的一种方式. 也可以使用其它方式保存, 比如表单: `<input type="hidden" name="token" value="鸡肋">`, 比如url中的参数重写: `Domain Name Registration and Web Hosting, 比如html5中的localStore等.

# Cookie和Session的区别
1. Session存在服务端, Cookie存在客户端.

2. Cookie存在客户端, 不可控, 不安全, 一般只存`session_id`(口令), 存储的数据最好都经过加密处理.

3. Session存在服务端, 只有服务端有访问权限. 相对安全可控, 可以存真实的`user_id`等敏感信息.

## Cookie

1. Cookie由服务端生成, 并发送给浏览器, 由浏览器将Cookie保存到本地文件系统内. Cookie文件的名字一般是user@domain.

2. Cookie文件的内容都是经过加密的, 需要经过CGI程序处理.

3. Cookie文件的内容有name, value, expire(过期时间), path, domain(域), secure(安全).
```
path: #指定与cookie相关联的页面.

domain: #指定关联的服务器或域.

name: #cookie变量的名称key.

value: #cookie变量key存储的值.

expire: #一般cookie生成时就会被指定一个expire值, 也就是生存时间. 在这个周期内cookie是有效的, 超过这个周期cookie就会被清除.
```
4. Cookie的生成过程是: 服务器在Response头信息中, 添加一个Set-Cookie字段, 该字段的值指定cookie内容. 如`Set-Cookie: session_id=xxx;expires=xxx;...`.浏览器接收到响应后. 自动在本地存储对应的cookie信息.

5. 浏览器端发送Cookie过程: 发送请求时, 如果本地本域有Cookie, 浏览器自动在Request头信息中, 添加`Cookie: key1=value1; key2=value2;...`.

6. 由于Cookie中包含了"状态识别/身份识别"等敏感信息, 虽然信息经过加密, 但如果被别人截获并提交同样的Cookie, 就可以冒充他人访问服务器.

7. 单个Cookie保存的数据不能超过4k, 很多浏览器都限制一个站点最多保存20个Cookie.

## Session
1. 当服务端要为某个客户端的请求创建一个session时, 会首先检查这个客户端的请求里是否已包含一个`session_id`. 如果有则表明已经为此客户端创建过session, 服务器就按照这个`session_id`查找出服务端保存的session(如果查找失败会创建一个新的session).

2. 如果请求中不包含`session_id`,就会创建一个新的`session_id`并返回客户端保存.

## Session与Cookie过期
1. 服务端在保存Session时也可以设置Session的过期时间, 服务端的Web服务器通过也有一个默认的过期时间. 同时根据服务端的机制不同, 各种重启, 资源回收都可能导致Session过期.

2. 服务端每次接收到请求, 如果命中session, 会重置该session的过期时间. 不出意外, 如果在过期前一直发送请求, session就不会过期.

3. **会话Cookie**: 大部分服务端在发回`session_id`时使用了会话Cooke(即没有设置该Cookie的过期时间), 导致该Cookie存在客户端**内存**中, 所以关闭浏览器即丢失了`session_id`信息, 会话即过期.

4. 当(存放着`session_id`的)Cookie和Session中两者任一过期, 即宣告会话过期. 状态不再被保存.

5. **session过期后通过cookie恢复状态**: 这点也迷糊, 如何做比较安全.
``
1. 第一次验证成功时, 生成token令牌, 保存在数据库中, 并给客户端cookie设置一个自动登陆值.设置比较长的有效期.

2. 存储登陆值的cookie可以由: 登陆名|有效时间|hash值. hash值可以由"登陆名+创建时间+token(加密后的)的前几位+salt加密生成.

3. session命中的情况下, 都通过session验证.

4. session未命中时, 获取cookie中的自动登陆值, 解密并与数据库中的tooken匹配, 如果匹配成功, 创建新的session, 创建新的token, 创建新的自动登陆cookie, 并返回客户端.
```

# 会话机制
会话机制(状态维护)不一定必须用Session和Cookie来实现. 只要能实现以下功能, 使用任何工具, 方式都可以:

1. 服务端能够生成一个不重复(唯一)的口令. 并将新生成的或变更过的口令告诉客户端.

2. 客户端可以保存/记录服务端发给自己的口令, 并在接下来的所有请求中, 都向服务端出示口令.

3. 服务端接收到客户端的请求后, 通过客户端提供的口令, 能够对客户端进行唯一识别.

