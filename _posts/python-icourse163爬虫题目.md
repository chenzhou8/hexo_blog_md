---
title: Python网络爬虫与信息提取-网络爬虫之规则
date: 2017-08-26 23:17:44
categories: python
tags: python
cover_img: http://qiniucdn.timilong.com/1543736711372.jpg
description: Python网络爬虫与信息提取-网络爬虫之规则.

---


[1].下面哪个不是Python Requests库提供的方法？ <code>B. .push() </code>
```
A. .get() 
B. .push() 
C. .post() 
D. .head()
```

[2]Requests库中，下面哪个是检查Response对象返回是否成功的状态属性？ <code>D. status_code</code>
```
A. status
B. headers
C. raise_for_status
D. status_code
```
<!--more-->

[3]Requests库中，下面哪个属性代表了从服务器返回HTTP协议头所推荐的编码方式？ <code>C. encoding</code>
```
A. text
B. headers
C. encoding
D. apparent_encoding
```

[4]Requests库中，下面哪个属性代表了从服务器返回HTTP协议内容部分猜测的编码方式？ <code>A. apparent_encoding</code>
```
A. apparent_encoding
B. text
C. encoding
D. headers
```

[5]Requests库中，下面哪个是由于DNS查询失败造成的获取URL异常？ <code>D. requests.ConnectionError</code>
```
A. requests.Timeout
B. requests.HTTPError
C. requests.URLRequired
D. requests.ConnectionError
```

[6]以下哪个是不合法的HTTP URL？ <code>D. news.sina.com.cn:80</code>
```
A. https://210.14.148.99/
B. http://dwz.cn/hMvN8
C. http://223.252.199.7/course/BIT-1001871002#/
D. news.sina.com.cn:80
```

[7]在Requests库的get()方法中，能够定制向服务器提交HTTP请求头的参数是什么？ <code>A. headers</code>
```
A. headers
B. json
C. data
D. cookies
```

[8]在Requests库的get()方法中，timeout参数用来约定请求的超时时间，请问该参数的单位是什么？ <code>B. 秒</code>
```
A. 毫秒
B. 秒
C. 分钟
D. 微秒
```

[9]下面哪个不是网络爬虫带来的负面问题？ <code>C. 商业利益</code>
```
A. 法律风险
B. 隐私泄露
C. 商业利益
D. 性能骚扰
```

[10]下面哪个说法是不正确的？ <code>B. Robots协议是互联网上的国际准则，必须严格遵守。</code>
```
A. Robots协议是一种约定。
B. Robots协议是互联网上的国际准则，必须严格遵守。
C. Robots协议告知网络爬虫哪些页面可以抓取，哪些不可以。
D. Robots协议可以作为法律判决的参考性“行业共识”。
```

[11]如果一个网站的根目录下没有robots.txt文件，下面哪个说法是不正确的？ <code>B. 网络爬虫可以不受限制的爬取该网站内容并进行商业使用。</code>
```
A. 网络爬虫应该以不对服务器造成性能骚扰的方式爬取内容。
B. 网络爬虫可以不受限制的爬取该网站内容并进行商业使用。
C. 网络爬虫可以肆意爬取该网站内容。
D. 网络爬虫的不当爬取行为仍然具有法律风险。
```

[12]百度的关键词查询提交接口如下，其中，keyword代表查询关键词：<code> C. .get()</code>
```
http://www.baidu.com/s?wd=keyword
```
请问，提交查询关键词该使用Requests库的哪个方法？ 
```
A. .post()
B. .patch()
C. .get()
D. .put()
```

[13]获取网络上某个URL对应的图片或视频等二进制资源，应该采用Response类的哪个属性？ <code>A. .content</code>
```
A. .content
B. .text
C. .status_code
D. .head
```

[14]Requests库中的get()方法最常用，下面哪个说法正确？ <code>A. 服务器因为安全原因对其他方法进行限制，所以，get()方法最常用。</code>
```
A. 服务器因为安全原因对其他方法进行限制，所以，get()方法最常用。
B. get()方法是其它方法的基础，所以最常用。
C. 网络爬虫主要进行信息获取，所以，get()方法最常用。
D. HTTP协议中GET方法应用最广泛，所以，get()方法最常用。
```

[15]下面哪些功能网络爬虫做不到？ <code>C. 爬取某个人电脑中的数据和文件。</code>
```
A. 持续关注某个人的微博或朋友圈，自动为新发布的内容点赞。
B. 爬取网络公开的用户信息，并汇总出售。
C. 爬取某个人电脑中的数据和文件。
D. 分析教务系统网络接口，用程序在网上抢最热门的课。
```

[16]请在上述网络爬虫通用代码框架中，填写空格处的方法名称。
```
try:
    r = requests.get(url)
    r.__________________()
    r.encoding = r.apparent_encoding
    print(r.text)
except:
    print("Error")

答案: raise_for_status
```

[17]在HTTP协议中，能够对URL进行局部更新的方法是什么？
```
答案: PATCH/patch/Patch
```

[18] 下述代码的输出结果是什么？
```
>>> kv = {'k': 'v', 'x': 'y'} 
>>> r = requests.request('GET', 'http://python123.io/ws', params=kv) 
>>> print(r.url)

答案: http://python123.io/ws?k=v&x=y 或 http://python123.io/ws?x=y&k=v 
```

[19]某一个网络爬虫叫NoSpider，编写一个Robots协议文本，限制该爬虫爬取根目录下所有.html类型文件，但不限制其它文件。请填写robots.txt中空格内容：
```
User-agent:NoSpider
Disallow:___________

答案: /*.html 或 /*.HMTL
```

[20]请填写下面语句的空格部分，使得该语句能够输出向服务器提交的url链接。
```
>>>import requests
>>>r =  requests.get(url)
>>>print(r.____________)

答案: request.url
```
