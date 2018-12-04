---
title: Kafka-创建或更新partitions数量
date: 2018-11-26 18:37:56
tags: Kafka
cover_img: http://qiniucdn.timilong.com/1543229086228.jpg
feature_img:
description: 通过进入kafka server, 和通过docker-compose在创建之初指定partitions两种方式来更改kafka的分区数.
keywords: Kafka, Partitions
categories: Kafka
---

![tu](http://qiniucdn.timilong.com/1543229086228.jpg)

> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

## 更新方法--创建成功后，进入kafka-server进行kafka脚本命令进行更新

### 查看某个topic的description内容
```
kafka-topics.sh --describe --zookeeper 192.168.160.xxx:2181 --topic  mle-computing

kafka-topics.sh --describe --zookeeper 192.168.160.xxx:2181 --topic  mle-rpc-webhooks
```

### 创建一个新的topic，并指定partitions(分区), replication-factor(副本集)
```
kafka-topics.sh --create --zookeeper 192.168.160.xxx:2181 --replication-factor 1 --partitions 3 --topic my-test-topic
```

### 列出所有的topic
```
kafka-topics.sh --list --zookeeper 192.168.160.xxx:2181
```

### 更改某个topic的partitions数量
```
kafka-topics.sh --zookeeper 192.168.160.xxx:2181 --alter --partitions 5 --topic mle-computing
```

## 更新方法--创建kafka server时指定partitions数量

```
version: '2.0'
services:
  zookeeper:
    image: wurstmeister/zookeeper
    restart: always
    ports:
      - "2181:2181"

  kafka:
    image: wurstmeister/kafka
    restart: always
    depends_on:
      - zookeeper
    links:
      - zookeeper:zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: 192.168.160.xxx
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_CREATE_TOPICS: "mle-computing:5:1,mle-rpc-webhooks:5:1"  # 5表示分区数量，1表示副本集数量, 这种情况下指定5不会生效，生效的结果是1:1
      KAFKA_NUM_PARTITIONS: 5  # 表示分区数量
      LOG4J_LOGGER_KAFKA_AUTHORIZER_LOGGER: DEBUG, authorizerAppender
    volumes:
      - /var/run/docker.sock:/var/run/docker.socks
```

