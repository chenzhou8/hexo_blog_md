title: python-简单的爬虫
date: 2016-07-08 09:55:35
categories: python
tags: python
cover_img: http://qiniucdn.timilong.com/1543735236912.jpg
description: 爬虫可以从一个URL出发，访问所有它所关联的URL，并从每个页面中提取我们所需要的价值数据。

---

### 爬虫简介
爬虫：一段自动抓取互联网信息的程序
爬虫可以从一个URL出发，访问所有它所关联的URL，并从每个页面中提取我们所需要的价值数据。
爬虫技术的价值：互联网数据为我所用

### 简单爬虫架构

#### 爬虫调度端：启动爬虫，监视爬虫的运行情况
* URL管理器：对将要爬取的URL，和已经爬取过的URL进行管理
* 网页下载器：从URL管理器中取出一个将要爬取的URL, 传送给网页下载器。网页下载器会将指定的URL页面下载下来，存储成一个字符串。
* 网页解析器：将网页下载器存储的字符串传送给网页解析器进行解析，一方面会解析出有价值的数据，以及指向其它页面的URL，这些URL可以补充进URL管理器。


#### 运行流程
![http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20160708101206.png](http://qiniucdn.timilong.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20160708101206.png)


### URL管理器

#### URL管理器：管理待抓取的URL集合和已抓取URL集合
* 防止重复抓取、防止循环抓取
* 添加新的URL到待抓取的集合中
* 在添加新的URL的同时：还需判断待添加的URL是否已经在容器中
* 获取待爬取的URL
* 获取待爬取的URL同时：判断是否还有待爬去的URL
* 如果该URL被爬取后，我们将该URL从待爬取状态移动到已爬取状态。


#### URL管理器实现方式
* 将待爬取的URL集合直接存储在内存中
    * python内存
        * 待爬取的URL集合：set()-python set()可以直接去除集合中重复的元素
        * 已爬取的URL集合：set()
* 将URL存储在关系数据库中
    * MySQL
        * 建立urls表格
            * 字段1：url
            * 字段2：is_crawled-标志该url是否被爬取
* 将URL存储在缓存数据库中
    * redis(高性能，大公司)
        * 待爬取的URL集合：set
        * 已爬取的URL集合：set


### 网页下载器(urllib2)
将互联网上的URL对应的网页下载到本地的工具，是爬虫的核心组件。
网页下载器：

* 将URL对应的互联网网页以html格式下载到本地，存储成本地文件或者字符串


#### python的网页下载器：urllib2
python官方基础模块，支持直接的网页下载，或者向网页提交一些需要用户输入的数据。还支持需要用户登录访问的cookie处理，需要代理访问的代理处理等增强功能。


#### urllib2下载网页方法1：最简洁方法

```
urllib2.urlopen(url)
```

完整代码：
```
import urllib2

#直接请求
url = 'www.baidu.com'
response = urllib2.urlopen(url)

#获取状态码，如果是200表示获取成功。
code = response.getcode()

#读取获取的内容
if code == 200:
    context = response.read()

```


#### urllib2下载网页的方法2：添加data、http header
将url、data、header传送飞urllib2.Request类，生成一个request的对象，使用：
```
urllib2.urlopen(request)
```

完整代码：
```
import urllib2

# 创建Request对象
request = urllib2.Request(url)

# 添加数据
request.add_data('a', '1') #将用户的a信息值设置为1

# 添加http的header
request.add_header('User-Agent', 'Mozilla/5.0') #将爬虫伪装成Mozilla的浏览器

# 发送请求获取结果
response = urllib2.urlopen(request)
```


#### urllib2下载网页方法3: 添加特殊情景的处理器
* 部分网页需要用户登录才能访问：需要添加cookie的处理-使用HTTPCookieProcessor.
* 部分网页需要代理才能访问：使用ProxyHandler
* 部分网站使用https加密访问：使用HTTPSHandler
* 部分网页的URL相互自动跳转关系：使用HTTPRedirectHandler 

将以上四种的handler都传送给:

```
opener = urllib2.build_opener(handler)#使用build_opener()方法创建一个opener的对象

urllib2.install_opener(opener)  #让该模块具有上述handler的处理能力。

urllib2.urlopen(url)   (or  urllib2.open(request))
```

完整代码：
```
import urllib2, cookielib

#创建cookie容器
cj = cookielib.CookieJar()

#创建1个opener
opener = urllib.build_opener(urllib2.HTTPCookieProcessor(cj))

#给urllib2安装opener
urllib2.install_opener(opener)

#使用带有cookie的urllib2访问网页
response = urllib2.urlopen("http://www.baidu.com/")
```

#### 完整代码
```
import urllib2, cookielib

url = "http://www.baidu.com"

print ("第一种方法")

response1 = urllib2.urlopen(url)
print response1.getcode()
print len(response1.read())

print ("第二种方法")
request = urllib2.Request(url)
request.add_header("usr-agent", "Mozilla/5.0")
response2 j= urllib2.urlopen(request)
print response2.getcode()
print len(response2.read())


print ("第三种方法")
cj = cookielib. CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
response3 = urllib2.urlopen(url)
print response3.getcode()
print "======cookie========\n"
print cj
print "======html==========\n"
print response3.read()

```
#### requests
第三方插件，提供更为强大的功能。


### 网页解析器(Beautiful Soup)
从网页中提取有价值的数据工具。
网页解析器以下载好的html网页形成的字符串作为输入，通过解析，得到有价值的数据或者新的url列表。

#### 网页解析器分类
网页解析器有以下三种：

* 正则表达式: 将整个网页文档当作一个字符串，使用模糊匹配的方式来提取出有价值的数据或者url。-模糊匹配
* python自带的html.parser模块: python自带的解析html的解析模块。-结构化解析
* Beautiful Soup: 第三方插件，可以使用python自带的html.parser或者lxml作为解析器。-结构化解析
* lxml: 第三方插件解析html、xml网页。-结构化解析

结构化解析：将整个文档那个当作一个DOM树，以树的方式进行上下级元素间遍历，详情参考w3c-DOM.

#### Beautiful Soup详解
[Beautiful Soup官网](http://www.crummy.com/software/BeautifulSoup/)
Python的第三方库，用于从HTML或者XML中提取数据。

安装并测试beautifulsoup4
- 安装：pip install beautifulsoup4
- 测试：import bs4

语法：
下载号的html网页字符串->创建BeautifulSoup对象(将怎个字符串加载成DOM树)->进行节点的搜索(find_all:搜索出所有满足要求的节点, find:搜索出第一个满足要求的节点)->访问节点的名称、属性 、文字。

```html
<a href="123.html" class="article_link" >Python </a>
```

创建BeautifulSoup对象：

```
from bs4 import BeautifulSoup

# 根据html网页字符串创建BeautifulSoup对象
soup = BeautifulSoup(
                 html_doc,            #html文档字符串
                 'html.parser'        #html解析器
                 from_encoding='utf8' #html文档的编码
                 )

# 方法：find_all(name, attrs, string)

# 查找所有标签为a的节点
soup.find_all('a')

# 查找所有标签为a，链接符合/view/123.html形式的节点
soup.find_all('a', href='/view/123.html')
soup.find_all('a', href=re.compile(r'/view/\d+\.html'))

# 查找所有标签为div, class为abc，文字为Python的节点
soup.find_all('div', class_='abc', string='Python')

# 通过以上代码得到节点：<a href='1.html'>Python</a>

# 获取查找到的节点的标签名称
node.name

# 获取查找到的a节点的href属性
node['href']

# 获取查找到的a节点的链接文字
node.get_text()

```

BeautifulSoup实例测试：

```
import urllib2
from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
  <title></title>
</head>
<body>
  <div class="header">
  </div>
  <div class="content">
    <p class="p">this is a test</p>
    <a href="http://www.baidu.com" class="btn btn-success">百度</a>
    <a href="http://www.imooc.com" class="btn btn-primary">慕课</a>
    <a href="http://www.timilong.com class="timilong">timilong</a>
  </div>
  <div class="footer">
  </div>
</body>
</html>
"""

soup = Beautiful(html_doc, 'html.parser', from_encoding='utf-8')

print ("获取所有的链接\n")
links = soup.find_all('a')
for link in links:
    print link.name, link['href'], link.get_text()

print ("获取timilong的链接\n")
link_node = soup.find('a', href='http://www.timilong.com')
print link_node.name, link_node['href'], link_node.get_text()

print ("正则表达式\n")
link_node = soup.find('a', href=re.compile(r'timilong'))
print link_node.name, link_node['href'], link_node.get_text()

print ("获取class='p'的文字")
link_node = soup.find('p', class_="p")
print link_node.name, link_node.get_text()

```

### 完整的python爬虫实例

#### 确定目标
爬取百度百科Python词条相关的1000个页面数据

#### 分析目标
目标：爬取百度百科Python词条相关的1000个页面数据
入口页：http://baike.baidu.com/view/21087.htm
URL格式：
  -词条页面URL：/view/125379.htm
数据格式：
-标题

```
<dd class="lemma-Wgt-lemmaTitle-title"><h1>...</h1></dd>
```

-简介

```
<div class="lemma-summary">...</div>
```

页面编码：utf-8

#### 代码结构
- __init__.py:初始化
- url_manager.py:URL管理器
- spider_main.py:爬虫调度程序
- html_downloader:html下载器
- html_parser:html解析器
- html_outputer:html页面输出

#### spider_main.py

```
from baike_spider import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print ('craw %d : %s' % (count, new_url)) #当前打印的是第几个url 
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                if count == 1000:
                    break

                count = count + 1
            except:
                print 'craw failed'

            self.outputer.output_html()

if __name__ == "__main__":
    root_url = "http://baike.baidu.com/view/21087.htm"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)   
```

#### url_manager.py

```
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url): #向url_manager中添加一个新的url
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls): #向url_managet中批量添加url   
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self): #判断url_manager中是否有新的待爬取的url
        return len(self.new_urls) != 0

    def get_new_url(self): #从url_manager中获取一个新的待爬取的url
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

```

#### html_downloader.py

```
class HtmlDownloader(object):
    def downloader(self, url):
        if url is None:
            return None
        
        response = urllib2.urlopen(url)

        if response.getcode() != 200:
            return None

        return response.read()
```

#### html_parser.py

```
class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # /view/123.htm
        links = soup.find_all('a', href=re.conpile(r"/view/\d+\.htm"))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, jpage_url, soup):
        res_data = {}
        
        #<dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>...</dd>
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        
        res_data['title'] = title_node.get_text()
        
        # <div class="lemma-summary">...</div>
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()

        res_data['url'] = page_url

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return 
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
        
```

#### html_outputer.py

```
class HtmlOutput(object):
    def __init__(self):
        self.datas = []

    def collect_data(self):#搜集数据
        if data is None:
            return 
        self.datas.append(data)


    def output_html(self):#将搜集的数据放入html中用页面输出
        fout = open('output.html', 'w')

        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        
        #ascii编码
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
```

#### 实验结果

