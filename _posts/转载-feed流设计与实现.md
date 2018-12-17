---
title: 转载-feed流设计与实现
cover_img: http://qiniucdn.timilong.com/1544683490997.jpg
date: 2018-12-17 17:19:14
tags: 架构
feature_img:
description: 本文收集了六篇观音湖feed流业务架构设计相关文章。
keywords: 架构
categories: 架构
---

> 转载自: 微信公众号，[架构师之路](https://mp.weixin.qq.com/s/DM0dKHyD3FweVSHcjabLaw)

## Feed流架构设计

[《feed流业务，推拉架构实践》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961230&idx=1&sn=b2ab831a72f54950498d43ac01e26453&chksm=bd2d02528a5a8b444050c242729f764d6435185feb015f81631d75b018b9760b1a90a467e817&scene=21#wechat_redirect)

[《网页端收消息，如何像TCP一样实时》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961175&idx=1&sn=4e74348e9e6c20aa11bf55949b24e20a&chksm=bd2d028b8a5a8b9da078995f26640959a348442e08b87883e25fe5ca371295eb8dbf29b6383d&scene=21#wechat_redirect)

[《群消息，究竟存1份还是多份》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961197&idx=1&sn=dddd9e9de62975d220d167e5bfb94eee&chksm=bd2d02b18a5a8ba7aeb57ed4bcad722ffa98cbfa74ec80e03588d98d2c0b8f716e025f35f28a&scene=21#wechat_redirect)

[《群消息已读回执，究竟是推还是拉》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961184&idx=1&sn=d0add7f47d928febbd1ebd32239f05ce&chksm=bd2d02bc8a5a8baa704268891880e2560969fc1c3ed8cc45325db4313d8b43eb6db641cb469b&scene=21#wechat_redirect)

[《系统通知，究竟是推送还是拉取？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961154&idx=1&sn=277f6ec612555bf5a95585e9a161bb5f&chksm=bd2d029e8a5a8b884c9855b8e315a697a0e8eccf227fb36395334d140dd9eebf2489e99862d3&scene=21#wechat_redirect)

[《状态同步，究竟是推送还是拉取？》](http://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961154&idx=1&sn=277f6ec612555bf5a95585e9a161bb5f&chksm=bd2d029e8a5a8b884c9855b8e315a697a0e8eccf227fb36395334d140dd9eebf2489e99862d3&scene=21#wechat_redirect)

