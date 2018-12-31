---
title: docker-build简单用法
date: 2018-08-08 11:34:46
categories: Docker
tags: Docker
cover_img: http://qiniucdn.timilong.com/1543387754757.jpg
description: 手动构建docker images时，需要使用到本文介绍的docker build命令.
---

![tu](http://qiniucdn.timilong.com/1543387754757.jpg)

## 说明

docker build 命令用于使用 Dockerfile 创建镜像。

## 语法

```
docker build [OPTIONS] PATH | URL | -
```

OPTIONS说明:
```
--build-arg=[] :设置镜像创建时的变量；

--cpu-shares :设置 cpu 使用权重；

--cpu-period :限制 CPU CFS周期；

--cpu-quota :限制 CPU CFS配额；

--cpuset-cpus :指定使用的CPU id；

--cpuset-mems :指定使用的内存 id；

--disable-content-trust :忽略校验，默认开启；

-f :指定要使用的Dockerfile路径；

--force-rm :设置镜像过程中删除中间容器；

--isolation :使用容器隔离技术；

--label=[] :设置镜像使用的元数据；

-m :设置内存最大值；

--memory-swap :设置Swap的最大值为内存+swap，"-1"表示不限swap；

--no-cache :创建镜像的过程不使用缓存；

--pull :尝试去更新镜像的新版本；

--quiet, -q :安静模式，成功后只输出镜像 ID；

--rm :设置镜像成功后删除中间容器；

--shm-size :设置/dev/shm的大小，默认值是64M；

--ulimit :Ulimit配置。

--tag, -t: 镜像的名字及标签，通常 name:tag 或者 name 格式；可以在一次构建中为一个镜像设置多个标签。

--network: 默认 default。在构建期间设置RUN指令的网络模式
```

## 例子

```
docker build -t "test_docker/mle_platform_api_v0.1" . --no-cache
    * -t 是指明到哪个repository下的哪个tag
    * . 表示当前目录下的dockerfile
    * --no-cache: 表示不使用缓存功能，在没有结束提交之前的镜像层，都看作缓存层，比如我们yum update后，再次执行dockefile是不会在yum update了，所以使用--no-cache后才会执行yum update。

注意 . 目录表示当前目录， 需要在当前目录下编写: Dockerfile文件。

```

使用URL github.com/creack/docker-firefox 的 Dockerfile 创建镜像。
```
docker build github.com/creack/docker-firefox
```


