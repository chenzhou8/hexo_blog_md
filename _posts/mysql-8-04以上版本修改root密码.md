---
title: mysql-8.04以上版本修改root密码
date: 2018-08-08 12:16:24
tags: MySQL
---

# 忘记root密码

## 用安全方式打开mysql服务，然后更新存密码的表

```
>>> sudo mysqld_safe --skip-grant-tables

Logging to '/usr/local/mysql-5.7.23-macos10.13-x86_64/data/localhost.err'.
2018-08-08T03:58:25.6NZ mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql-5.7.23-macos10.13-x86_64/data
2018-08-08T03:58:27.6NZ mysqld_safe mysqld from pid file /usr/local/mysql-5.7.23-macos10.13-x86_64/data/localhost.pid ended
```

<!--more-->

## 新开终端、更新密码

登录, 不需要密码
```
mysql -u root
```

use mysql
```
>>> use mysql;

>>> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';  # 123456为新密码

>>> FLUSH PRIVILEGES;

>>> exit
```

重新登录, 需要密码
```
mysql -uroot -p123456

# 成功进入
```

# 没有忘记root密码，只是需要一个新密码
```
mysqladmin -u用户名 -p旧密码 password 新密码 
```
