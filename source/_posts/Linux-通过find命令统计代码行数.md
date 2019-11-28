---
title: Linux-通过find命令统计代码行数
cover_img: 'http://qiniucdn.timilong.com/ChMkJ1bKy12ITWlmAG4KdpMDEKsAALIpwJtu1AAbgqO112.jpg'
date: 2019-11-28 18:56:16
tags: Linux
feature_img:
description: 通过Linux系统命令，统计代码行数
keywords: Linux
categories: Linux
---

![cover_img](http://qiniucdn.timilong.com/ChMkJ1bKy12ITWlmAG4KdpMDEKsAALIpwJtu1AAbgqO112.jpg)

## 命令
```
wc -l `find . -name '*.go'`
```

## 输出
```
[@k:nsqd (master)]$ wc -l `find . -name '*.go'`
      12 ./backend_queue.go
      22 ./buffer_pool.go
     589 ./channel.go
     223 ./channel_test.go
     607 ./client_v2.go
       5 ./context.go
       9 ./dqname.go
      10 ./dqname_windows.go
      33 ./dummy_backend_queue.go
     105 ./guid.go
      42 ./guid_test.go
     736 ./http.go
     943 ./http_test.go
      99 ./in_flight_pqueue.go
      81 ./in_flight_pqueue_test.go
      20 ./logger.go
     198 ./lookup.go
     151 ./lookup_peer.go
     100 ./message.go
     752 ./nsqd.go
     449 ./nsqd_test.go
     151 ./options.go
    1018 ./protocol_v2.go
    1919 ./protocol_v2_test.go
     240 ./stats.go
     159 ./stats_test.go
     162 ./statsd.go
      48 ./tcp.go
     491 ./topic.go
     241 ./topic_test.go
    9615 total
```


