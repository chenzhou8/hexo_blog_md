---
title: docker-通过docker-compose安装mysql_redis_kafka等
cover_img: http://qiniucdn.timilong.com/1544683408710.jpg
date: 2018-12-29 10:04:05
tags: 运维
feature_img:
description: 通过docker-compose的方式安装Kafka, Zookeeper, MySQL, Redis, PostgreSQL
keywords: 运维，docker
categories: 运维
---

![cover_img](http://qiniucdn.timilong.com/1544683408710.jpg)

> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

## 安装Kafka

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
      KAFKA_ADVERTISED_HOST_NAME: 192.168.160.80
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_CREATE_TOPICS: "mle-computing:5:1,mle-rpc-webhooks:5:1"
      KAFKA_NUM_PARTITIONS: 5
      LOG4J_LOGGER_KAFKA_AUTHORIZER_LOGGER: DEBUG, authorizerAppender
    volumes:
      - /var/run/docker.sock:/var/run/docker.socks

```

## 安装MySQL

```
# Use root/example as user/password credentials
version: '2'
services:
  mysql:
    image: mysql:5.7.22
    restart: always
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: 123456
    volumes:
      - /data/mysql:/var/lib/mysql
```

## 安装redis

```
version: '2.0'

services:
  redis:
    image: 'bitnami/redis:latest'
    environment:
      - ALLOW_EMPTY_PASSWORD=yes
      - REDIS_DISABLE_COMMANDS=FLUSHDB,FLUSHALL
    ports:
      - '6379:6379'
    volumes:
      - '/data/redis:/bitnami/redis'
```

## 安装postgresql

```
version: "3"

services:
  postgres:
    image: postgres:latest
    container_name: postgresql_name
    volumes:
      - /data/postgresql:/var/lib/postgresql/data
    expose:
      - 5432
    ports:
      - 5432:5432
    environment:
      - POSTGRES_DB=test_dbname
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=123456
```

