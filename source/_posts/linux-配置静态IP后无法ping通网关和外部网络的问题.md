---
title: linux-配置静态IP后无法ping通网关和外部网络的问题
cover_img: 'http://qiniucdn.timilong.com/1551520939891.jpg'
date: 2019-05-16 18:21:01
tags: Linux
feature_img:
description: Linux日常配置。
keywords: Linux
categories: Linux
---

![cover_img](http://qiniucdn.timilong.com/1551520939891.jpg)

### centos7配置静态IP
centos7安装成功后, 为了保证多个虚拟机的通讯, 需配置静态ip和统一网关, 只需要修改网卡(用ifconfig查看使用的网卡, 我的是ens33)的配置文件就行了。
其他文件不用动(/etc/sysconfig/network  这个文件不用动(否则会ping不通))

网卡路径:  `/etc/sysconfig/network-scripts/ifcfg-ens33`  (rns33为网卡名)
```shell
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
BOOTPROTO="static"  #静态获取ip
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="ens33"
UUID="a8f0def7-cd82-4e97-9615-fc4001fd2282"
DEVICE="ens33"
IPADDR=192.168.204.133   #设置的本机静态ip
GATEWAY=192.168.204.2    #网关
NETMASK=255.255.255.0
DNS1=8.8.8.8
DNS2=114.114.114
ONBOOT="yes"   #重启后使用该网卡
```

修改保存之后重启服务 `service network restart`

然后尝试 `ping www.baidu.com` 或者 `ping 192.168.204.2` (这里写你自己的网关)   如果ping的通就OK了.


### Ubuntu16.04配置静态IP
打开Ubuntu的终端，输入：
```
vim /etc/network/interfaces
```

然后输入如下代码：
```
auto lo
iface lo inet loopback
 
auto ens33
iface ens33 inet static
address 192.168.204.131
netmask 255.255.255.0
gateway 192.168.204.2
```

然后，配置DNS服务器：
> 注: dns也可以在上面的文件直接配置 即:
> 在interfaces末尾加入dns-nameservers 114.114.114.114 8.8.8.8

```
vim /etc/resolv.conf
```

在里面填入:
```
nameserver 114.114.114.114

nameserver 8.8.8.8
```
保存退出然后重启网卡:
```
sudo /etc/init.d/networking restart
```

然后尝试 `ping www.baidu.com` 或者 `ping 192.168.204.2`(这里写你自己的网关), 如果ping的通就OK了.

最后如果用的是VMware的话修改网关或ip后(网卡都已经确定重启), 需要断开 网络适配器 再重新以NAT方式连接, 否则就ping不通网关上不了网。
