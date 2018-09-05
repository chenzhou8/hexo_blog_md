title: loadRunner入门教程
date: 2016-05-31 20:59:13
categoriges: 软件测试
tags: loadRunner
---

测试环境： Windows 7 使用前请关闭电脑管家、安全卫士等安全软件

### loadRunner使用入门
loadRunner是一种预测行为和性能的负载测试工具。
可适用于各种体系架构的自动负责测试，能预测系统行为并评估系统性能。

本篇教程以测试loadRunner自带的webTours网站为例。
<!--more-->
### 1. 启动loadRunner自带的webTours网站。
```
开始菜单->所有程序->HP->Samples->start the web tour server
```

启动后，在浏览器(默认是ie浏览器，google浏览器亲测有效，其它没有测过)输入以下网址访问:
```
http://localhost:1080\webTours
```

### 2. 访问成功后，关闭浏览器，然后打开loadRunner Virtual UserGene Generator:
```
1. 新建一个录制脚本，使用"Web（http/html）"进行创建，此时相当于选择的录制协议就是http协议，
这个协议适合录制web的应用程序。
2. 开始录制，点击开始录制按钮，点击后在弹出框“Url Address”中键入要录制网页的地址
“http://localhost:1080\webTours”，点击确定。浏览器使用默认的IE浏览器。
3. 接着，loadRunner会自动打开浏览器，跳转到你指定的网页。
4. 进行录制脚本的工作，可以选择sign up注册用户然后自动登录订票，
也可以使用默认账户:jojo, 密码:bean登录，开始订票，一步一步操作。
5. 订票完成后，退出登录，然后点击loadRunner控制台的停止按钮。
6. 等待loadRunner自动生成脚本语言。
```

### 3. 录制成功后，可在loadRunner中Action中看到刚刚录制的脚本。
这时需要，重放刚刚录制的脚本，查看是否错误，有错误按照相应错误解决，或者重新录制脚本
，可直接覆盖当前的脚本录制。回放无错误后进行下步操作。

###4. 打开loadRunner Control
```
加载刚刚录制的脚本，设置并发用户数等等参数信息。点击开始运行。等待较长的一段时间。
运行完毕后，生成了一个运行脚本，这时可在菜单栏找到分析结果的按钮。会自动打开loadRunner Analysis分析刚刚运行的结果。
```

###5. 进入loadRunner Analysis后
```
可直接查看到刚刚的并发测试的结果，报表，图等等。
```



