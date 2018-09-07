title: mysql-linux下基本操作
date: 2016-07-13 00:08:18
categories: MySql
tags: MySql
---

### 打开终端，进入root
```
    su -i
```

输入密码：
```
    ******
```
<!--more-->

### 进入MySQL
```
    mysql -h localhost -u root -p
```

回车

输入密码：
```
    ******
```

成功进入mysql，页面如下：
```
root@timilong-pc:~# mysql -h localhost -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 7
Server version: 5.6.28-1 (Debian)

Copyright (c) 2000, 2015, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>

```

 输入help：
```
mysql> help

For information about MySQL products and services, visit:
   http://www.mysql.com/
   For developer information, including the MySQL Reference Manual, visit:
      http://dev.mysql.com/
      To buy MySQL Enterprise support, training, or other products, visit:
         https://shop.mysql.com/

         List of all MySQL commands:
         Note that all text commands must be first on line and end with ';'
         ?         (\?) Synonym for `help'.
         clear     (\c) Clear the current input statement.
         connect   (\r) Reconnect to the server. Optional arguments are db and host.
         delimiter (\d) Set statement delimiter.
         edit      (\e) Edit command with $EDITOR.
         ego       (\G) Send command to mysql server, display result vertically.
         exit      (\q) Exit mysql. Same as quit.
         go        (\g) Send command to mysql server.
         help      (\h) Display this help.
         nopager   (\n) Disable pager, print to stdout.
         notee     (\t) Don't write into outfile.
         pager     (\P) Set PAGER [to_pager]. Print the query results via PAGER.
         print     (\p) Print current command.
         prompt    (\R) Change your mysql prompt.
         quit      (\q) Quit mysql.
         rehash    (\#) Rebuild completion hash.
         source    (\.) Execute an SQL script file. Takes a file name as an argument.
         status    (\s) Get status information from the server.
         system    (\!) Execute a system shell command.
         tee       (\T) Set outfile [to_outfile]. Append everything into given outfile.
         use       (\u) Use another database. Takes database name as argument.
         charset   (\C) Switch to another charset. Might be needed for processing binlog with multi-byte charsets.
         warnings  (\W) Show warnings after every statement.
         nowarning (\w) Don't show warnings after every statement.

         For server side help, type 'help contents'

```

### MySQL常用操作
注意：MySQL中每个命令后都要以分号；结尾。

#### 显示数据库

```
    mysql> show databases;
```

返回结果：
```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| test_aaa           |
+--------------------+
4 rows in set (0.00 sec)

mysql> 

```

mysql库非常重要，它里面有MySQL的系统信息，我们改密码和新增用户，实际上就是用这个库中的相关表进行操作。

#### 显示数据库中的表
打开库，对每个库进行操作就要打开此库，类似于foxpro 
```
    mysql> use test_aaa;
```

返回结果：
```
mysql> use test_aaa;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> 

```

显示表格：
```
    mysql>show tables;
```

返回结果：
```
mysql> show tables;
+--------------------+
| Tables_in_test_aaa |
+--------------------+
| account            |
+--------------------+
1 row in set (0.00 sec)

mysql> 

```

在数据库test_aaa中有一个名为account的表格。

#### 显示数据表的结构
输入：
```
    mysql> describe account;
```

返回结果：
```
mysql> describe account;
+--------+---------+------+-----+---------+-------+
| Field  | Type    | Null | Key | Default | Extra |
+--------+---------+------+-----+---------+-------+
| acctid | int(11) | YES  |     | NULL    |       |
| money  | int(11) | YES  |     | NULL    |       |
+--------+---------+------+-----+---------+-------+
2 rows in set (0.00 sec)

mysql> 

```

#### 显示表中的记录
输入：
```
    mysql> select * from account;
```

返回结果：
```
mysql> select * from account;
+--------+-------+
| acctid | money |
+--------+-------+
|      1 |    30 |
|      2 |   110 |
+--------+-------+
2 rows in set (0.00 sec)

mysql> 

```

#### 创建一个新的数据库
输入：
```
   mysql> create database 库名；-->不指定编码方式
   mysql> create database `timilong_tiffocr` default character set utf8 collate utf8_general_ci; -->指定编码方式
```

例如：穿件一个名字为test_db的数据库：
```
mysql> create database test_db;
Query OK, 1 row affected (0.00 sec)

mysql> 

```

#### 创建一个新的表格
输入：
```
    mysql> use 库名;    
    mysql> create table 表名(字段设定列表);
```

例如：在刚创建的test_db数据库中建立name表，表中有id(序号，自动增长)，xm(姓名)，xb(性别)，csny(出身年月)四个字段。
```
mysql> use test_db;
Database changed
mysql> create table name (id int(3) auto_increment not null primary key ,xm char(8), xb char(2), csny date)charset=utf8;
Query OK, 0 rows affected (0.32 sec)

mysql> 

```

可以用describe命令察看刚建立的表结构。
```
    mysql> describe name;
    +-------+---------+------+-----+---------+----------------+
    | Field | Type    | Null | Key | Default | Extra          |
    +-------+---------+------+-----+---------+----------------+
    | id    | int(3)  | NO   | PRI | NULL    | auto_increment |
    | xm    | char(8) | YES  |     | NULL    |                |
    | xb    | char(2) | YES  |     | NULL    |                |
    | csny  | date    | YES  |     | NULL    |                |
    +-------+---------+------+-----+---------+----------------+
    4 rows in set (0.00 sec)

    mysql> 

```

#### 增加记录
例如：增加几条相关纪录。
```
mysql> insert into name values('', '张三', '男', '1971-10-01');
Query OK, 1 row affected, 3 warnings (0.11 sec)

mysql> insert into name values('', '白云', '女', '1972-05-20');
Query OK, 1 row affected, 3 warnings (0.09 sec)

mysql> 

```

可用select命令来验证结果。
```
mysql> select * from name;
+----+--------+------+------------+
| id | xm     | xb   | csny       |
+----+--------+------+------------+
|  1 | 张三   | 男   | 1971-10-01 |
|  2 | 白云   | 女   | 1972-05-20 |
+----+--------+------+------------+
2 rows in set (0.00 sec)

mysql> 

```

#### 修改记录
例如：将张三的出生年月改为1971-01-10
```
    mysql> update name set csny='1971-01-10' where xm='张三';
```

查看结果:
```
mysql> update name set csny="1971-01-10" where xm="张三";
Query OK, 1 row affected (0.12 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> select * from name;
+----+--------+------+------------+
| id | xm     | xb   | csny       |
+----+--------+------+------------+
|  1 | 张三   | 男   | 1971-01-10 |
|  2 | 白云   | 女   | 1972-05-20 |
+----+--------+------+------------+
2 rows in set (0.00 sec)

mysql> 

```

#### 删除记录
例如：删除张三的记录
```
    mysql> delete from name where xm="张三";
```

查看结果：
```
mysql> delete from name where xm="张三";
Query OK, 1 row affected (0.11 sec)

mysql> select * from name;
+----+--------+------+------------+
| id | xm     | xb   | csny       |
+----+--------+------+------------+
|  2 | 白云   | 女   | 1972-05-20 |
+----+--------+------+------------+
1 row in set (0.00 sec)

mysql> 

```

#### 删除表格
```
    mysql> drop table 表名;
```

#### 删除数据库
```
    mysql> drop database 库名;
```

### 查看MySQL的编码
MySQL默认编码是Latin1，不支持中文，要支持中文需要把数据库的默认编码修改为gbk或者utf8。

需要以root用户身份登陆才可以查看数据库编码方式(以root用户身份登陆的命令为：>mysql -h localhost -u root  –p,之后输入root用户的密码)，查看数据库的编码方式命令为:
```
show variables like 'character%';
```

查看结果：
```
mysql> show variables like 'character%';
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | latin1                     |
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | latin1                     |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
8 rows in set (0.00 sec)

mysql> 

```

以上可知数据库的编码方式是latin1. 数据库服务器编码为latin1.
需要修改为gbk或者utf8.

修改编码方式：
```
set charcter_set_database = utf8;
set charcter_set_server = utf8;
```
以上方法经过测试后发现，是在当前环境中修改编码方式成功。
当退出后编码方式又恢复为以前的latin1编码。

另外一种查看编码的方式：
```
show variables like 'collation%';
```

### 修改MySQL中某个表格的编码
利用sql语句进行修改，举例说明：

#### 将表test的编码方式改为utf8
```
    mysql> alter table `test` default character set utf8;
```

#### 将表test中name字段的编码方式改为utf8
```
    mysql> alter table `test` change `name` `name` varchar(36) character set utf8;
```

###  linux下mysql修改配置文件的编码方式
修改mysql的配置文件,使数据库与服务器操作系统的字符集设置一致。
```
待完善
```

### 创建表格时默认编码方式为utf8
```
CREATE DATABASE `test2` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
```


