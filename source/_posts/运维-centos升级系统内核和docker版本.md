---
title: 运维-centos升级系统内核和docker版本
cover_img: http://qiniucdn.timilong.com/1544683520171.jpg
date: 2019-01-18 11:29:59
tags: 运维
feature_img:
description: CentOS 7 上升级Docker，并升级系统内核
keywords: 运维
categories: 运维
---

![cover_img](http://qiniucdn.timilong.com/1544683520171.jpg)

> 升级docker原文：https://blog.csdn.net/kongxx/article/details/78361048
> 升级系统内核原文: https://www.jianshu.com/p/726bd9f37220

## 命令行
```
$ yum update
$ yum erase docker docker-common docker-client docker-compose  # 卸载安装好的旧版本的docker

$ vim /etc/yum.repos.d/docker.repo

   [dockerrepo]
   name=Docker Repository
   baseurl=https://yum.dockerproject.org/repo/main/centos/7/
   enabled=1
   gpgcheck=1
   gpgkey=https://yum.dockerproject.org/gpg

$ yum install -y docker-engine
$ yum install -y docker-compose
$ docker --version

-------------------------------------------------------------------------

$ uname -a
$ rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
$ rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
$ yum --disablerepo="*" --enablerepo="elrepo-kernel" list available
$ yum --enablerepo=elrepo-kernel install kernel-ml
$ uname -sr
$ vim /etc/default/grub

   GRUB_DEFAULT=0
   GRUB_TIMEOUT=5
   GRUB_DEFAULT=0
   GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
   GRUB_DISABLE_SUBMENU=true
   GRUB_TERMINAL_OUTPUT="console"
   GRUB_CMDLINE_LINUX="rd.lvm.lv=centos/root rd.lvm.lv=centos/swap crashkernel=auto rhgb quiet"
   GRUB_DISABLE_RECOVERY="true"

$ grub2-mkconfig -o /boot/grub2/grub.cfg
$ shutdown now -r
$ uname -sr
```
