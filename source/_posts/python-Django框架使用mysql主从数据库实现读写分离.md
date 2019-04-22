---
title: python-Django框架使用mysql主从数据库实现读写分离
cover_img: 'http://qiniucdn.timilong.com/1551520934786.jpg'
date: 2019-04-22 10:13:58
tags: python
feature_img:
description: Django框架使用mysql主从数据库实现读写分离.
keywords: python
categories: python
---

![cover_img](http://qiniucdn.timilong.com/1551520934786.jpg)

## 配置好mysql主从
参考: [Mysql主从数据库配置]()

 
## 在配置文件中增加slave数据库的配置
```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,  # 主
        'USER': 'root',   # 主数据库用户名
        'PASSWORD': 'password', # 主数据库密码
        'NAME': 'database_name'  # 主数据库名字
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 8306,  #从
        'USER': 'root',   # 从数据库用户名
        'PASSWORD': 'password', # 从数据库密码
        'NAME': 'database_name'  # 从数据库名字
    }
}
```

## 创建数据库操作的路由分发类

在项目封装功能的utils文件夹中创建db_router.py
```python
class MasterSlaveDBRouter(object):
    """数据库主从读写分离路由"""
 
    def db_for_read(self, model, **hints):
        """读数据库"""
        return "slave"
 
    def db_for_write(self, model, **hints):
        """写数据库"""
        return "default"
 
    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return True
```

## 项目setting配置文件中配置读写分离路由
```python
# 配置读写分离
DATABASE_ROUTERS = ['itme_name.utils.db_router.MasterSlaveDBRouter']  # 指定你的路由分发类
```
