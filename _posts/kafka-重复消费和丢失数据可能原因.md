---
title: kafka-重复消费和丢失数据可能原因
date: 2018-09-14 17:43:39
tags: 消息队列
cover_img:
feature_img:
description: Kafka重复消费和丢失数据研究
keywords: kafka
categories: 消息队列
---

> 转载自: CSDN，[Kafka重复消费和丢失数据研究](https://blog.csdn.net/zollty/article/details/53958641)

### Kafka重复消费原因

底层根本原因：<code>已经消费了数据，但是offset没提交。</code>

#### 原因1：强行kill线程，导致消费后的数据，offset没有提交。

#### 原因2：设置offset为自动提交，关闭kafka时，如果在close之前，调用 consumer.unsubscribe() 则有可能部分offset没提交，下次重启会重复消费。

例如：

```
try:
    consumer.unsubscribe();
except Exception as e:
    pass

try:
    consumer.close();
except Exception as e:
    pass
```

上面代码会导致部分offset没提交，下次启动时会重复消费。

#### 原因3（重复消费最常见的原因）：消费后的数据，当offset还没有提交时，partition就断开连接。
比如:
> 通常会遇到消费的数据，处理很耗时，导致超过了Kafka的session timeout时间（0.10.x版本默认是30秒），那么就会re-blance重平衡，此时有一定几率offset没提交，会导致重平衡后重复消费。

### Kafka Consumer丢失数据原因

猜测：设置offset为自动定时提交，当offset被自动定时提交时，数据还在内存中未处理，此时刚好把线程kill掉，那么offset已经提交，但是数据未处理，导致这部分内存中的数据丢失。

### 解决方案：记录offset和恢复offset的方案

理论上记录offset，下一个group consumer可以接着记录的offset位置继续消费。

#### offset记录方案：

每次消费时更新每个topic+partition位置的offset在内存中， <code>Map<key, value>，key=topic+'-'+partition，value=offset</code>

当调用关闭consumer线程时，把上面Map的offset数据记录到文件中<code>（分布式集群可能要记录到redis中）</code>。

下一次启动consumer，需要读取上一次的offset信息，方法是 以当前的topic+partition为key，从上次的Map中去寻找offset。

然后使用consumer.seek()方法指定到上次的offset位置。

#### 说明：

1、该方案针对单台服务器比较简单，直接把offset记录到本地文件中即可，但是对于多台服务器集群，offset也要记录到同一个地方，并且需要做去重处理。
如果线上程序是由多台服务器组成的集群，是否可以用一台服务器来支撑？应该可以，只是消费慢一点，没多大影响。

2、如何保证接着offset消费的数据正确性

为了确保consumer消费的数据一定是接着上一次consumer消费的数据，

consumer消费时，记录第一次取出的数据，将其offset和上次consumer最后消费的offset进行对比，如果相同则继续消费。

如果不同，则停止消费，检查原因。
