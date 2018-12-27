---
title: 运维-支持NVIDIA-GPU调用的docker-compose配置方式
cover_img: http://qiniucdn.timilong.com/1544683570720.jpg
date: 2018-12-27 12:43:48
tags: 运维
feature_img:
description: docker-compose.yml支持runtime位nvidia的调用。
keywords: 运维
categories: 运维
---

![cover_img](http://qiniucdn.timilong.com/1544683570720.jpg)

## docker-compose.yml
```
version: "2.3"
services:
  xxxxxx-service:
    image: daocloud.io/xxxxxxxxxxx/xxxxxxxxx:latest
    container_name: xxxxxxx-service
    runtime: nvidia
    devices:
      - /dev/nvidia0
    restart: always
    command: python3 run.py
    volumes:
      - /data:/data
    environment:
      FACE_VERIFY_RADIUS: 1.2
      TF_SERVING_SERVER:
      DBSCAN_EUCLIDEAN_EPS: 1.1
      CACHE_DIRS_ROOT: /data
      CUDA_VISIBLE_DEVICES: 0
      TF_CPP_MIN_LOG_LEVEL: 3
```
