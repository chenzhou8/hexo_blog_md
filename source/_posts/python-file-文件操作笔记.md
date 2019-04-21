---
title: python-file-文件操作笔记
cover_img: 'http://qiniucdn.timilong.com/1551520858891.jpg'
date: 2019-04-21 16:33:56
tags: python
feature_img:
description: Python 文件操作解读.
keywords: python
categories: python
---

![cover_img](http://qiniucdn.timilong.com/1551520858891.jpg)

## 文件属性
```python
file.fileno(): 文件描述符
file.mode :文件打开权限
file.encoding: 文件的编码格式
file.closed: 文件是否关闭
```

## 标准文件
```python
sys.stdin : 文件标准输入
sys.stdout : 文件标准输出
sys.stderr :  文件标准错误
```

## 文件命令行参数
```
sys.argv
```

## 文件的编码格式
```python
1. u''的使用 unicode 编码格式
2. 使用 codecs 模块提供方法创建制定编码格式的文件
3. 函数：codecs.open(fname,mode,encoding,error,buffering)
4. mode: 打开方式
5. encoding: 编码格式
```

## 文件系统
![文件系统](http://qiniucdn.timilong.com/16a38f24d64e31d8)

![python操作文件流程](http://qiniucdn.timilong.com/16a38f316f9ffc64)

## 使用os模块打开文件

> os.open(filename, flage [, mode])

`flage`定义如下
```python
os.O_CREAT：创建文件
os.O_RDONLY: 只读方式打开
os.O_WRONLY: 只写方式打开
os.O_RDWR: 读写方式打开
```
---

```python
os.read(fd,buffersize): 读取文件
os.write(fd,string): 写入文件
os.lseek(fd,pos.how):文件指针操作
os.close(fd):关闭文件
```

![方法1](http://qiniucdn.timilong.com/16a39b4e1cf8e07c)

![方法2](http://qiniucdn.timilong.com/16a39b88599d62bb)
