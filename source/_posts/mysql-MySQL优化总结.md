---
title: MySQL优化总结
cover_img: 'http://qiniucdn.timilong.com/ChMkJlwhnwaIJ0Y-AAL4x4oByVsAAt-BwK3fvoAAvjf984.jpg'
date: 2019-08-13 22:00:39
tags: MySQL
feature_img:
description: MySQL优化的一些总结.
keywords: MySQL
categories: MySQL
---

![cover_img](http://qiniucdn.timilong.com/ChMkJlwhnwaIJ0Y-AAL4x4oByVsAAt-BwK3fvoAAvjf984.jpg)

## 存储引擎的选择(MyISAM和Innodb)
存储引擎：MySQL中的数据、索引以及其他对象是如何存储的，是一套文件系统的实现。

5.1之前默认存储引擎是MyISAM, 5.1之后默认存储引擎是Innodb。

#### 功能差异
![zhihu](https://pic1.zhimg.com/80/v2-0e38e0faa85d457ad767f98da68fd424_hd.jpg)

#### 选择依据

MyISAM引擎设计简单，数据以紧密格式存储，所以某些读取场景下性能很好。

如果没有特别的需求，使用默认的Innodb即可。

MyISAM：以读写插入为主的应用程序，比如博客系统、新闻门户网站。

Innodb：更新（删除）操作频率也高，或者要保证数据的完整性；并发量高，支持事务和外键保证数据完整性。比如OA自动化办公系统。

#### 官网建议

官方建议使用Innodb,上面只是告诉大家,数据引擎是可以选择,不过大多数情况还是不要选为妙

## 字段设计
数据库设计3大范式:

- 第一范式（确保每列保持原子性）
- 第二范式（确保表中的每列都和主键相关）
- 第三范式（确保每列都和主键列直接相关，而不是间接相关）

通常建议使用范式化设计,因为范式化通常会使得执行操作更快。但这并不是绝对的,范式化也是有缺点的,通常需要关联查询，不仅代价昂贵,也可能使一些索引策略无效。

所以,我们有时需要混同范式化和反范式化,比如一个更新频率低的字段可以冗余在表中,避免关联查询

#### 单表字段不宜过多

建议最多30个以内

字段越多,会导致性能下降,并且增加开发难度(一眼望不尽的字段,我们这些开发仔会顿时傻掉的)

#### 使用小而简单的合适数据类型

a.字符串类型
```
固定长度使用char,非定长使用varchar,并分配合适且足够的空间

char在查询时,会把末尾的空格去掉;
```

b.小数类型
```
一般情况可以使用float或double,占用空间小,但存储可能会损失精度

decimal可存储精确小数,存储财务数据或经度要求高时使用decimal
```

c.时间日期
```
datetime:

范围:1001年~9999年
存储:8个字节存储,以YYYYMMDDHHMMSS的格式存储
时区:与时区无关


timestamp:

范围:1970年~2038年
存储:4个字节存储,存储以UTC格式保存,与UNIX时间戳相同
时区:存储时对当前的时区进行转换,检索时再转换回当前的时区

1.通常尽量使用timestamp,因为它占用空间小,并且会自动进行时区转换,无需关心地区时差

2.datetime和timestamp只能存储最小颗粒度是秒,可以使用BIGINT类型存储微秒级别的时间戳
```

d.大数据 blob和text
```
blob和text是为存储很大的数据的而设计的字符串数据类型,但通常建议避免使用

MySQL会把每个blob和text当做独立的对象处理,存储引擎存储时会做特殊处理,当值太大,innoDB使用专门的外部存储区域进行存储,行内存储指针,然后在外部存储实际的值。这些都会导致严重的性能开销
```

#### 尽量将列设置为NOT NULL

a.可为NULL的列占用更多的存储空间

b.可为NULL的列,在使用索引和值比较时,mySQL需要做特殊的处理,损耗一定的性能

建议:通常最好指定列为NOT NULL,除非真的需要存储NULL值

#### 尽量使用整型做主键

a.整数类型通常是标识列最好的选择,因为它们很快并且可以使用AUTO_INCREMENT

b.应该避免使用字符串类型作为标识列,因为它们很消耗空间,并且通常比数字类型慢

c.对于完全"随机"的字符串也需要多加注意。例如：MD5(),SHAI()或者UUID()产生的字符串。这些函数生成的新值也任意分布在很大空间内，这会导致INSERT和一些SELECT语句很缓慢

## 索引

#### 使用索引为什么快

- 索引相对于数据本身,数据量小
- 索引是有序的，可以快速确定数据位置
- InnoDB的表示索引组织表,表数据的分布按照主键排序

就好比书的目录,想要找到某一个内容,直接看目录便可找到对应的页

#### 索引的存储结构

a.B+树

b.哈希(键值对的结构)

MySQL中的主键索引用的是B+树结构,非主键索引可以选择B+树或者哈希

通常建议使用B+树索引



因为哈希索引缺点比较多:
```
1.无法用于排序

2.无法用于范围查询

3.数据量大时,可能会出现大量哈希碰撞,导致效率低下
```

#### 索引的类型

按作用分类:
```
1.主键索引:不解释,都知道

2.普通索引:没有特殊限制,允许重复的值

3.唯一索引:不允许有重复的值,速度比普通索引略快

4.全文索引:用作全文搜索匹配,但基本用不上,只能索引英文单词,而且操作代价很大
```

按数据存储结构分类:

1.聚簇索引

> 定义：数据行的物理顺序与列值（一般是主键的那一列）的逻辑顺序相同，一个表中只能拥有一个聚集索引。 主键索引是聚簇索引,数据的存储顺序是和主键的顺序相同的

2.非聚簇索引

> 定义：该索引中索引的逻辑顺序与磁盘上行的物理存储顺序不同，一个表中可以拥有多个非聚集索引。 聚簇索引以外的索引都是非聚集索引,细分为普通索引、唯一索引、全文索引,它们也被称为二级索引。

如下图《高性能MySQL》 Innodb存储数据和索引的关系

![zhihu](https://pic1.zhimg.com/80/v2-e60cf162b49402bc91056d167bfb2460_hd.jpg)


主键索引的叶子节点存储的是"行指针",直接指向物理文件的数据行。

二级索引的叶子结点存储的是主键值

<b>覆盖索引: </b> 可直接从非主键索引直接获取数据无需回表的索引

比如:

假设t表有一个(clo1,clo2)的多列索引
```python
select clo1,clo2 from t where clo = 1
```

那么,使用这条sql查询,可直接从`(clo1,clo2)`索引树中获取数据,无需回表查询

因此我们需要尽可能的在`select`后只写必要的查询字段，以增加索引覆盖的几率。

多列索引: 使用多个列作为索引,比如`(clo1,clo2)`

使用场景: 当查询中经常使用`clo1`和`clo2`作为查询条件时,可以使用组合索引,这种索引会比单列索引更快

需要注意的是,多列索引的使用遵循最左索引原则

假设创建了多列索引`index(A, B, C)`，那么其实相当于创建了如下三个组合索引：
```
1.index(A,B,C)

2.index(A,B)

3.index(A)
```
这就是最左索引原则，就是从最左侧开始组合。

#### 索引优化

1.索引不是越多越好,索引是需要维护成本的

2.在连接字段上应该建立索引

3.尽量选择区分度高的列作为索引, 区分度`count(distinct col)/count(*)`
表示字段不重复的比例, 比例越大扫描的记录数越少，状态值、性别字段等区分度低的字段不适合建索引

4.几个字段经常同时以`AND`方式出现在`Where`子句中,可以建立复合索引,否则考虑单字段索引

5.把计算放到业务层而不是数据库层

6.如果有 `order by`、`group by` 的场景，请注意利用索引的有序性。 `order by` 最后的字段是组合索引的一部分，并且放在索引组合顺序的最后，避免出现 `file_sort` 的情况，影响查询性能。

例如对于语句 `where a=? and b=? order by c`，可以建立联合索引(a,b,c)。

`order by` 最后的字段是组合索引的一部分，并且放在索引组合顺序的最后，避免出现 `file_sort(外部排序)` 的情况，影响查询性能。

例如对于语句 `where a=? and b=? order by c`，可以建立联合索引`(a, b, c)`。
如果索引中有范围查找，那么索引有序性无法利用，如 `WHERE a>10 ORDER BY b;` 索引`(a,b)`无法排序。

#### 可能导致无法使用索引的情况
```
1.is null 和 is not null

2.!= 和 <> (可用in代替)

3."非独立列":索引列为表达式的一部分或是函数的参数
```

例如:

表达式的一部分: `select id from t where id +1 = 5`

函数参数: `select id from t where to_days(date_clo) >= 10`

4.`like`查询以`%`开头

5. `or` (`or`两边的列都建立了索引则可以使用索引)

6. 类型不一致

如果列是字符串类型，传入条件是必须用引号引起来，不然无法使用索引
```python
select * from tb1 where email = 999;
```

## Sql优化建议

1.首先了解一下sql的执行顺序,使我们更好的优化
```python
(1)FROM:数据从硬盘加载到数据缓冲区，方便对接下来的数据进行操作

(2)ON:join on实现多表连接查询,先筛选on的条件,再连接表

(3)JOIN:将join两边的表根据on的条件连接

(4)WHERE:从基表或视图中选择满足条件的元组

(5)GROUP BY:分组，一般和聚合函数一起使用

(6)HAVING:在元组的基础上进行筛选，选出符合条件的元组（必须与GROUP BY连用）

(7)SELECT:查询到得所有元组需要罗列的哪些列

(8)DISTINCT:去重

(9)UNION:将多个查询结果合并

(10)ORDER BY：进行相应的排序

(11)LIMIT:显示输出一条数据记录
```

- `join on`实现多表连接查询，推荐该种方式进行多表查询，不使用子查询(子查询会创建临时表, 损耗性能)。
- 避免使用`HAVING`筛选数据,而是使用`where`
- `ORDER BY`后面的字段建立索引, 利用索引的有序性排序,避免外部排序
- 如果明确知道只有一条结果返回，`limit 1` 能够提高效率

2. 超过三个表最好不要 `join`

3.避免 `SELECT *`，从数据库里读出越多的数据，那么查询就会变得越慢

4.尽可能的使用 `NOT NULL`列,可为`NULL`的列占用额外的空间,且在值比较和使用索引时需要特殊处理,影响性能

5.用`exists`、`not exists`和`in`、`not in`相互替代

原则是哪个的子查询产生的结果集小，就选哪个
```python
select * from t1 where x in (select y from t2)
select * from t1 where exists (select null from t2 where y =x)
```

`IN`适合于外表大而内表小的情况；
`exists`适合于外表小而内表大的情况

6、使用`exists`替代`distinct`

当提交一个包含一对多表信息（比如部门表和雇员表）的查询时，避免在`select`子句中使用`distinct`，一般可以考虑使用`exists`代替，`exists`使查询更为迅速，因为子查询的条件一旦满足，立马返回结果。

低效写法：
```python
select distinct dept_no,dept_name from dept d,emp e where d.dept_no=e.dept_no
```

高效写法：
```python
select dept_no,dept_name from dept d where exists (select 'x' from emp e where e.dept_no=d.dept_no)
```

备注：
> 其中x的意思是：因为exists只是看子查询是否有结果返回，而不关心返回的什么内容，因此建议写一个常量，性能较高！

用`exists`的确可以替代`distinct`，不过以上方案仅适用`dept_no`为唯一主键的情况，如果要去掉重复记录，需要参照以下写法：
```python
select * from emp where dept_no exists (select Max(dept_no)) from dept d, emp e where e.dept_no=d.dept_no group by d.dept_no)
```

7、避免隐式数据类型转换

隐式数据类型转换不能适用索引，导致全表扫描！
`t_tablename`表的`phonenumber`字段为`varchar`类型

以下代码不符合规范：
```python
select column1 into i_l_variable1 from t_tablename where phonenumber=18519722169;
```

应编写如下：
```python
select column1 into i_lvariable1 from t_tablename where phonenumber='18519722169';
```

8.分段查询

在一些查询页面中，当用户选择的时间范围过大，造成查询缓慢。
主要的原因是扫描行数过多。这个时候可以通过程序，分段进行查询，循环遍历，将结果合并处理进行展示。

## Expalin 分析执行计划

`explain`显示了`mysql`如何使用索引来处理`select`语句以及连接表。可以帮助选择更好的索引和写出更优化的查询语句。

例:
```python
explain SELECT user_name from sys_user where user_id <10
```

该语句连接类型为`range`, 使用主键索引进行了范围查询, 估计扫描了100行数据

更多含义详看下面表格从上可看出

![zhihu](https://pic4.zhimg.com/80/v2-ed8326097720340c80d151800d5691a7_hd.jpg)
