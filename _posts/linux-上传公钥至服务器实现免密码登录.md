---
title: linux-上传公钥至服务器实现免密码登录
date: 2016-08-06 11:14:41
tags: Linux
categories: Linux
description: 使用ssh-key实现免输入账号密码登录服务器
---

# 生成秘钥
使用linux有一段时间了，最近在服务器上架设了一个git仓库，每次提交时都使用密码实在是比较反人类，因此就特意研究了一下如何使用ssh密钥来登录服务器。

公钥和私钥的生成
<code>ssh-keygen</code>命令专门是用来生成密钥的。该命令有很多选项，这里列出了最基本的四个：

> -t 用来指定密钥类型（dsa | ecdsa | ed25519 | rsa | rsa1）;
> -P 用来指定密语
> -f 用来指定生成的密钥文件名
> -C 用来添加注释

```shell
ssh-keygen -t rsa -P 123456 -f host -C 'my host key'
# 意思就是新建了密语为123456注释为my host key文件名为host的密钥。此命令会生成host和host.pub两个文件，前者为私钥文件，后者为公钥文件。如果你想免密登录的话，请将密语设置为空。
```

# 将公钥部署到服务器
上一步生成了公钥和私钥后，需要将公钥部署到服务器并用私钥登录。因此首先需要将创建的公钥上传到服务器。
使用scp或者你的工具将公钥上传到服务器并将文件内容追加到<code>~/.ssh/authorized_keys</code>中。例如：

# 在本机上执行此命令，上传公钥
```shell
scp -P your_port host.pub user@hostname:/tmp
```

# 在服务器上执行此命令，追加到authorized_keys
```shell
cd /tmp && cat host.pub >> ~/.ssh/authorized_keys
```

# 更改权限
```shell
chmod 600 ~/.ssh/authorized_keys
```
更改服务器配置
打开<code>/etc/ssh/sshd_config</code>文件，将如下的配置打开：
```shell
RSAAuthentication yes
PubkeyAuthentication yes
AuthorizedKeysFile  .ssh/authorized_keys
```

重启sshd，<code>service sshd restart</code>或者<code>systemctl restart sshd.service。</code>重启之后，服务器已经支持远程ssh连接了

# 连接服务器
本人是通过ssh命令来远程连接服务器的，通过<code>ssh -p your_port username@domain -i your_private_certification</code>命令，就可以连接到服务器了。如果你是通过xshell或者putty来连接的话，导入你的私钥并连接就可以了。

# 其他
如果你想只允许服务器通过公钥和私钥的方式来连接服务器的话，可以将服务器配置文件<code>/etc/ssh/sshd_config</code>中的<code>PasswordAuthentication yes</code>改为<code>PasswordAuthentication No</code>，不过在重启sshd时不要关闭当前的连接，确认通过私钥能连接到服务器才可以关闭。否则，一旦私钥连不上，密码连接方式又被禁用了，恐怕你就要告别你的服务器了。

