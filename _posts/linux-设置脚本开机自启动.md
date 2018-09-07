---
title: Linux-设置脚本开机自启动
date: 2018-08-16 20:09:14
tags: Linux
categories: Linux
---

### 设置自启动

给Ubuntu添加一个开机启动脚本，操作如下：

1、新建个脚本文件new_service.sh

```
#!/bin/bash
# command content
  
exit 0
```

2、设置权限
```
sudo chmod 755 new_service.sh
```

或者
```
sudo chmod +x new_service.sh
```

3、把脚本放置到启动目录下
```
sudo mv new_service.sh /etc/init.d/
```

4、将脚本添加到启动脚本

执行如下指令，在这里90表明一个优先级，越高表示执行的越晚
```
cd /etc/init.d/
sudo update-rc.d new_service.sh defaults 90
```

5、移除Ubuntu开机脚本
```
sudo update-rc.d -f new_service.sh remove
```

6、通过sysv-rc-conf来管理上面启动服务的启动级别等，还是开机不启动
```
sudo sysv-rc-conf 
```

<!--more-->

### 移除符号链接
当你需要移除这个符号连接时，方法有三种：
```
1. 直接到 /etc/rc2.d 下删掉相应的链接，当然不是最好的方法
2. $ update-rc.d -f s10 remove //推荐做法
3. 如果 update-rc.d 命令你不熟悉，还可以试试看 rcconf 这个命令，也很方便。
```
