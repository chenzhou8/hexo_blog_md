---
title: docker-Docker容器镜像瘦身的三个小窍门
date: 2018-09-03 19:38:09
tags: Docker
cover_img: http://qiniucdn.timilong.com/1543387757615.jpg
feature_img:
description: 在构建Docker容器时，我们应尽可能减小镜像的大小。使用共享层的镜像尺寸越小，其传输和部署速度越快。 不过在每个RUN语句都会创建一个新层的情况下，如果我们需要获取镜像完成前的中间产物，又如何控制其大小呢？
keywords: Docker
---

![tu](http://qiniucdn.timilong.com/1543387757615.jpg)

> 转载自: 微信公众号[Docker 梁晓勇 译](https://mp.weixin.qq.com/s/Iwn4bMQwD-HEK-WI1494GQ)

## 介绍
在构建Docker容器时，我们应尽可能减小镜像的大小。使用共享层的镜像尺寸越小，其传输和部署速度越快。

不过在每个RUN语句都会创建一个新层的情况下，如果我们需要获取镜像完成前的中间产物，又如何控制其大小呢？

你可能已经注意到市面上多数的Dockerfile都会使用类似这样的招数：
```
FROM ubuntu
RUN apt-get update && apt-get install vim
```

为什么要使用`&&`，而不像这样运行两个`RUN`语句？
```
FROM ubuntu
RUN apt-get update
RUN apt-get install vim
```

从Docker 1.10起，COPY、ADD和RUN语句会在镜像中添加新层。上述示例将创建两个层，而不是一个。
![分层](http://omdt9pa3d.bkt.clouddn.com/docker-%E5%88%86%E5%B1%82)


## 层跟Git提交类似。

Docker层存储了镜像上一版本和当前版本之间的差异。与Git提交类似，层有利于与其他仓库或镜像进行共享。

实际上，当我们从Registry请求镜像时，我们只会下载那些不存在的层。这种方式让镜像共享更高效。

但是，层是有代价的。

层会占用空间，层越多，最终的镜像就越大。Git仓库在这方面是相似的。因为Git需要保存提交之间的所有变更，仓库的大小会随着层数的增加而增加。
在过去，做法就是像第一个例子那样将几个RUN语句合并在一行中。

## 使用Docker多阶段构建将层合并为一

当Git仓库变得越来越大时，我们可以放弃所有过往信息，将历史提交合并成一个。

使用Docker的多阶段构建，我们也能实现类似的功能。

接下来的例子中，我们将构建一个Node.js容器。

首先是index.js文件：
```
const express = require('express')
const app = express()

app.get('/', (req, res) => res.send('Hello World!'))

app.listen(3000, () => {
  console.log(`Example app listening on port 3000!`)
})
```

接着是package.json文件：
```
{
  "name": "hello-world",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "express": "^4.16.2"
  },
  "scripts": {
    "start": "node index.js"
  }
}
```

通过以下Dockerfile来打包该应用：
```
FROM node:8

EXPOSE 3000

WORKDIR /app
COPY package.json index.js ./
RUN npm install

CMD ["npm", "start"]
```

构建镜像：
```
$ docker build -t node-vanilla .
```

然后我们可以这么验证它：
```
$ docker run -p 3000:3000 -ti --rm --init node-vanilla
```

访问 http://localhost:3000 应该就能看到“Hello World!”欢迎语。

这个Dockerfile文件中有一个COPY和一个RUN语句。在我们的预期中，在基础镜像上应该至少有两层：
```
$ docker history node-vanilla
IMAGE          CREATED BY                                      SIZE
075d229d3f48   /bin/sh -c #(nop)  CMD ["npm" "start"]          0B
bc8c3cc813ae   /bin/sh -c npm install                          2.91MB
bac31afb6f42   /bin/sh -c #(nop) COPY multi:3071ddd474429e1…   364B
500a9fbef90e   /bin/sh -c #(nop) WORKDIR /app                  0B
78b28027dfbf   /bin/sh -c #(nop)  EXPOSE 3000                  0B
b87c2ad8344d   /bin/sh -c #(nop)  CMD ["node"]                 0B
<missing>      /bin/sh -c set -ex   && for key in     6A010…   4.17MB
<missing>      /bin/sh -c #(nop)  ENV YARN_VERSION=1.3.2       0B
<missing>      /bin/sh -c ARCH= && dpkgArch="$(dpkg --print…   56.9MB
<missing>      /bin/sh -c #(nop)  ENV NODE_VERSION=8.9.4       0B
<missing>      /bin/sh -c set -ex   && for key in     94AE3…   129kB
<missing>      /bin/sh -c groupadd --gid 1000 node   && use…   335kB
<missing>      /bin/sh -c set -ex;  apt-get update;  apt-ge…   324MB
<missing>      /bin/sh -c apt-get update && apt-get install…   123MB
<missing>      /bin/sh -c set -ex;  if ! command -v gpg > /…   0B
<missing>      /bin/sh -c apt-get update && apt-get install…   44.6MB
<missing>      /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>      /bin/sh -c #(nop) ADD file:1dd78a123212328bd…   123MB
```

实际上，最终的镜像上添加了五个新层：Dockerfile里的每条语句一层。

我们来试试Docker的多阶段构建。

我们使用的Dockerfile与之前相同，不过分成了两部分：
```
FROM node:8 as build

WORKDIR /app
COPY package.json index.js ./
RUN npm install

FROM node:8

COPY --from=build /app /
EXPOSE 3000
CMD ["index.js"]
```

Dockerfile的第一部分创建了三个层。接着这些层被合并复制到第二个阶段中。然后又在这个镜像之上添加了两层，最终变成三个层。
![合并层](http://omdt9pa3d.bkt.clouddn.com/docke-%E5%90%88%E5%B9%B6%E5%B1%82)

现在来验证一下。首先，构建该容器：
```
$ docker build -t node-multi-stage .
```

查看其构建历史：
```
$ docker history node-multi-stage
IMAGE          CREATED BY                                      SIZE
331b81a245b1   /bin/sh -c #(nop)  CMD ["index.js"]             0B
bdfc932314af   /bin/sh -c #(nop)  EXPOSE 3000                  0B
f8992f6c62a6   /bin/sh -c #(nop) COPY dir:e2b57dff89be62f77…   1.62MB
b87c2ad8344d   /bin/sh -c #(nop)  CMD ["node"]                 0B
<missing>      /bin/sh -c set -ex   && for key in     6A010…   4.17MB
<missing>      /bin/sh -c #(nop)  ENV YARN_VERSION=1.3.2       0B
<missing>      /bin/sh -c ARCH= && dpkgArch="$(dpkg --print…   56.9MB
<missing>      /bin/sh -c #(nop)  ENV NODE_VERSION=8.9.4       0B
<missing>      /bin/sh -c set -ex   && for key in     94AE3…   129kB
<missing>      /bin/sh -c groupadd --gid 1000 node   && use…   335kB
<missing>      /bin/sh -c set -ex;  apt-get update;  apt-ge…   324MB
<missing>      /bin/sh -c apt-get update && apt-get install…   123MB
<missing>      /bin/sh -c set -ex;  if ! command -v gpg > /…   0B
<missing>      /bin/sh -c apt-get update && apt-get install…   44.6MB
<missing>      /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>      /bin/sh -c #(nop) ADD file:1dd78a123212328bd…   123MB
```

符合预期！文件大小有变化么？
```
$ docker images | grep node-
node-multi-stage   331b81a245b1   678MB
node-vanilla       075d229d3f48   679MB
```

是的，新的镜像要小一点点。

看起来还不错！尽管应用本身已经做了精简，我们还是减少了其整体大小。

不过，镜像依然很大！

要让它变得更小一点，我们还能做点什么？

### 使用Distroless移除容器中的所有累赘

目前的镜像不仅含有Node.js，还含有yarn、npm、bash以及大量其他二进制文件。同时，它是基于Ubuntu的。因此拥有一个完整的操作系统以及所有的二进制文件和实用程序。

这些在运行容器时都不是必需的。我们唯一的依赖项是Node.js。

Docker容器应封装在单一进程中，且只包含运行所需的最精简内容。我们不需要一个操作系统。

实际上，除了Node.js，其他都可以移除。

那么要怎么做呢？

幸运的是，Google也有同样的想法，他们带来了GoogleCloudPlatform/distroless[1]。

有如其仓库说明所述：
“Distroless”镜像只包含应用程序及其运行时依赖。不包含包管理器、Shell以及其他标准Linux发行版中能找到的其他程序。
这正是我们所需要的！

我们可以调整Dockerfile文件来使用这个新的基础镜像：
```
FROM node:8 as build

WORKDIR /app
COPY package.json index.js ./
RUN npm install

FROM gcr.io/distroless/nodejs

COPY --from=build /app /
EXPOSE 3000
CMD ["index.js"]
```

然后像平常那样编译镜像：
```
$ docker build -t node-distroless .
```

应用程序应能正常运行。要验证这一点，可以像这样运行容器：
```
$ docker run -p 3000:3000 -ti --rm --init node-distroless
```

访问 http://localhost:3000 页面即可。

这个未包含额外程序的镜像会多小呢？

$ docker images | grep node-distroless
node-distroless   7b4db3b7f1e5   76.7MB

仅仅76.76MB！

比前一个镜像少了600MB！

真是个好消息！不过在使用Distroless时有些事项需要注意。

容器运行时，如果想对其进行检查，可以这么做：
```
$ docker exec -ti <替换成_docker_id> bash
```

上述命令将附加到容器中并运行bash，这与发起一个SSH会话相近。

不过由于Distroless是原始操作系统的精简版本，不包含额外的程序。容器里并没有Shell！

如果没有Shell，要如何附加到运行的容器中呢？

好消息和坏消息是，做不到。

坏消息是我们只能运行容器中的二进制程序。这里能运行的只有Node.js：
```
$ docker exec -ti <替换成_docker_id> node
```

好消息是因为没有Shell，如果黑客入侵了我们的应用程序并获取了容器的访问权限，他也无法造成太大的损害。也就是说，程序越少则尺寸越小也越安全。不过，代价是调试更麻烦。
需要注意的是，我们不应该在生产环境中附加到容器中进行调试，而应依靠正确的日志和监控。
如果我们既希望能调试，又关心尺寸大小，又该怎么办？


## 使用Alpine作为更小的基础镜像

我们可以使用Alpine取代Distroless来作为基础镜像。

Alpine Linux[2]是：
> 一个基于musl libc[3]和busybox[4]、面向安全的轻量级Linux发行版。

换言之，它是一个尺寸更小、更安全的Linux发行版。

是否言过其实，我们来检查一下这个镜像是否更小。

修改之前的Dockerfile并使用node:8-alpine：
```
FROM node:8 as build

WORKDIR /app
COPY package.json index.js ./
RUN npm install

FROM node:8-alpine

COPY --from=build /app /
EXPOSE 3000
CMD ["npm", "start"]
```

构建该镜像：
```
$ docker build -t node-alpine .
```

现在看一下它的大小：
```
$ docker images | grep node-alpine
node-alpine   aa1f85f8e724   69.7MB
```

69.7MB！

甚至比Distroless镜像还要小！

我们来看看能不能附加运行中的容器。

首先，启动容器：
```
$ docker run -p 3000:3000 -ti --rm --init node-alpine
Example app listening on port 3000!
```

现在附加到容器中：
```
$ docker exec -ti 9d8e97e307d7 bash
OCI runtime exec failed: exec failed: container_linux.go:296: starting container process caused "exec: \"bash\": executable file not found in $PATH": unknown
```

运气不佳。但或许容器有sh这个Shell？
```
$ docker exec -ti 9d8e97e307d7 sh
/ #
```

很好！我们既可以附加到运行的容器中，得到的镜像尺寸也很小。

听起来很棒，不过有一个小问题。

Alpine基础镜像是基于muslc的，这是一个C的替代标准库。

但是，多数Linux发行版，比如Ubuntu、Debian及CentOS都是基于glibc的。这两个库照理应该实现了相同的接口。

不过，它们的目标不同：

- glibc最常用，速度更快
- muslc占用空间更少，以安全为核心

在编译应用程序时，多数情况下是使用某个libc来编译的。如果想在其他libc中使用，只能重新编译。

也就是说，使用Alpine镜像来构建容器可能会造成不可预期的问题，因为使用的是不同的C标准库。

特别是在处理预编译的二进制文件时，比如Node.js的C++扩展，这个差异更明显。

举个例子，PhantomJS预置包就无法在Alpine中工作。


## 怎么选择基础镜像？

Alpine、Distroless或是原生镜像到底用哪个？

如果是在生产环境中运行，并且注重安全性， Distroless镜像可能会更合适。

Docker镜像中每增加一个二进制程序，就会给整个应用程序带来一定的风险。

在容器中只安装一个二进制程序即可降低整体风险。

举个例子，如果黑客在运行于Distroless的应用中发现了一个漏洞，他也无法在容器中创建Shell，因为根本就没有。
注意：最小化攻击面是OWASP的推荐做法[5]。
如果更在意要是大小，则可以换成Alpine基础镜像。

这两个都很小，代价是兼容性。Alpine用了一个稍稍有点不一样的C标准库——muslc。时不时会碰到点兼容性的问题。比如这个[6]和这个[7]。

原生基础镜像非常适合用于测试和开发。

它的尺寸比较大，不过用起来就像你主机上安装的Ubuntu一样。并且，你能访问该操作系统里有的所有二进制程序。

下面，回顾一下各个镜像大小：
```
node:8 681MB
node:8结合多阶段构建 678MB
gcr.io/distroless/nodejs 76.7MB
node:8-alpine 69.7MB
```

相关链接：

https://github.com/GoogleCloudPlatform/distroless
https://alpinelinux.org
https://www.musl-libc.org
https://www.busybox.net
https://www.owasp.org/index.php/Minimize_attack_surface_area
https://github.com/grpc/grpc/issues/8528
https://github.com/grpc/grpc/issues/6126

原文链接：https://itnext.io/3-simple-tricks-for-smaller-docker-images-f0d2bda17d1e
