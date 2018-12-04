title: python爬虫实战2-爬取百度贴吧的帖子
date: 2016-10-18 14:04:43
categories: python
tags: 爬虫
cover_img: http://qiniucdn.timilong.com/1543736907739.jpg
description: python爬虫实战2-爬取百度贴吧的帖子
---

![tu](http://qiniucdn.timilong.com/1543736907739.jpg)

### 分析百度贴吧的帖子

以[西南民族大学贴吧－9月10月交易贴](http://tieba.baidu.com/p/4763194794)为例子:



1. 标题部分

帖子标题的原HTML:

```
<div class="core_title core_title_theme_bright">
  <h1 class="core_title_txt  " title="【跳蚤市场】2016年9.10月份交易专贴" style="width: 470px">
    【跳蚤市场】2016年9.10月份交易专贴
  </h1>
  <ul class="core_title_btns">
    <li>
      <a id="lzonly_cntn" href="/p/4763194794?see_lz=1" alog-alias="lzonly" class="l_lzonly"><span id="lzonly" class="d_lzonly_bdaside">只看楼主</span>
      </a>
    </li>
    <li id="j_favthread" class="p_favthread" data-field="{&quot;status&quot;:0,&quot;is_anonym&quot;:false}">
      <div class="p_favthr_tip"></div><div class="p_favthr_main">
        <p>收藏</p>
      </div>
    </li>
    <li class="quick_reply">
      <a href="#" id="quick_reply" class="j_quick_reply">回复
      </a>
    </li>       
  </ul>
</div>

```
分析知帖子标题的h1的class属性以"core_title_txt"组成。
所以可以用正则表达式：

```
 pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
```
获得该贴的标题。




2. 回复贴的总页数

页数的原HTML代码:

```
<div class="p_thread thread_theme_7" id="thread_theme_7">
  <div class="l_thread_info">
    <ul class="l_posts_num">
      <li class="l_pager pager_theme_5 pb_list_pager"><span class="tP">1</span>
        <a href="/p/4763194794?pn=2">2</a>
        <a href="/p/4763194794?pn=3">3</a>
        <a href="/p/4763194794?pn=4">4</a>
        <a href="/p/4763194794?pn=5">5</a>
        <a href="/p/4763194794?pn=6">6</a>
        <a href="/p/4763194794?pn=2">下一页</a>
        <a href="/p/4763194794?pn=9">尾页</a>
      </li>
      <li class="l_reply_num" style="margin-left:8px">
        <span class="red" style="margin-right:3px">608</span>回复贴，共
        <span class="red">9</span>页
      </li>
      <li class="l_reply_num">，跳到 
        <input theme="6" id="jumpPage6" max-page="9" type="text" class="jump_input_bright">页&nbsp;
        <button id="pager_go6" type="button" value="确定" class="jump_btn_bright">确定</button>&nbsp;
      </li>
    </ul>
  </div>
  <div id="tofrs_up" class="tofrs_up">
    <a href="/f?kw=%E8%A5%BF%E5%8D%97%E6%B0%91%E6%97%8F%E5%A4%A7%E5%AD%A6&amp;ie=utf-8" title="西南民族大学">&lt;&lt;返回西南民族大学吧</a>
  </div>
</div>
```

分析知帖子主题内容部分的li的class属性以"l_reply_num"组成。
所以可以用正则表达式：

```
pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
```
获得总的页数


3. 帖子内容

帖子内容的原HTML:

```
<div id="post_content_97207207866" class="d_post_content j_d_post_content  clearfix">
  为维护吧内秩序、整合资源方便吧友查看，请各位把各类广告、交易、兼职等信息统一发到此贴，大家有要卖的要买的可以在这里看看。在贴吧内另开贴的你懂的。
  <br>也可发至交易专区<br>交易区吧传送门：
  <a href="http://jump.bdimg.com/safecheck/index?url=x+Z5mMbGPAs95UolpNuq+CwM2BpViN6QmOAUpYcHEp3yh2g54/DNZkwZOyqc+ysHracV4bv5FhgOh7UAFerFKP6yLAEdcrKLyeGknQty2X0jRha1FKRps3NThXBpPvJle+dwuR5U/I3rj2gEWSj0J1ylgIj3lwMhC9PC1kFa9y1H/mFRJ8LD7iZqNqoA+5sYYfeLqDUKUME2ccw3UuJz3St9mSeEws4jeLOj9K+ShbpV92TAmoWV0zA8Zu4mdgY0" target="_blank">http://tieba.baidu.com/f?kw=%CE%F7%C4%CF%C3%F1%B4%F3%BD%BB%D2%D7%C7%F8&amp;fr=itb_favo&amp;fp=favo
  </a>  
  <br>
  另外，出于方便翻阅的目的，各类信息
  <br>
  请勿超过200字＋四张图，大量
  <br>
  刷楼删除，骗子信息自重。
  <br>
  本贴只提供平台，请各位睁大双眼
  <br>
  确认信息真实度。</div>
```

分析知帖子主题内容部分的div的id属性以"post_content_id"组成。
所以可以用正则表达式：

```
pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
```
获得所有楼层的回复内容。


### 代码实现部分:

```
#! /usr/bin/env python2
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re

# 处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')

    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')

    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')

    # 将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')

    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')

    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')

    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)

        # strip()将前后多余内容删除
        return x.strip()


# 百度贴吧爬虫类
class BDTB:
    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self,baseUrl,seeLZ,floorTag):
        # base链接地址
        self.baseURL = baseUrl

        # 是否只看楼主
        self.seeLZ = '?see_lz='+str(seeLZ)

        # HTML标签剔除工具类对象
        self.tool = Tool()

        # 全局file变量，文件写入操作对象
        self.file = None

        # 楼层标号，初始为1
        self.floor = 1

        # 默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.defaultTitle = u"百度贴吧"

        # 是否写入楼分隔符的标记
        self.floorTag = floorTag

    # 传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            # 构建URL
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)

            # 返回UTF-8格式编码内容
            return response.read().decode('utf-8')

        # 无法连接，报错
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因", e.reason
                return None

    # 获取帖子标题
    def getTitle(self,page):
        # 得到标题的正则表达式
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
        result = re.search(pattern,page)
        if result:
            # 如果存在，则返回标题
            return result.group(1).strip()
        else:
            return None

    # 获取帖子一共有多少页
    def getPageNum(self,page):
        # 获取帖子页数的正则表达式
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # 获取每一层楼的内容,传入页面内容
    def getContent(self,page):
        # 匹配所有楼层的内容
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            # 将文本进行去除标签处理，同时在前后加入换行符
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents

    def setFileTitle(self,title):
        # 如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")

    def writeData(self,contents):
        # 向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                # 楼之间的分隔符
                floorLine = "\n" + str(self.floor) + u"-----------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL已失效，请重试"
            return
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        #出现写入异常
        except IOError,e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"



print u"请输入帖子代号"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()

```


### 运行效果:

![运行效果](http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20161018143022.png)


### 结果展示

![结果展示](http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20161018143308.png)
