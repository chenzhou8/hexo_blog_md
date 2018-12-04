---
title: mysql-关于MySQL内核-一定要知道的-转载
cover_img: http://qiniucdn.timilong.com/1543735257967.jpg
date: 2018-12-04 10:56:46
tags: MySQL
feature_img:
description: MySQL技术内核相关文章收集.
keywords: MySQL
categories: MySQL
---

> 转载自: 微信公众号，[架构师之路](https://mp.weixin.qq.com/s/tmkRAmc1M_Y23ynduBeP3Q)


## [《InnoDB，为何并发如此之高？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961444&idx=1&sn=830a93eb74ca484cbcedb06e485f611e&chksm=bd2d0db88a5a84ae5865cd05f8c7899153d16ec7e7976f06033f4fbfbecc2fdee6e8b89bb17b&scene=21#wechat_redirect)
文章介绍了：
（1）什么是并发控制；

（2）并发控制的常见方法：锁，数据多版本；

（3）redo，undo，回滚段的实践；

（4）InnoDB如何利用回滚段实现MVCC，实现快照读。


结论是，<b>快照读(Snapshot Read)</b>，这种不加锁的读，是InnoDB高并发的核心原因之一。

番外篇：[《快照读，在RR和RC下的差异》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961513&idx=1&sn=e955133cbd87c652d9bcbccad608190e&chksm=bd2d0d758a5a84632046e7c692064b415621ae329426adf77ae03e4a0cc55d662d6d4c543019&scene=21#wechat_redirect)

快照读，在可重复读与读提交两种事务隔离级别下，有微小的差异，文章通过案例做了简单叙述。

## InnoDB的七种锁

先从一个有意思的案例，引出了锁的话题。

假设有数据表：
```
t(id int PK, name);
```
目前的记录是：
```
10, shenjian

20, zhangsan

30, lisi
```

事务A先执行，并且处于未提交状态：
```
delete from t where id=40;
```

事务A想要<b>删除一条不存在的记录</b>。

事务B后执行：
```
insert into t values(40, ‘c’);
```

事务B想要插入一条主键不冲突的记录。

<b>问题1</b>：事务B是否阻塞？

<b>问题2</b>：如果事务B阻塞，锁如何加在一条不存在的记录上呢？

<b>问题3</b>：事务的隔离级别，索引类型，是否对问题1和问题2有影响呢？


接下来的几篇文章详细的介绍了InnoDB内核中的七种锁。

[《InnoDB插入自增列，是表锁吗？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961455&idx=1&sn=4c26a836cff889ff749a1756df010e0e&chksm=bd2d0db38a5a84a53db91e97c7be6295185abffa5d7d1e88fd6b8e1abb3716ee9748b88858e2&scene=21#wechat_redirect)

这一篇，介绍了InnoDB内核的第一种锁，自增锁（Auto-inc Locks）。

[《InnoDB并发插入，会不会互斥？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961461&idx=1&sn=b73293c71d8718256e162be6240797ef&chksm=bd2d0da98a5a84bfe23f0327694dbda2f96677aa91fcfc1c8a5b96c8a6701bccf2995725899a&scene=21#wechat_redirect)

这一篇，介绍了InnoDB内核的三种锁：

- 共享/排他锁（Shared and Exclusive Locks）

- 意向锁（Intention Locks）

- 插入意向锁（Insert Intention Locks）

[《InnoDB，select为何会阻塞insert？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961471&idx=1&sn=da257b4f77ac464d5119b915b409ba9c&chksm=bd2d0da38a5a84b5fc1417667fe123f2fbd2d7610b89ace8e97e3b9f28b794ad147c1290ceea&scene=21#wechat_redirect)

这一篇，介绍了InnoDB内核最有意思的三种锁：

- 记录锁（Record Locks）

- 间隙锁（Gap Locks）

- 临键锁（Next-Key Locks）

这几篇文章，有大量的案例，相信大家会有收获。


## 索引到底是怎么实现的？

这两篇文章很重要，讲解MySQL索引底层实现，也是阅读量最高的几篇之一。

[《数据库索引，到底是什么做的？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961486&idx=1&sn=b319a87f87797d5d662ab4715666657f&chksm=bd2d0d528a5a84446fb88da7590e6d4e5ad06cfebb5cb57a83cf75056007ba29515c85b9a24c&scene=21#wechat_redirect)

这一篇，介绍了哈希索引，树索引，数据预读/局部性原理，B+树的优化思路。

[《MyISAM与InnoDB的索引差异究竟是啥？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961494&idx=1&sn=34f1874c1e36c2bc8ab9f74af6546ec5&chksm=bd2d0d4a8a5a845c566006efce0831e610604a43279aab03e0a6dde9422b63944e908fcc6c05&scene=21#wechat_redirect)

在上一篇基础之上，用图例讲述了MyISAM与InnoDB的索引差异与实践。


## [《InnoDB如何巧妙实现，事务的4种隔离级别？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961498&idx=1&sn=058097f882ff9d32f5cdf7922644d083&chksm=bd2d0d468a5a845026b7d2c211330a6bc7e9ebdaa92f8060265f60ca0b166f8957cbf3b0182c&scene=21#wechat_redirect)
聊MySQL，聊锁，聊事务，一定逃不开<b>事务的隔离级别</b>，本文简述了读未提交，读提交，可重复读，串行化的巧妙实现。


## [《别废话，各种SQL到底加了什么锁？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961508&idx=1&sn=9f31a95e5b8ec16fa0edc7de6087d2a1&chksm=bd2d0d788a5a846e3bf16d300fb9723047bd109fd22682c39bdf7ed4e77b167e333460f6987c&scene=21#wechat_redirect)
这是一篇直接给结论的文章：
- 普通select

- 加锁select

- update与delete

- insert

各类SQL语句分别加了什么锁？

## [《超赞，InnoDB调试死锁的方法！》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961535&idx=1&sn=b62e9d71836ac5cf2d3cedf69e1ef395&chksm=bd2d0d638a5a84750adfc39d7e177a63330d6bde0f56600764b2d79e0fb9d96ad69e26e19ff1&scene=21#wechat_redirect)
死锁的复现和调试都是很困难的，本文通过几个案例，分享了复现与调试并发事务+死锁的方法，大家一定要动起手来，这样印象才会更加深刻。

## [《MySQL不为人知的主键与唯一索引》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961550&idx=1&sn=8c6de40ae8ac8a52095071fe0ff0fe03&chksm=bd2d0d128a5a8404733b0d6835c38c8c89a292af6dfdcb77da6b73cc2a2122f0f2571bc32428&scene=21#wechat_redirect)

本文分享了MySQL中最常见的两类约束：主键与唯一索引约束，并细聊了这两类约束在InnoDB与MyISAM上的差异，有个MyISAM大坑，一定要注意绕过。

## 其他
[《InnoDB的五项最佳实践，知其所以然》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961428&idx=1&sn=31a9eb967941d888fbd4bb2112e9602b&chksm=bd2d0d888a5a849e7ebaa7756a8bc1b3d4e2f493f3a76383fc80f7e9ce7657e4ed2f6c01777d&scene=21#wechat_redirect)
这是一篇聊InnoDB实践的文章：关于count(*)，关于全文索引，关于事务，关于外键，关于行锁与表锁，不仅会使用，还要知其所以然。

[《MySQL5.6，InnoDB的一些新特性》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961448&idx=1&sn=b1be68798cfcb4511d62853d51b1ad12&chksm=bd2d0db48a5a84a27d098e3387d60c277f635d4d5ea6c3e0ad70b94a2151a6cc62ae65ddc365&scene=21#wechat_redirect)

MySQL5.6，介绍了InnoDB的一些新特性，例如：居然能够支持memcached插件了，居然能把InnoDB表放在DVD或者CD里，是不是有点意思？

## 总结
[《架构师之路17年精选80篇》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651960945&idx=1&sn=d08f33c5f317fee8956252da8e0236b6&chksm=bd2d03ad8a5a8abb0370b826b7384a4095a5ed36238f0911d102b0ceee8e5d2fbe3bc80c56d9&scene=21#wechat_redirect)
