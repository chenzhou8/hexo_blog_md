title: python-MySQL数据库操作
date: 2016-07-09 07:25:40
categories: python
tags: python
cover_img: http://qiniucdn.timilong.com/1543736943777.jpg
description: python-MySQL数据库操作.
---

![tu](http://qiniucdn.timilong.com/1543736943777.jpg)

## Python访问DB的官方接口规范

### Python DB API

Python访问数据库的统一接口规范。
[官网](htttps://www.python.org/dev/peps/pep-0249)

Python应用程序通过Python DB API即可完成对不同数据库的访问，对应用程序来说，只需切换少量代码即可实现。

### Python DB API包含的内容：

Python程序----------------------------------->数据库服务器
-数据库连接对象connection.(建立连接)
-数据库交互对象cursor(交互数据)
-数据库异常类exceptions(处理数据库操作过程中的事故)
![python db api](http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20160709073935.png)

### Python DB API访问数据库流程

-开始
-创建connection
-获取cursor
-执行查询、执行命令、获取数据、处理数据
-关闭cursor
-关闭connection(网络资源，一直没有关闭会浪费应用程序和数据库服务器的资源)
-结束

![访问流程](http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20160709075539.png)


## Python开发DB程序的开发环境

![windows 下的python开发环境](http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20160709074444.png)


## Python访问DB的connection、cursor两大对象

### 连接对象：建立Python客户端与数据库的网络连接

创建方法：MySQLdb.Connect(参数):
```
参数名   | 类型   | 说明
host     | 字符串 | MySQL服务器地址
port     | 数字   | MySQL服务器端口号
user     | 字符串 | 用户名
password | 字符串 | 密码
db       | 字符串 | 数据库名称
charset  | 字符串 | 连接编码
```

### connection对象支持的方法:
```
方法名     | 说明
cursor()   | 使用该连接创建并返回游标
commit()   | 提交当前事物
rollback() | 回滚当前事物
close()    | 关闭连接
```

```python
import MySQLdb
conn = MySQLdb.Connect(
                host = '127.0.0.1',
                port = 3306,
                user = 'root',
                passwd = '123456',
                db = 'test_db',
                charset = 'utf-8'
)
cursor = conn.cursor()

print conn
print cursor

cursor.close()
conn.close()

```

### 数据库游标对象cursor

游标对象:用于执行查询和获取结果
cursor对象支持的方法：
```
参数名              | 说明
execute(op[, args]) | 执行一个数据库查询和命令
fetchone()          | 取的结果集的下一行
fetchmany(size)     | 获取结果集的下几行
fetchall()          | 获取结果集中剩下的所有行
rowcount            | 最近一次execute返回数据的行数或者影响行数
close()             | 关闭游标对象
```

其中:
```
execute方法：执行SQL、将结果从数据库获取到客户端
客户端----------------------MySQL服务器
execute(sql语句)----------->执行SQL语句
                               |
                               |
本地缓冲区<----------------- 结果
```


`fetch*()`方法：移动rownumber, 返回缓冲区的数据

## Python执行增、删、改、查操作的实例讲解

### select查询数据

流程图：
![流程图](http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20160712114529.png)

首先，在test_db数据库中创建一个user表格:

```sql
CREATE TABLE 'user' (
    'userid' INT(11) NOT NULL AUTO_INCREMENT,
    'username' VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY ('userid')
)ENGINE = INNODB AUTO_INCREMENT=9 DEFAULT CHARSET = utf8
```

测试cursor方法：

```python
import MySQLdb
conn = MySQLdb.Connect(
                host = '127.0.0.1',
                port = 3306,
                user = 'root',
                passwd = '123456',
                db = 'test_db',
                charset = 'utf8'
                )

cursor = conn.cursor()

sql = "select * from user"
cursor.execute(sql)

rs = cursor.fetchall()

for row in rs:
    print "userid = %s, username = %s" % row

cursor.close()

conn.close()
```

### insert/update/delete更新数据库

流程图：
![流程图](http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20160712124117.png)

事物：访问和更新数据库的一个程序执行单元
- 原子性：事物中包括的诸操作要么都做，要么都不做
- 一致性：事物必需使数据库从一致性状态变到另一个一致性状态
- 隔离性：一个事物的执行不能被其它事物干扰
- 持久性：事物一旦提交，它对数据库的改变就是永久性的

开发中如何使用事物？
- 关闭自动commit：设置conn.autocommit(False)
- 正常结束事物：conn.commit()
- 异常结束事物：conn.rollback()

针对select中test_db数据库的user表格继续进行insert/update/delete:

```python
import MySQLdb

conn = MySQLdb.Connect(
                host = '127.0.0.1',
                port = 3306,
                user = 'root',
                password = '123456',
                db = 'test_db',
                charset = 'utf8'
                )

cursor = conn.cursor()

sql_select = "select * from user"
sql_insert = "insert into user(userid, username) values(10, 'name10')"
sql_update = "update user set username='name91' where userid=9"
sql_delete = "delete from user where userid < 3"

cursor.excute(sql_select)
print cursor.rowcount

cursor.excute(sql_insert)
print cursor.rowcount

cursor.excute(sql_update)
print cursor.rowcount

cursor.excute(sql_delete)
print cursor.rowcount

conn.commit()

cursor.close()

conn.close()

```

测试conn.rollback():
```python
import MySQLdb

conn = MySQLdb.Connect(
               host = '127.0.0.1',
               port = '3368',
               user = 'root',
               password = '123456',
               db = 'test_db',
               charset = 'utf8'
)

cursor = conn.cursor()

sql_select = "select * from user"
sql_insert = "insert into user(userid, username) values(10, name10)"
sql_update = "update user set username = 'name91' where userid = 9" #修改此处的userid为userd,造成异常调用conn.rollback()
sql_delete = "delete from user where useris < 3"

try:
    cursor.execute(sql_select)
    print cursor.rowcount

    cursor.execute(sql_insert)
    print cursor.rowcount

    cursor.execute(sql_update)
    print cursor.rowcount

    cursor.execute(sql_delete)
    print cursor.rowcount
except Exception as e:
    print e
    conn.rollback()

cursor.close()
conn.close()

```

## 完整实例：银行转账实现账户A给账户B转账100元

开始事务-->检查账户A和账户是否可用-->检查账户A是否有100元-->账户A减去100元、账户B加上100元-->提交事务
(出现异常-->回滚事务)

### 代码实现

数据库部分：
在名为bank的数据库中创建account表格：账户的id和账户的金额
```python
CREATE TABLE 'ACCOUNT' (
  `acctid` INT(11) DEFAULT NULL COMMENT '账户ID',
  `money` INT(11) DEFAULT NULL COMMENT '余额'
) ENGINE = INNODB DEFAULT CHARSET = utf8;
```

python代码部分：transfer_money.py
```python
# coding: utf8

import sys
import MySQLdb

class TransferMoney(object):
    def __init__(self, conn):
        self.conn = conn

    def transfer(self, source_acctid, target_acctid, money):
        try:
            self.check_acct_available(source_acctid)
            self.check_acct_available(target_acctid)
            self.has_enough_money(source_acctid, money)
            self.reduce_money(source_acctid, money)
            self.add_money(target_acctid, money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def check_acct_available(self, acctid):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where acctid = %s" % acctid
            cursor.execute(sql)
            print "check_acct_available:" + sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账号%s不存在" % acctid)
        finally:
            cursor.close()

    def has_enough_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where acctid=%s and money>%s" % (acctid, money)
            cursor.execute(sql)
            print "has_enough_money:"  + sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账户%s的钱不足%s" % (acctid, money))
        finally:
            cursor.close()

    def reduce_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money=money-%s where acctid=%s" % (money, acctid)
            cursor.execute(sql)
            print "reduce_money:" + sql
            if cursor.rowcount != 1:
                raise Exception("账户%s减钱失败" % (acctid))
        finally:
            cursor.close()

    def add_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money=money+%s where acctid=%s" % (money, acctid)
            cursor.execute(sql)
            print "add_money:" + sql
            if cursor.rowcount != 1:
                raise Exception("账户%s加钱失败" % (acctid))
        finally:
            cursor.close()


if __name__ == "__main__":
    source_acctid = sys.argv[1]
    target_acctid = sys.argv[2]
    money = sys.argv[3]

    conn = MySQLdb.Connect(host="127.0.0.1", user="root", passwd="jiajin@123", port=3306, db="test_aaa", charset="utf8")

    tr_money = TransferMoney(conn)

    try:
        tr_money.transfer(source_acctid, target_acctid, money)
    except Exception as e:
        print "出现问题" + str(e)
    finally:
        conn.close()
```

