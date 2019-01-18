---
title: docker-构建前后分离项目
cover_img: http://qiniucdn.timilong.com/1544683505643.jpg
date: 2019-01-18 10:29:28
tags: Docker
feature_img:
description: 记录一次帮助前端搭建Docker的经历.
keywords: Docker
categories: Docker
---

![cover_img](http://qiniucdn.timilong.com/1544683505643.jpg)

> 转载自: 微信公众号，[架构师之路]()
> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

## 前端项目

### docker-compose
```
mocha-xxxx:
  image: xxxxxxx:latest
  command: nginx -g "daemon off;"
  privileged: false
  restart: always
  ports:
  - 8080:80

```

### Dockerfile
```
FROM daocloud.io/library/ubuntu:latest

MAINTAINER wangxingkang<wang_xingkang@qq.com>

# 安装nginx
# RUN apt-get install -y epel-release
# 安装node


RUN apt-get update && apt-get install -y nginx && apt-get install -y nodejs && node -v && apt-get install -y npm

# 创建一个临时工作目录
RUN mkdir /app

# 切换到当前工作目录
WORKDIR /app

# copy当前的所有文件到临时工作目录
COPY . /app/


# 安装依赖 # 执行编译
RUN npm install -g yarn && npm run bootstrap && npm run build

# 处理静态资源
ADD nginx.conf /etc/nginx/nginx.conf

RUN mkdir /var/www/html/dist
RUN cp -r dist/* /var/www/html/dist

# 删除临时目录
RUN rm -rf /app && apt-get --purge remove -y nodejs &&  apt-get --purge remove -y npm && apt autoremove -y

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]

```
