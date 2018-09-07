---
title: linux-上传公钥至服务器实现免密码登录
date: 2018-08-06 11:14:41
tags: Linux
categories: Linux
---

# 在客户端生成秘钥

```
>>> ssh-keygen -t rsa  # 如果已经生成则直接查看cat .ssh/id_rsa.pub是否有内容
```


# 将客户端的公钥添加到server端的.ssh/authorized_keys中实现免密登录

```
>>> ssh-copy-id -i .ssh/id_rsa.pub root@47.xx.yy.zzz
>>> 输入root的密码 <enter>
```

<!--more-->

# 上传成功可看到

![上传成功](http://7xorah.com1.z0.glb.clouddn.com/ssh-copy-id.png)

# 免密登录

```
ssh root@47.xx.yy.zzz 
```

后续如有需要、可在服务上关闭密码登录
