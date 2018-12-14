---
title: python网络爬虫与信息提取
date: 2017-09-10 20:04:18
categroies: python
tags: python
cover_img: http://qiniucdn.timilong.com/1543736952322.jpg
description: python网络爬虫与信息提取
---

![tu](http://qiniucdn.timilong.com/1543736952322.jpg)

## 课程内容
```
1. Requests: 自动爬去HTML页面，自动网络请求提交
2. robots.txt: 网络爬虫排除标准
3. Beautiful Soup: 解析HTML页面
4. Projects: 实战项目A/B
5. Re: 正则表达式详解-提取页面关键信息
6. Scrapy*: 专业网络爬虫框架介绍，网络爬虫原理介绍，
```

## 第0周 网络爬虫之前奏
```
1. 课程内容导学
2. 工具介绍与选择
```

## 第1周 网络爬虫之规则
### Requests库入门
```
安装方法: pip install requests

测试:
    import requests

    response = requests.get("htttp://www.baidu.com")
    response.encoding = 'utf-8'
    status = response.status_code
    context = response.text
    headers = response.headers
    print(type(response))
    print(status)
    print(headers)
    print(context)

7个主要方法: 
    1. requests.request()  -->  构造一个请求，支撑以下各方法的基础方法
    2. requests.get()      -->  获取HTML网页的主要方法，对应HTTP的GET
    3. requests.head()     -->  获取HTML网页头信息的方法，对应HTTP的HEAD
    4. requests.post()     -->  向HTML网页提交POST请求的方法，对应于HTTP的POST
    5. requests.put()      -->  向HTML网页提交PUT请求的方法，对应于HTTP的PUT
    6. requests.patch()    -->  向HTML网页提交局部修改请求，对应于HTTP的PATCH
    7. requests.delete()   -->  向HTML网页提交删除请求的方法，对应于HTTP的DELETE 

① requests.request(method, url, **kwargs):
    method: 请求方式
        r = requests.request('GET', url, **kwargs)
        r = requests.request('HEAD', url, **kwargs)
        r = requests.request('POST', url, **kwargs)
        r = requests.request('PUT', url, **kwargs)
        r = requests.request('PATCH', url, **kwargs)
        r = requests.request('DELETE', url, **kwargs)
        r = requests.request('OPTIONS', url, **kwargs)  # 向服务器获取参数说明

    url: 将要获取的目标url
    **kwargs: 控制访问的参数, 均为可选参数
        params: 字典或者字节序列, 作为参数增加到url中
            >>> kv = {'key1': 'value1', 'key2': 'value2'}
            >>> r = requests.request('GET', 'http://python123.io/ws', params=kv)
            >>> print(r.url)
            ... http://python123.io/ws?key1=value1&key2=value2

        data: 字典,字节序列或者文件对象,作为Requests的内容
            >>> kv = {'key1': 'value1', 'key2': 'value2'}
            >>> r = requests.request('POST', 'http://python123.io/ws', data=kv)
            >>> body = "Requests主体内容"
            >>> r = requests.request('POST', 'http://python123.io/ws', data=body)

        json: JSON格式的文件数据, 作为Request的内容
            >>> kv = {'key1': 'value1', 'key2': 'value2'}
            >>> r = requests.request('POST', 'http://python123.io/ws', json=kv)

        headers: 字典, 定制HTTP头信息
            >>> hd = {'user-agent': 'Chrome/10'}
            >>> r = requests.request('POST', 'http://python123.io/ws', headers=hd)

        cookies: 字典或者CookieJar, Request中的cookie, 一般用于访问带有cookie效验的url
        auth: 元组, 之初HTTP验证功能
        files: 字典类型, 向URL传递文件
            >>> fs = {'file': open('data.xls', 'rb')}
            >>> r = requests.request('POST', 'http://python123.io/ws', files=fs)

        timeout: 设定超时时间, 以秒为单位
            >>> r = requests.request('GET', 'http://www.baidu.com', timeout=10)

        proxies: 字典类型, 设定访问代理服务器, 可以增加登录认证
            >>> pxs = {'http': 'http://user.pass@10.10.10.1:1234', 'https': 'https://10.10.10.1:4321'}
            >>> r = requests.request('POST', 'http://www.baidu.com', proxies=pxs)

        allow_redirects: True/False, 默认为True, 重定向开关
        stream: True/False, 默认为True, 获取内容立即下载开关
        verify: True/False, 默认为True, 认证SSL证书的开关
        cert: 本地SSL证书的路径字段

② requests.get(url, params=None, **kwargs)方法:
    url: 拟获取页面的URL链接
    params: url中的额外参数，字典或者字节流格式，可选
    **kwargs: 12个控制访问的参数，可选
        >>> url = "http://www.baidu.com"
        >>> response = requests.get(url)  # requests.get() --> 构造一个向服务器请求资源的Request对象
        # 返回一个包含服务器对应URL所有资源的Response对象response, 爬虫返回内容
        # requests.get(url, params=None, **kwargs)

    get()方法内部实现:
        def get(url, params=None, **kwargs):
            """ Sends a GET request
            :param url: 
            :param params:
            :param \*\*kwargs:
            :return: :class: Response <Respose> object
            :rtype: requests.Response
            """
            kwargs.setdefaulg('allow redirects', True)
            return request('get', url, params=params, **kwargs)

③ requests.head(url, **kwargs)
④ requests.post(url, data=None, json=None, **kwargs)
⑤ requests.put(url, data=None, **kwargs)
⑥ requests.patch(url, data=None, **kwargs)
⑦ requests.delete(url, **kwargs)

说明: requests的七个常用方法实际上后面留个方法是对requst方法的封装，便于使用

Response对象的属性:
    response = requests.get("http://www.baidu.com")
    response.text:  HTTP响应内容的字符串形式，即url对应的页面内容
    response.encoding: 从HTTP header中猜测的响应内容的编码方式
    response.headers: HTTP响应头信息
    response.content: HTTP响应内容的二进制形式(图片以二进制存储，可用该方法还原)
    response.status_code:  HTTP请求的返回状态, 200表示链接成功，400表示失败
    response.apparent_encoding: 从内容中分析出的响应内容编码方式(备选编码方式)

    response.status_code == 200 --> response.text/response.encoding/response.apparent_encoding/response.content
    response.status_code == 404/其它 --> 某些原因出错，产生异常

理解Response编码:
   response.encoding: 从HTTP头中猜测的编码方式  # HTTP头中的charset, 返回存储在response.encoding, 
                                                # 如果服务器不存在charset要求，则默认ISO-8859-1不能解析中文, 从头中猜测
   response.apparent_encoding: 从内容中分析出的响应内容编码方式(备用编码方式), 从HTTP内容中解析出的编码, 更准确, 有分析内容

   如果response.text乱码, 则应检测上述两种编码，并:
   encoding = response.apparent_encoding  
   response.encoding = encoding
   response.text  # 正常显示
```

#### Requests库认识
```
1. 理解Requests库的异常
    requests.ConnectionError: 网络链接错误异常，如DNS查询失败，拒绝链接等 
    requests.HTTPError: HTTP错误异常
    requests.URLRequired: URL缺失异常
    requests.TooManyRedirects: 超过大量重定向次数，产生重定向异常
    requests.ConnectTimeout: 链接远程服务器超时异常
    requests.Timeout: 请求URL超时，产生超时异常

2. 异常状态
    response = requests.get("http://www.baidu.com")
    response.raise_for_status() # 如果该状态不是200, 产生requests.HTTPError 异常

3. requests爬取网页的通用代码框架
##################################
    import reqeusts
    def getHTMLText(url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status() # 如果该状态不是200, 产生requests.HTTPError 异常
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as err:
            return "产生异常: {0}".format(err)

    if __name__ == "__main__":
        url = "https://www.baidu.com"
        result = getHTMLText(url)
        print(result)
##################################

4. HTTP协议
HTTP: Hypertext Transfer Protocol, 超文本传输协议
    HTTP是一个基于“请求与响应”模式的，每次请求都是独立无状态的应用层协议
    HTTP协议采用URL作为定位网络资源的通用格式
    URL格式: http://host[:port][path]
        host: 合法的Internet主机域名或者IP地址
        port: 端口号，缺省端口为80
        path: 请求的资源的路径
    例子: http://www.bit.edu.cn
          http://220.182.111.188/duty
    HTTP URL理解: URL是通过HTTP协议存取资源的Internet路径，一个URL对应一个数据资源
    HTTP协议对资源的操作:
        GET:     请求获取URL位置的资源: 全部资源
        HEAD:    请求获取URL位置资源的响应消息报告，即获得该资源的: 头部信息
        POST:    请求向URL位置的资源后附加新的数据
        PUT:     请求向URL位置存储一个资源，覆盖原URL位置的资源
        PATCH:   请求局部更新URL位置的资源，即改变该处资源的部分内容
        DELETE:  请求删除URL位置存储的资源

        OPTIONS: 查看上述操作

    PATCH与PUT的区别:
        假设URL位置有一组数据UserInfo， 包括UserID, UserName等20个字段。
        需求: 用户修改了UserName, 其它不变。
        方法: 1. 采用PATCH, 仅发送修改后的UserName. 节省带宽。
              2. 采用PUT, 必须将所有20个字段一并提交到URL， 未提交字段被删除。

HTTP方法与Requests的方法一一对应。
    例子:
        # head()方法
        response = requests.head("https://www.baidu.com")
        response.headers # headers属性
        >>> {'Content-Length': '238', ...}  # 有效节省网络带宽
        response.text  # text属性
        >>>  # 为空

        # post()方法: 向URL POST一个字典，字段编码为form（表单）
        payload = {'key1': 'value1', 'key2': 'value2'}
        response = requests.post("https://httpbin.org/post", data = payload)
        print(response.text)
        >>> {...}

        # put()方法: 与post()方法类似，重点是将原有的数据覆盖掉
        payload = {'key1': 'value1', 'key2': 'value2'}
        response = requests.post("https://httpbin.org/put", data = payload)
        print(response.text)
        >>> {...}

Requests方法解析:
    requests.request(method, url, **kwargs)
        method: 请求方式， 对应get/post/put/patch等, 对应的方法是基于requests.request()方法实现的
            response = requests.request('GET', url, **kwargs)
            response = requests.request('HEAD', url, **kwargs)
            response = requests.request('POST', url, **kwargs)
            response = requests.request('PUT', url, **kwargs)
            response = requests.request('PATCH', url, **kwargs)
            response = requests.request('DELETE', url, **kwargs)
            response = requests.request('OPTIONS', url, **kwargs)
        url: 拟请求页面的url链接
        **kwargs: 控制访问的参数，共13个, 均为可选项，如下
            params: 字典或字节序列，作为参数增加到URL中
                例子: 
                    kv = {'key1': 'value1', 'key2': 'value2'}
                    response = requests.request('GET', 'http://python123.io/ws', paramgs=key)
                    print(response.url)
                    >>> http://python123.io/ws?key1=value1&key2=value2
            data: 字典、字节序、或文件对象， 作为Request的内容
                例子: 
                    kv = {'key1': 'value1', 'key2': 'value2'}
                    response = requests.request('POST', 'http://python123.io/ws', data=kv)
                    body = "测试主体内容"
                    response = requests.request("POST", "http://python123.io/ws", data=body)
                    # 这样不会放在URL中，而是放在URL对应的data域中，被封装一起post

            json: JSON格式的数据，作为Request的内容
                例子: 
                    kv = {'key1': 'value1', 'key2': 'value2'}
                    kv = {'key1': 'value1', 'key2': 'value2'}
                    response = requests.request("POST", "http://python123.io/ws", json=kv)
                    # 这样不会放在URL中，而是放在URL对应的json域中，被封装一起post

            headers: 字典， HTTP定制头: 定义了向某个URL发起请求时，所定义的http头字段
                例子:
                    hd = {'user-agent': 'Chrome/10'}
                    response = requests.request("POST", "http://python123.io/ws", headers=hd)
            
            cookies: 字典或者CookieJar, Request中的cookie
            auth: 元组， 支持HTTP认证功能
            files: 字典类型， 传输文件
                例子:
                    fs = {'file': open('data.xls', 'rb')}
                    response = requests.request('POST', 'http://python.io/ws', files=fs)
            timeout: 设定超时时间，秒为单位
            proxies: 字典类型，设定访问代理服务器，可以增加登录认证, 增加爬虫的代理, 有效防止爬虫逆向追踪
                例子:
                    pxs = {
                        'http': 'http://user:pass@10.10.10.1:1234",
                        'https': 'https://10.10.10.1:4321"
                    }
                    response = requests.request('GET', 'http://www.baidu.com', proxies=pxs)
            allow_redirects: True/False，默认为True, 是否允许重定向的开关
            stream: True/False, 默认为True, 获取内容立即下载开关
            verify: True/False, 默认为True，认证SSL证书的开关。
            cert: 保存本地SSL证书路径



```

#### 网络爬虫的"盗亦有道"
```
网络爬虫的限制:
1. 来源审查: 判断User-Agent进行限制
     检测来访的http协议头的User-Agent域,只响应浏览器或者友好的爬虫

2. 发布公告: Robots协议
    告知所有爬虫可以爬取哪些信息, 爬取策略, 要求爬虫遵守,爬虫是否遵守由爬虫开发人员决定

3. Robots协议
    Robots Exclusion Standard 网络爬虫排除标准
    作用: 网站告知爬虫哪些页面可以抓取,哪些页面不可抓取
    使用方法: 在网站的根目录下的robots.txt文件中写明: 哪些目录可爬取,哪些不可以爬取
        User-agent: *
        Allow: *
        Disallow: /simright/admin
        Sitemap: https://www.simright.com/sitemap.xml 

    网络爬虫: 自动或者人工识别robots.txt, 再进行内容爬取
    约束性: Robots协议是建议性的但非约束性, 网络爬虫可以不遵守,但是有法律风险
```

#### Requests库网络爬虫实战(5个实例)
1. 京东商品页面的爬取
```
import requests

url = "https://item.jd.com/5038791.html"
try:
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    print(response.text)
except Exception as err:
    print("爬取失败: {0}".format(err)
```

2. 亚马逊商品页面的爬取
```
import requests

url = "https://www.amazon.cn/dp/B014KB5HI4/ref=cngwdyfloorv2_recs_0/460-7844996-3437002"
try:
    kv = {'user-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=kv)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    print(response.text)
except Exception as err:
    print("爬取失败: {0}".format(err))
# response.request.headers  -> 可检测发送的get请求的header部分信息
# response.status_code -> 可检测get请求的response的状态码
```

3. 百度/360搜索引擎关键词提交
```
1. 百度的关键词接口
    https://www.baidu.com/s?wd=<keyword>
2. 360搜索关键词接口
    https://www.so.com/s?q=<keyword>

import requests

url = "https://www.baidu.com/s"  # url = "https://www.so.com/s"
keyword = 'python'
try:
    kv = {'wd': keyword}  # kv = {'q': keyword}
    r = requests.get(url, params=kv)
    print("url: {0}".format(r.request.url))
    r.raise_for_status()
    print(len(r.text))
```

4. 爬取并自动保存图片
```
import os
import requests

url = "http://image.nationalgeographic.com.cn/2017/1116/20171116110105262.jpg"
root = "/home/timilong/spider/img/"
path = root + url.split('/')[-1]
try:
    if not os.path.exists(root)
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(url)
        r.raise_for_status()
        with open(path, 'wb') as f:
            f.write(r.content)
        print('保存成功: {url}'.format(url=url))
    else:
        print('文件已存在')
except Exception as err:
    print('爬取失败: {err}'.format(err))
```

5. ip地址归属地址的自动查询
```
import requests

ip = '202.204.80.12'
url = 'http://www.ip138.com/ip.asp'
try:
    kv = {'ip': ip}
    r = requests.get(url, params=kv)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text[-500:])
except Exception as err:
    print('获取ip地理位置失败: {err}'.format(err))
```

#### 第1周测验: 
见icourse163-org-Python网络爬虫与信息提取-测验1.md


### 第2周 网络爬虫之提取
```
1. 课程导学
2. Beautiful Soup库
3. 信息组织与提取方法
4. 实例1: 中国大学排名的爬虫
5. 第2周测验: icourse163-org-Python网络爬虫与信息提取-测验2.md
```

#### Beautiful Soup库
```
1. 安装: pip install beautifulsoup4
2. 导入: from bs4 import BeautifulSoup
3. 测试:
    import requests
    from bs3 import BeautifulSoup

    url = "http://www.python123.io/ws/demo.html"
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        demo = r.text
        soup = BeautifuSoup(demo, 'html.parser')
        print(soup.prettify())
    except Exception as err:
        print("出错: {0}".format(err))

4. 基本元素:
    4.1 标签树
    4.2 解析器
        解析器                  使用方法                                  安装库
        bs4的html解析器         BeautifulSoup(demo, 'html.parser')        pip install beautifulsoup
        lxml的html解析器        BeautifulSoup(demo, 'lxml')               pip install lxml
        lxml的xml解析器         BeautifulSoup(demo, 'xml')                pip install lxml
        html5lib的解析器        BeautifulSoup(demo, 'html5lib')           pip install html5lib
    4.3 基本元素
        基本元素            使用说明
        Tag                 标签,最基本的组织单元,分别用<>和</>开头和结尾: soup.<tag>
        Name                标签的名字,<p>...</p>的名字是'p',格式: <tag>.name
        Attributes          标签的属性,字典形式组织,格式: <tag>.attrs
        NavigableString     标签内非属性字符串, <>和</>中的字符串,格式<tag>.string
        Comment             标签内字符串注释部分, 一种特殊的Comment类型

5. 基于bs4库的html内容的遍历方法
    5.1 下行遍历
        属性                     说明
        soup.<tag>.contents      子节点的列表,将tag的所有子节点的存入列表
        soup.<tag>.children      子节点的迭代类型,与.contents类似,用于循环遍历儿子节点
        soup.<tag>.descendants   子孙节点的遍历类型,包括所有子孙节点,用于循环遍历
    5.2 上行遍历
        属性                     说明
        soup.<tag>.parent        节点的父亲标签  
        soup.<tag>.parents       节点的所有先辈标签的迭代类型,用于循环遍历祖先节点
    5.4 平行遍历
        属性                               说明
        soup.<tag>.next_siblings           返回按照HTML文本顺序的下一个平行节点标签
        soup.<tag>.previous_sibling        返回按照html文本顺序的上一个平行节点标签
        soup.<tag>.next_siblings           迭代类型, 返回按照HTML文本顺序的后续所有平行节点标签
        soup.<tag>.previous_siblings       迭代类型, 返回按照HTML文本顺序的前续所有平行节点标签

        条件: 所有的平行遍历发生在同一个父亲节点下的各平行节点间

6. html格式化输出
    soup.a.pretify()
```

#### 信息组织与提取方法
```
1. XML, JSON, YAML
    XML: Internet上的信息交互与传递 -> html
    JSON: 移动应用云端和节点的信息通信,无注释,常用于后端接口定义,可直接作为js的一部分
    YAML: 各类系统的配置文件,有注释且易读

2. 信息提取一般方法
    2.1 标签树解决整个文档
    2.2 直接检索
    2.3 融合
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(demo, 'html.parser')
    for link in soup.find_all('a'):
        print(link.get('href'))

3. 基于bs4的html内容查找方法
    import requests
    from bs4 import BeautifulSoup

    r = requests.get('http://python123.io/ws/demo.html')
    r.encoding = r.apparent_encoding
    demo = t.text
    soup = BeautifulSoup(demo, 'html.parser')

    soup.find_all(name, attrs, recursive, string, **kwargs)
    返回一个列表类型, 存储查找的结果
    name: 对标签名称的检索字符串 
        soup.find_all('a')
        soup.find_all(['a', 'b'])
        soup.find_all(True)
        soup.find_all(re.compile('b'))
    attrs: 对标签属性值的检索字符串
        soup.find_all('p', 'course')
        soup.find_all(id='link1')
        soup.find_all(id=re.compile('link'))
    recursive: 是否对子孙全部检索, 默认为True
        soup.find_all('a') -> [...]
        soup.find_all('a', recursive=False) -> []
    string: <>...</>中字符串区域中检索字符串
        soup.find_all(string=re.compile('python'))
    **kwargs: 对标签名称的检索字符串

    简写:
        <tag>(...)  <==> <tag>.find_all(...)
        soup(...)   <==> soup.find_all(...)

4. bs4的扩展方法
    方法                              说明
    <>.find_all()                     全局检索
    <>.find()                         搜索且只返回一个结果,<string>类型  
    <>.find_parents()                 在先辈节点中搜索,<list>类型
    <>.find_parent()                  在先辈节点中搜索,返回一个结果,<string>类型
    <>.find_next_siblings()           在后续平行节点中搜索,<list>类型
    <>.find_next_sibling()            在后续平行节点中搜索,返回一个结果,<string>类型
    <>.find_previous_siblings()       在前续平行节点中搜索,<list>类型
    <>.find_previous_sibling()        在前续平行节点中搜索,返回一个结果,<string>类型

```

#### 实战: 中国大学排名
``` CrawUnivRankingB.py
import requests
import bs4
from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string])


def printUnivList(ulist, num):
    tplt = "{0:^10}\t{1:{4}^10}\t{2:^10}\t{3:^10}"
    print(tplt.format("排名", "学校名称", "地区", "总分", chr(12288)))
    for i in range(num):
        u=ulist[i]
        print(tplt.format(u[0], u[1], u[2], u[3], chr(12288)))


def main():
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, 20) # 20 univs
main()
```

### 第3周 网络爬虫之实战
```
1. 课程导学
2. Re(正则表达式)库入门
3. 实例2: 淘宝商品比较定向爬虫
4. 实例3: 股票数据定向爬虫
5. 课程综合测验: 网络爬虫与信息提取(客观题)
```

#### 正则表达式入门

```
.                        表示任何单个字符
[]                       字符集,对
```

