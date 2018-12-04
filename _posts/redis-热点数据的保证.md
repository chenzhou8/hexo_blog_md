---
title: redis-热点数据的保证
date: 2018-09-23 20:46:41
tags: Redis
feature_img:
description: MySQL里有2000w数据，redis中只存20w的数据，如何保证redis中的数据都是热点数据？
keywords: Redis
categories: Redis
cover_img: http://qiniucdn.timilong.com/1543735294748.jpg
---

![tu](http://qiniucdn.timilong.com/1543735294748.jpg)

> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

### MySQL里有2000w数据，redis中只存20w的数据，如何保证redis中的数据都是热点数据？

redis 内存数据集大小上升到一定大小的时候，就会施行数据淘汰策略。

### redis 提供 6种数据淘汰策略

> voltile-lru：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰
> volatile-ttl：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
> volatile-random：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰
> allkeys-lru：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰
> allkeys-random：从数据集（server.db[i].dict）中任意选择数据淘汰
> no-enviction（驱逐）：禁止驱逐数据

由maxmemory-policy 参数设置淘汰策略：
> CONFIG SET maxmemory-policy volatile-lru      #淘汰有过时期的最近最好使用数据

