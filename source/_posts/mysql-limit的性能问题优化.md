---
title: mysql-limit的性能问题优化
cover_img: 'http://qiniucdn.timilong.com/1551520939891.jpg'
date: 2019-05-09 12:59:08
tags: MySQL
feature_img:
description: MySQL limit进行分页会遇到的性能问题及其优化。
keywords: MySQL
categories: MySQL
---

![cover_img](http://qiniucdn.timilong.com/1551520939891.jpg)

## MySQL的分页查询通常通过limit来实现
MySQL的`limit`基本用法很简单。`limit`接收1或2个整数型参数，如果是2个参数，第一个是指定第一个返回记录行的偏移量，第二个是返回记录行的最大数目。初始记录行的偏移量是0。
为了与PostgreSQL兼容，`limit`也支持`limit` # offset #。

## 问题
对于小的偏移量，直接使用limit来查询没有什么问题，但随着数据量的增大，越往后分页，limit语句的偏移量就会越大，速度也会明显变慢。
优化思想：
避免数据量大时扫描过多的记录

解决：
```
子查询的分页方式或者JOIN分页方式。
JOIN分页和子查询分页的效率基本在一个等级上，消耗的时间也基本一致。
```

下面举个例子。一般MySQL的主键是自增的数字类型，这种情况下可以使用下面的方式进行优化。

下面以真实的生产环境的80万条数据的一张表为例，比较一下优化前后的查询耗时：

### 传统limit，文件扫描
```
[SQL]SELECT * FROM tableName ORDER BY id LIMIT 500000,2;

受影响的行: 0
时间: 5.371s
```

### 子查询方式，索引扫描
```
[SQL]
SELECT * FROM tableName
WHERE id >= (SELECT id FROM tableName ORDER BY id LIMIT 500000 , 1)
LIMIT 2;

受影响的行: 0
时间: 0.274s
```


### JOIN分页方式
```
[SQL]
SELECT *
FROM tableName AS t1
JOIN (SELECT id FROM tableName ORDER BY id desc LIMIT 500000, 1) AS t2
WHERE t1.id <= t2.id ORDER BY t1.id desc LIMIT 2;

受影响的行: 0
时间: 0.278s
```
可以看到经过优化性能提高了将近20倍。

## 优化原理
子查询是在索引上完成的，而普通的查询时在数据文件上完成的，通常来说，索引文件要比数据文件小得多，所以操作起来也会更有效率。

因为要取出所有字段内容，第一种需要跨越大量数据块并取出，而第二种基本通过直接根据索引字段定位后，才取出相应内容，效率自然大大提升。

因此，对`limit`的优化，不是直接使用`limit`，而是首先获取到`offset`的id，然后直接使用`limit` [size]来获取数据。
在实际项目使用，可以利用类似策略模式的方式去处理分页，例如，每页100条数据，判断如果是100页以内，就使用最基本的分页方式，大于100，则使用子查询的分页方式。

