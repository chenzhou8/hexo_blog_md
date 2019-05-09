---
title: mysql-配置mysql主从数据库.md
cover_img: 'http://qiniucdn.timilong.com/1551520678591.jpg'
date: 2019-04-22 10:23:48
tags: MySQL
feature_img:
description: MySQL主从数据库配置.
keywords: MySQL
categories: MySQL
---

![cover_img](http://qiniucdn.timilong.com/1551520678591.jpg)


## 配置主从同步有很多种方法，可以总结为如下的步骤：
```
（1） 在主服务器上，必须开启二进制日志机制和配置一个独立的ID

（2） 在每一个从服务器上，配置一个唯一的ID，创建一个用来专门复制主服务器数据的账号

（3） 在开始复制进程前，在主服务器上记录二进制文件的位置信息

（4） 如果在开始复制之前，数据库中已经有数据，就必须先创建一个数据快照（可以使用mysqldump导出数据库，或者直接复制数据文件）

（5） 配置从服务器要连接的主服务器的IP地址和登陆授权，二进制日志文件名和位置
```

这里演示主机电脑中的ubuntu⾥⾯的MySQL作为主机 ，使⽤Dokcer安装的MySQL作为从机

## 安装MySQL从机
在docker里面安装mysql的镜像， 此版本的镜像，尽量和⾃⼰MySQL主机版本⼀致

### 可以从docker官⽅镜像 
```
docker image pull mysql:5.7.22 （我的主机mysql版本为5.7.22）
```

### 本地已有docker的镜像可以直接安装
```
docker load -i mysql_docker_5722.tar
```

### 指定从机配置⽂件
运⾏mysql docker镜像，需要在宿主机中建⽴⽂件⽬录⽤于mysql容器保存数据和读取配置⽂件。
在家目录下创建mysql_slave文件夹， 放入mysql的配置文件， 
这里最后一行命令是直接复制主机mysql的配置文件， 在去修改就可以了
```
cd ~
mkdir mysql_slave
cd mysql_slave
mkdir data
cp -r /etc/mysql/mysql.conf.d ./
```

### 配置从机
将docker运行的mysql作为slave运行， 开启前需配置文件

修改port ， server-id和主机做区分， 主机分别是3306， 1 ， 另外不开启日志
```
sudo vim ~/mysql_slave/mysql.conf.d/mysqld.cnf
port  =  8306
general_log  = 0
server-id  = 2
```

### 创建docker容器
创建docker容器,    MYSQL_ROOT_PASSWORD 是创建mysql root用户的密码
```
docker run --name mysql-slave -e MYSQL_ROOT_PASSWORD=mysql -d --network=host -v /home/python/mysql_slave/data:/var/lib/mysql -v /home/python/mysql_slave/mysql.conf.d:/etc/mysql/mysql.conf.d mysql:5.7.22
```

测试， 在ubuntu中使用mysql命令尝试连接docker容器中的mysql
```
mysql -uroot -pmysql -h 127.0.0.1 --port=8306
```

### 冷备份
登录到MySQL主机，收集数据
```
mysqldump -uroot -pmysql --all-databases --lock-all-tables > ~/master_db.sql
```

登录到MySQL从机，同步数据 
```
mysql -uroot -pmysql -h127.0.0.1 --port=8306 < ~/master_db.sql
```

### 配置主机
编辑设置mysqld的配置文件， 设置log_bin 和server_id
```
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
```

```
server-id   = 1
log_bin     =  /var/log/mysql/mysql-bin.log
```

重启主机mysql服务
```
sudo service mysql restart
```

### 热备份
登入主服务器Ubuntu中的mysql，创建用于从服务器同步数据使用的帐号, 这里是slave
```
mysql –uroot –pmysql
```

```
GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' identified by 'slave';
 
FLUSH PRIVILEGES;
```

获取主服务器的二进制日志信息, 查看File, Position
File为使用的日志文件名字，Position为使用的文件位置，这两个参数须记下，配置从服务器时会用到。
```
SHOW MASTER STATUS;
```

配置从服务器slave (docker里面的mysql), 进入docker里面的mysql, 执行命令
```
mysql -uroot -pmysql -h 127.0.0.1 --port=8306
```

```
change master to master_host='127.0.0.1', master_user='slave', master_password='slave',master_log_file='mysql-bin.000006', master_log_pos=590;
master_host：主服务器Ubuntu的ip地址
master_log_file: 前面查询到的主服务器日志文件名======File
master_log_pos: 前面查询到的主服务器日志文件位置======Position
```

这时候已经配置完成， 尝试启动slave服务器， 并查看同步状态
```
start slave;
show slave status \G
```

如果 显示`Slave_IO_Running :Yes, Slave_SQL_Running: Yes`表示同步已经正常运行.
