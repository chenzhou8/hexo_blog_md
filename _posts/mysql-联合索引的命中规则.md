---
title: mysql-联合索引的命中规则
date: 2018-08-10 11:23:37
tags: MySql
categories: MySql
---

## 联合索引优点
```
查询语句 SELECT T.* FROM T WHERE T.c1=1 AND T.c3=2;  涉及到两列，这个时候我们一般采用一个联合索引(c1, c3); 
而不用两个单列索引，这是因为一条查询语句往往应为mysql优化器的关系只用一个索引
就算有两个索引，也只用一个；

在只用一个的基础之上，联合索引会比单列索引更快；
```

<!--more-->

## 联合索引命中规则

示例如下
1) 首先创建表：<code>CREATE TABLE T (c1 INT, c2 VARCHAR(9), c3 INT, PRIMARY KEY(c1, c3));</code>
这样就建立了一个联合索引：c1,c3

2) 触发联合索引规则:
  1、使用联合索引的全部索引键，可触发索引的使用.
  例如: <code>SELECT T.* FROM T WHERE T.c1=1 AND T.c3=2;</code>

  2、使用联合索引的前缀部分索引键，如“key_part_1 <op>常量”，可触发索引的使用.
  例如：<code>SELECT T.* FROM T WHERE T.c1=1; </code>

  3、使用部分索引键，但不是联合索引的前缀部分如: "key_part_2 <op>常量", 不可触发索引的使用。
  例如: <code>SELECT T.* FROM T WHERE T.c3=1; </code>

  4、使用联合索引的全部索引键，但索引键不是AND操作，不可触发索引的使用。
  例如: <code>SELECT T.* FROM T WHERE T.c3=2 OR T.c1=1; </code>
