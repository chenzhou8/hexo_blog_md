---
title: mysql-索引分类及用途
date: 2018-08-10 11:47:57
tags: MySQL
categories: MySQL
cover_img: http://qiniucdn.timilong.com/1543735406642.jpg
description: mysql-索引分类及用途.
---

![tu](http://qiniucdn.timilong.com/1543735406642.jpg)

## 索引分类
MySQL索引分为普通索引、唯一性索引、全文索引、单列索引、多列索引等等。

##  MySQL: 索引以B树格式保存 
Memory存储引擎可以选择Hash或BTree索引，Hash索引只能用于=或<=>的等式比较。 

## 普通索引

```
create index on Tablename (列的列表) 
alter table TableName add index (列的列表) 
create table TableName([...], index [IndexName] (列的列表)
```


## 唯一性索引：create unique index 
```
alter ... add unique 
```

主键：一种唯一性索引，必须指定为primary key 

## 全文索引：从3.23.23版开始支持全文索引和全文检索，FULLTEXT

```
可以在char、varchar或text类型的列上创建。 
```

## 单列索引、多列索引

多个单列索引与单个多列索引的查询效果不同，因为： 
```
执行查询时，MySQL只能使用一个索引，会从多个索引中选择一个限制最为严格的索引。 
```

## 最左前缀(Leftmost Prefixing)：多列索引

```
例如：fname_lname_age索引，以下的搜索条件MySQL都将使用 

fname_lname_age索引: firstname, lastname, age;
                     firstname, lastname;
                     firstname; 其他情况将不使用。 

```

## 根据sql查询语句确定创建哪种类型的索引，如何优化查询 

选择索引列： 
```
a.性能优化过程中，选择在哪个列上创建索引是最重要的步骤之一, 可以考虑使用索引的主要有
  两种类型的列：在where子句中出现的列，在join子句中出现的列。 

b.考虑列中值的分布，索引的列的基数越大，索引的效果越好。 

c.使用短索引，如果对字符串列进行索引，应该指定一个前缀长度，可节省大量索引空间，提升查询速度。 

d.利用最左前缀 

e.不要过度索引，只保持所需的索引。每个额外的索引都要占用额外的磁盘空间，并降低写操作的性能。 
```

在修改表的内容时，索引必须进行更新，有时可能需要重构，因此，索引越多，所花的时间越长。 

## MySQL只对以下操作符才使用索引 

<code> <, <=, =, >, >=, between, in </code>

以及某些时候的 <code> like(不以通配符%或_开头的情形) </code>

## mysql 索引分类 

在数据库表中，对字段建立索引可以大大提高查询速度。
通过善用这些索引，可以令 MySQL的查询和运行更加高效。
索引是快速搜索的关键。MySQL索引的建立对于MySQL的高效运行是很重要的。
下面介绍几种常见的MySQL索引类型。 

### 1、普通型索引 
这是最基本的索引类型，而且它没有唯一性之类的限制。普通索引可以通过以下几种方式创建： 
```
（1）创建索引，例如CREATE INDEX 索引的名字 ON tablename (列名1，列名2,...); 
（2）修改表，例如ALTER TABLE tablename ADD INDEX 索引的名字 (列名1，列名2,...); 
（3）创建表的时候指定索引，例如CREATE TABLE tablename ( [...], INDEX 索引的名字 (列名1，列名 2,...) );
```

### 2、唯一索引 

这种索引和前面的“普通索引”基本相同，但有一个区别：
<code>索引列的所有值都只能出现一次，即必须唯一。</code>

唯一性索引可以用以下几种方式创建：
```
（1）创建索引，例如CREATE UNIQUE INDEX 索引的名字 ON tablename (列的列表); 
（2）修改表，例如ALTER TABLE tablename ADD UNIQUE 索引的名字 (列的列表); 
（3）创建表的时候指定索引，例如CREATE TABLE tablename ( [...], UNIQUE 索引的名字 (列的列表) );
```

### 3、主键 
主键是一种唯一性索引，但它必须指定为“PRIMARY KEY”。
如果你曾经用过<code>AUTO_INCREMENT</code>类型的列，你可能已经熟悉主键之类的概念了。

主键一般在创建表的时候指定，例如:

<code>CREATE TABLE tablename ( [...], PRIMARY KEY (列的列表) );</code>

但是，我们也可以通过修改表的方式加入主键，例如:

<code>ALTER TABLE tablename ADD PRIMARY KEY (列的列表);</code>
每个表只能有一个主键(主键相当于聚合索引，是查找最快的索引)

### 4、单列索引和多列索引 
索引可以是单列索引，也可以是多列索引。 
```
（1）单列索引就是常用的一个列字段的索引，常见的索引。 
（2）多列索引就是含有多个列字段的索引 
```

创建表格: 
```
alter table student add index sy(name,age，score); 
```

其中, 索引sy就为多列索引，多列索引在以下几中情况下才能有效： 
```
select * from student where name='jia' and age>='12';
# where条件中含有索引的首列字段和第二个字段 

select * from student where name='jia';
# where条件中只含有首列字段 

select * from student where name='jia' and score<60;
# where条件中含有首列字段和第三个字段
```

总结：多列索引只有在where条件中含有索引中的首列字段时才有效 

### 5、选择索引列 
应该怎样选择索引列，首先要看查询条件，一般将查询条件中的列作为索引 
