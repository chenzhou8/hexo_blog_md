title: Linux-grep命令
date: 2017-07-16 22:06:39
categories: linux
tags: linux
---

## 语法

1. 语法如下
```
[root@www ~]# grep [-acinv] [--color=auto] '搜寻字符串' filename

选项与参数：
    -a : 将 binary 文件以 text 文件的方式搜寻数据
    -c : 计算找到 '搜寻字符串' 的次数
    -i : 忽略大小写的不同，所以大小写视为相同
    -n : 顺便输出行号
    -v : 反向选择，亦即显示出没有 '搜寻字符串' 内容的那一行！
    --color=auto : 可以将找到的关键词部分加上颜色的显示喔！
```

<!--more-->

2. 例子
```
用 dmesg 列出核心信息，再以 grep 找出内含 eth 那行,在关键字所在行的前两行与后三行也一起捉出来显示
[root@www ~]# dmesg | grep -n -A3 -B2 --color=auto 'eth'
245-PCI: setting IRQ 10 as level-triggered
246-ACPI: PCI Interrupt 0000:00:0e.0[A] -> Link [LNKB] ...
247:eth0: RealTek RTL8139 at 0xee846000, 00:90:cc:a6:34:84, IRQ 10
248:eth0: Identified 8139 chip type 'RTL-8139C'
249-input: PC Speaker as /class/input/input2
250-ACPI: PCI Interrupt 0000:00:01.4[B] -> Link [LNKB] ...
251-hdb: ATAPI 48X DVD-ROM DVD-R-RAM CD-R/RW drive, 2048kB Cache, UDMA(66)
# 如上所示，你会发现关键字 247 所在的前两行及 248 后三行也都被显示出来！
# 这样可以让你将关键字前后数据捉出来进行分析啦！
```

## 详细教程

[linux-grep常见用法](http://www.cnblogs.com/ggjucheng/archive/2013/01/13/2856896.html)

## 常用用法

1. 在当前目录下找出所有.py结尾的文件, 搜索其它也是类似的
```
ls -al | grep *.py
```

