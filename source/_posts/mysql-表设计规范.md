---
title: mysql-表设计规范
cover_img: 'http://qiniucdn.timilong.com/1551520852529.jpg'
date: 2019-03-03 23:37:14
tags: mysql
feature_img:
description: MySQL数据库表格设计规范
keywords: mysql
categories: mysql
---

![cover_img](http://qiniucdn.timilong.com/1551520852529.jpg)


## 表设计
1) 表必须定义主键，默认为ID，整型自增，如果不采用默认设计必须咨询DBA进行设计评估
2) ID字段作为自增主键，禁止在非事务内作为上下文作为条件进行数据传递
3) 禁止使用外键
4) 多表中的相同列，必须保证列定义一致
5) 国内表默认使用InnoDB，表字符集默认使用gbk，国际默认使用utf8的表
6) 表必须包含gmt_create和gmt_modified字段，即表必须包含记录创建时间和修改时间的字段
7) 单表一到两年内数据量超过500w或数据容量超过10G考虑分表，且需要提前考虑历史数据迁移或应用自行删除历史数据
8) 单条记录大小禁止超过8k（列长度(中文)*2（gbk）/3(utf8)+列长度(英文)*1）
9) 日志类数据不建议存储在MySQL上，优先考虑Hbase或OB，如需要存储请找DBA评估使用压缩表存储

## 字段设计

1) 表被索引列必须定义为not null，并设置default值
2) 禁止使用float、double类型，建议使用decimal或者int替代
3) 禁止使用blob、text类型保留大文本、文件、图片，建议使用其他方式存储（TFS/SFS），MySQL只保存指针信息
4) 禁止使用varchar类型作为主键语句设计

## 语句设计

1) 数据更新建议使用二级索引先查询出主键，再根据主键进行数据更新
2) 禁止使用非同类型的列进行等值查询！

## 其他

1) 禁止使用：存储过程、触发器、函数、视图、事件等MySQL高级功能
2) 禁止使用跨库查询
3) 禁止使用子查询，建议将子查询转换成关联查询
4) 禁止核心业务流程SQL包含：计算操作、多表关联、表遍历case when等复杂查询，建议拆分成单表简单查询
5) varchar长度设计需要根据业务实际需要进行长度控制，禁止预留过长空间。例如status使用varchar(128)进行存储

