title: deepin 2015加载windows 7启动项
date: 2016-05-09 19:50:04
tags: 操作系统
categories: 操作系统
cover_img: http://qiniucdn.timilong.com/1543735445857.jpg
description: deepin 2015加载windows 7启动项.
---

![tu](http://qiniucdn.timilong.com/1543735445857.jpg)

### 安装deepin 2015后无法加载出windows 7启动项解决方法

在终端输入如下命令：

```
grub-mkconfig -o /boot/grub/grub.cfg
```

然后回车;

查看启动菜单，出现windows 7的启动项。

重启电脑， OK。
