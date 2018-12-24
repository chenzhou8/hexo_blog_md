title: Linux-ifconfig命令
date: 2017-05-26 22:06:39
categories: Linux
tags: Linux
cover_img: http://qiniucdn.timilong.com/1543736973823.jpg
description: ifconfig命令.
---

![tu](http://qiniucdn.timilong.com/1543736973823.jpg)


## Linux系统的网络配置基本
包括：网络IP的配置、网关路由的配置、主机DNS的配置、主机名的配置等，本篇注重介绍网络IP的配置。


## Linux系统的网络地址配置分为两种方式
暂时的网络配置：利用ifconfig等命令配置的网络信息，会立即生效，但重启网络服务和系统会失效。
永久的网络配置：通过修改系统内的网络配置文件进行的修改，不会立即生效，需要重启网络服务或者系统会生效，并且会永久性的生效。 


## Linux下的网络接口和命名规则
⑴、网络接口：
    lo：本地回环接口
    erh[0-9]：以太网接口
    pppX：点对点的链接

⑵、以太网网卡的命名和驱动配置文件：
    REHL5：/etc/modprobe.conf
    alias ethX 驱动模块
    REHL6：/etc/dev/rules.d/70-persistent-net.rules


## 网络配置之ifconfig
⑴、ifconfig：查看活动的网卡信息，仅限于活动的网卡
    Fg：先查看本地的网卡信息如下--ifconfig

⑵、ifconfig的相关子命令;
    ifconfig eth[0-9]：查看某个网卡的信息
    Fg：查看eth0的网络信息

    ifconfig -a：查看所有的网卡信息，包含活动的与非活动的
    Fg：禁用eth0，然后利用ifconfig -a查看所有网卡信息

    ifconfig ethx IP/MASK：配置某个网卡的ip地址
    Fg：设置eth0的ip地址为172.16.36.5/16

    Ifconfig eth0 172.16.36.5/16

    ifconfig ethx [up|down]：启用或禁用某个网卡

⑶、以上配置的网络信息在重启网络服务或重启系统后，所有配置信息都会消失。
    Linux下重启网络服务的命令：
    REHL5网络服务命令： /etc/init.d/network {start | stop | restart | status}
    REHL6网络服务命令： /etc/init.d/NetworkManger {start | stop | restart | status} 


## route命令:用于查看和修改本机的路由信息
⑴、route：查看本机的路由信息。
    route -n：以数字的方式显示本机的路由信息。

⑵、route的子命令：
    route add ：添加主机路由
    route add -host：添加主机路由
    route add -net：添加网络路由
    route add -net 0.0.0.0：添加默认路由
    格式：route add -net|host DEST gw NEXTHOP
    Fg：通过172.16.32.1访问192.168.0.0/24网段
    route del：删除路由信息
    Route del -host：
    Route del -net：

## 网络配置命令之IP
⑴、IP命令是iproute2软件包内的一个命令，功能比ifconfig更强大，可以对系统配置IP和路由信息。 

⑵、ip link：配置网络接口属性
    ip link show：查看所有网络接口属性信息
    ip -s link show：查看所有统计信息
    ip link set ethX {up|down|arp {on|off}}:设置网络接口的工作属性

⑶、ip addr：配置网络地址
    ip addr show：查看网络信息
    ip addr add IP dev ethX ：配置IP地址（此命令配置的网卡信息利用ifconfig查看不到，需要利用ip addr show查看）
    ip addr add IP dev ethx label ethX:X：配置子Ip并对其加别名
    ip addr show dev ethx to 前缀：查看ethx 上的以前缀开头的信息
    ip addr flush eth1 to 10/8 ：删除eth1上所有的以10开头的ip地址。

⑷、ip route：路由信息
    ip route change|replace :修改路由信息
    ip route add to 目的网段 dev ethx via IP(下一跳IP)
    Fg：增加网段10.0.0.0/8通过172.16.36.3访问的路由信息


## Linux系统下网卡别名设置相关命令和方法
⑴、命令配置法：ifconfig和ip
    Ifconfig ethx:x IP/netmask
    ip addr add IP dev ethx label ethX:X

⑵、配置文件配置法：
    修改/etc/sysconfig/network-scripts/ifcfg-ethx:x
    DEVICE=ethx:x
....
注意：非主要地址不能用DHCP服务获得。 

## IP网络配置文件
⑴、网络配置文件位置：/etc/sysconfig/network
    网络接口配置文件位置：/etc/sysconfig/network-scripts/ifcfg-INTERFACE_NAME
⑵、ifcfg-ethx配置格式： 
    DEVICE=：关联的设备名称，要与文件名的后半部“INTERFACE_NAME”保存一至 
    BOOTPROTO={static|none|dhcp|bootp}：引导协议，要使用静态地址，使用static或none，dhcp表示使用dhcp服务器获取地址。
    IPADDR=：IP地址
    NETMASK=：子网掩码
    GAYEWAY=：设定网关
    ONBOOT=；开机是否自动激活此网络接口
    HWADDR=：硬件地址，要与硬件中的地址保持一致，可省。
    USERCTL={yes|no}：是否允许普通用户控制此接口
    PEERDNS={yes|no}：是否在BOOTPROTO为dhcp时是否接受由dhcp服务器指定的DNS地址
    以上设置不会立即生效，但重启网络服务或主机都会生效。永久生效
    Fg：配置本机ip地址为172.16.36.1/18.


## 路由配置文件
⑴、配置文件位置：/etc/sysconfig/network-scripts/route-ethx
    ethx：表示通过那个网卡路由
⑵、配置格式：
    添加格式一：
    DEST（目的） via NEXTTOP（下一跳）
    添加格式二：
    ADDRESS0=网络地址（目的地址）
    NETMASK0=子网掩码（目的网络）
    GATEWAY0=网关（通过那个网卡的网关）
    ADDRESS1=
    NETMASK1=
    GATEWAY1=
以上设置不会立即生效，但重启网络服务或主机都会生效。


## DNS配置文件
⑴、配置文件位置：/etc/resolv.conf
⑵、配置格式：
    nameserver DNS_IP1
    nameserver DNS_IP2
指定本地解析：
    /etc/hosts下添加
目标主机IP 主机名 主机别名
    fg：172.16.36.1 www.chris.com www
DNS解析过程-->/etc/hosts-->DNS


## 主机名配置文件
⑴、配置文件位置： /etc/sysconfig/network
⑵、配置格式：
    HOSTNAME=名称
    NETWORKING={yes|no}：是否开启网络功能
    NETWORKING
