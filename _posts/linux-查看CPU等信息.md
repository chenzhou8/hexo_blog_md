---
title: linux-查看CPU等信息
date: 2018-10-18 11:16:00
tags: Linux
cover_img: http://qiniucdn.timilong.com/1542968653498.jpg
feature_img:
keywords: Linux
categories: Linux
description: 通过Linux自身的一些命令查看CPU、内存、磁盘、主机名、ip配置等信息。
---

![tu](http://qiniucdn.timilong.com/1542968653498.jpg)

> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

## CPU信息
```shell
$ cat /proc/cpuinfo                                       # 查看CPU信息
$ cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c   # 查看CPU的型号
$ cat /proc/cpuinfo | grep physical | uniq -c             # 查看CPU的核心数 
$ getconf LONG_BIT                                        # 64  表示当前CPU运行在64bit模式下
$ cat /proc/cpuinfo | grep flags | grep ' lm ' | wc -l    # 8 (结果大于0, 说明支持64bit计算. lm指long mode, 支持lm则是64bit) 
```

## 内存信息
```shell
$ cat /proc/meminfo 
$ free -h
              total        used        free      shared  buff/cache   available
Mem:            31G        5.0G        3.1G         35M         23G         25G
Swap:            0B          0B          0B

$ grep MemTotal /proc/meminfo   # 查看内存总量
$ grep MemFree /proc/meminfo    # 查看空闲内存量

```

## 磁盘信息
```shell
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev             32G     0   32G   0% /dev
tmpfs           6.3G  667M  5.7G  11% /run
/dev/sdb6       319G   68G  236G  23% /
tmpfs            32G     0   32G   0% /dev/shm
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs            32G     0   32G   0% /sys/fs/cgroup
/dev/sda1       931G  6.3G  925G   1% /ceph-rbd
tmpfs           6.3G     0  6.3G   0% /run/user/1002

$ df -sh <目录名>  # 查看指定目录大小

$ mount | column -t      # 查看挂接的分区状态
$ fdisk -l               # 查看所有分区
$ swapon -s              # 查看所有交换分区
$ hdparm -i /dev/hda     # 查看磁盘参数(仅适用于IDE设备)
$ dmesg | grep IDE       # 查看启动时IDE设备检测状况
```

## 系统
```shell
# uptime                 # 查看系统运行时间、用户数、负载
# cat /proc/loadavg      # 查看系统负载
# hostname               # 查看计算机名
# lspci -tv              # 列出所有PCI设备
# lsusb -tv              # 列出所有USB设备
# lsmod                  # 列出加载的内核模块
# env                    # 查看环境变量
# head -n 1 /etc/issue   # 查看操作系统版本
# uname -a  # 查看当前操作系统内核信息
# cat /etc/issue | grep Linux  # 查看当前操作系统发行版信息
```


## 网络
```shell
$ dmesg | grep -i eth
$ ifconfig               # 查看所有网络接口的属性
$ iptables -L            # 查看防火墙设置
$ route -n               # 查看路由表
$ netstat -lntp          # 查看所有监听端口
$ netstat -antp          # 查看所有已经建立的连接
$ netstat -s             # 查看网络统计信息
```

## 进程
```shell
$ ps aux
$ ps -ef  # 查看所有进程
$ top  # 查看进程实时状态
```

## 用户
```shell
$ w                      # 查看活动用户
$ id <用户名>            # 查看指定用户信息
$ last                   # 查看用户登录日志
$ cut -d: -f1 /etc/passwd   # 查看系统所有用户
$ cut -d: -f1 /etc/group    # 查看系统所有组
$ crontab -l             # 查看当前用户的计划任务
```

## 服务
```shell
$ chkconfig --list       # 列出所有系统服务
$ chkconfig --list | grep on    # 列出所有启动的系统服务
```

## 程序
```shell
$ rpm -qa                # 查看所有安装的软件包
$ apt list  # ubuntu & debian
$ yum list  # centos
```

