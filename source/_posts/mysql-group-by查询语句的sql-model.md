---
title: mysql-group_by查询语句的sql_model
cover_img: 'http://qiniucdn.timilong.com/ChMkJ1whnwSIL5CbAAF-6exBWj8AAt-BwKT3twAAX8B238.jpg'
date: 2019-09-01 13:16:09
tags: MySQL
feature_img:
description: 为什么查询列表中多了它，GROUP BY语句就会报错呢？
keywords: MySQL
categories: MySQL
---

![cover_img](http://qiniucdn.timilong.com/ChMkJ1whnwSIL5CbAAF-6exBWj8AAt-BwKT3twAAX8B238.jpg)

> 转载自: 掘金，[MySQL：为什么查询列表中多了它，GROUP BY语句就会报错呢？](https://juejin.im/post/5d64d704e51d45620b21c3f4)

## 总结
```
mysql> SELECT * FROM student_score;
+----------+-----------+-----------------------------+-------+
| number   | name      | subject                     | score |
+----------+-----------+-----------------------------+-------+
| 20180101 | 杜子腾    | 母猪的产后护理              |    78 |
| 20180101 | 杜子腾    | 论萨达姆的战争准备          |    88 |
| 20180102 | 杜琦燕    | 母猪的产后护理              |   100 |
| 20180102 | 杜琦燕    | 论萨达姆的战争准备          |    98 |
| 20180103 | 范统      | 母猪的产后护理              |    59 |
| 20180103 | 范统      | 论萨达姆的战争准备          |    61 |
| 20180104 | 史珍香    | 母猪的产后护理              |    55 |
| 20180104 | 史珍香    | 论萨达姆的战争准备          |    46 |
+----------+-----------+-----------------------------+-------+
8 rows in set (0.00 sec)

mysql> SELECT subject, AVG(score) FROM student_score GROUP BY subject;
```

> 把非分组列放到查询列表中会引起争议，导致结果不确定 
