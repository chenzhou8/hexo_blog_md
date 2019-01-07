---
title: docker-通过shell命令使容器主进程不退出
cover_img: http://qiniucdn.timilong.com/1544683362440.jpg
date: 2019-01-07 21:11:14
tags: docker
feature_img:
description: 有时候调试docker时，可能需要让docker的主进程不退出，方便进入docker container进行debug.
keywords: docker
categories: docker
---

![cover_img](http://qiniucdn.timilong.com/1544683362440.jpg)

## docker命令
```
version: "2.0"

services:
  mocha-mle-training-service:
    image: xxxxxx
    command: /bin/sh -c "while true;do echo hello docker;sleep 1;done"  # /bin/sh ./run-server.sh
    privileged: false
    restart: always
    ports:
      - "10007:10007"
    volumes:
      - "/data:/data"
    environment:
      SENTRY_DSN:
      TF_SERVING_SERVER:
```
