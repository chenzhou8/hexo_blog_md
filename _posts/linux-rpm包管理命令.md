title: Linux-rpm包管理命令
date: 2017-06-16 22:06:39
categories: Linux
tags: Linux
description: RPM的全名为“RedHat Package Manager”, 是由RedHat公司开发的。Rpm是以一种数据库记录的方式将所需要的套件安装到linux主机的一套管理程序
---

## 简介

RPM的全名为“RedHat Package Manager”: 是由RedHat公司开发的。Rpm是以一种数据库记录的方式将所需要的套件安装到linux主机的一套管理程序

RPM主要优点: 
 1. 由于已经编译完成并且打包, 所以安装方便
 2. 由于套件信息已经记录在linux主机的数据库中, 方便查询、升级、卸载。

RPM数据库: /var/lib/rpm
RPM数据库建立可以利用: rpm --rebuilddb
RPM包名格式: 
```
    name-version-release.arch.rpm
    name-version-release-release.arch.rpm
```
    version: 主版本号.此版本号.发行版本号.平台.rpm
```
        主版本号改变: 重大改进
        次版本号改变: 某个子功能发生重大变化
        发行号: 修正了部分bug, 调整了一点功能
```

## rpm命令的详细用法
1. 语法如下
```
1) RPM软件安装命令:
    rpm -i /PATH/TO/PACKAGE_FILE: 安装软件包
    rpm -h: 以#显示安装进度, 每个#表示2%
    rpm -v: 显示安装详细信息
    rpm -vv: 更详细的信息
    rpm -ivh: 一般都是组合使用
    rpm --nodeps: 忽略依赖关系。
    rpm --replacepkgs|repackage: 重新安装、替换原来安装。
    rpm -ivh --oldpackage: 降级安装。
    rpm -ivh --force: 强行安装, 可以实现重装或降级
    rpm --test: 仅测试有没有依赖关系

2) rpm软件查询命令: 
    rpm -q PACKAGE_NAME: 查询指定的包是否安装
    rpm -qa: 查询以安装的所有包
    rpm -qi PACKAGE_NAME: 查询指定包的说明信息
    rpm -ql PACKAGE_NAME: 查询指定包安装后生成的文件列表
    rpm -qc PACKAGE_NAME: 查询制定包安装的配置文件
    rpm -qd PACKAGE_NAME: 查询指定包安装的帮助文件
    rpm -q --scripts PACKAGE_NAME: 查询指定包中包含的脚本
    rpm -qf /path/to/somefile: 查询指定的文件时由那个rpm包安装生成的

    如果某个rpm包尚未安装, 我们需要查询其说明信息, 安装后会生成的文件
    rpm -qpi /PATH/TO/PACKAGE_FILE
        i: 软件说明信息
    rpm -qpl /PATH/TO/PACKAGE_FILE
        l: 软件安装生成文件列表
 
 3) rpm软件升级命令:
    rpm -Uvh /PATH/TO/NEW_PACKAGE_FILE: 如果装有老版本的, 则升级; 否则, 则安装
    rpm -Fvh /PATH/TO/NEW_PACKAGE_FILE: 如果装有老版本的, 则升级; 否则, 则退出
    rpm -Uvh --oldpackage 低版本的包:降级
    
 4) rpm软件卸载命令:
    卸载的时候此包不能被其他软件包依赖
    rpm -e PACKAGE_NAME
    rpm --nodeps: 忽略依赖, 可能会造成其他依赖此包的软件无法正常运行。

5) rpm软件校验命令: 
    rpm -V PACKAGE_NAME: 无输出信息就是正常。
    Fh: 在zsh安装以后修改一下配置文件 

6) rpm重建数据库:
    数据库位置: /var/lib/rpm
    rpm --rebuilddb: 重建数据库, 一定会重新建立。
    rpm --initdb: 初始化数据库, 没有才建立, 有就不用建立。
7) 检验来源合法性及软件完整性: 
    红帽公钥: ls /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
    rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release: 导入秘钥文件 
    rpm -K /PATH/TO/PACKAGE_FILE
    dsa, gpg: 验证来源合法性, 也即验证签名; 可以使用--nosignature,略过此项
    sha1,md5: 验证软件包完整性; 可以使用--nodigest,略过此项
    rpm -K --nodigest /PACKAGE_NAME: 只验证签名。
    Fg: 检验zsh文件包的完整性
```


