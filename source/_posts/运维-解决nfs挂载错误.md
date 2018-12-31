---
title: 运维-解决nfs挂载错误

cover_img: http://qiniucdn.timilong.com/1544683573162.jpg
date: 2018-12-27 12:38:14
tags: 运维
feature_img:
description: 解决nfs挂载错误wrong fs type, bad option, bad superblock.
keywords: 运维
categories: 运维
---

![cover_img](http://qiniucdn.timilong.com/1544683573162.jpg)

## 错误

```
[root@localhost]# mount -t nfs 192.168.0.106:/home/nfs1
mount: wrong fs type, bad option, bad superblock on 192.168.0.106:/home/nfs1,
       missing codepage or helper program, or other error
       (for several filesystems (e.g. nfs, cifs) you might
       need a /sbin/mount.<type> helper program)
       In some cases useful info is found in syslog - try
       dmesg | tail  or so
```


## 解决办法
```
apt-get install nfs-common

或者

yum install nfs-utils
```
