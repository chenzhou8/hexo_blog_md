title: eisoo前端面试题
date: 2016-03-21 22:13:23
tags: 前端
categories: 面试
description: 爱数-提供智能数据管理的云计算公司, www.eisoo.com
cover_img: http://qiniucdn.timilong.com/1543736777461.jpg
---

#### 公司简介
[爱数-提供智能数据管理的云计算公司](www.eisoo.com)

#### CSS中的position常见的几种属性:

```
absolute: 生成绝对定位的元素， 相对于static定位以外的第一个父元素进行定位。
          元素的位置通过"left", "top", "right", "bottom"属性进行规定。

fixed: 生成绝对定位的元素， 相对于浏览器窗口进行定位。
       元素的位置通过"left", "top", "right", "bottom"属性进行规定

relative: 生成相对定位的元素， 相对于其正常的位置进行定位。
          因此，"left: 20px" 会向left位置添加20像素。

static: 默认值， 没有定位， 元素出现在正常的流中(忽略top, bottom, left, right, z-index声明)
      
inherit: 规定应该从父元素继承position属性的值。
```

#### JavaScript的基本数据类型

```
JavaScript中有5种简单的数据类型(也称基本数据类型): 
    Undefined, 
    Null, 
    Boolean, 
    Number, 
    String.
还有一种复杂的数据类型——Object,Object本质上是由一组无序的名值对组成的。
```

#### JavaScipt执行"2014"+1的结果是?

```
"2014"+1 = "20141"
```

#### 最常见的网站解决方案LAMP是由:

```
L: Linux.
A: Apache.
M: MySQL.
P: Python.
```

#### 常用的HTTP状态码示请求需要用户验证？
[HTTP状态码](http://baike.baidu.com/link?url=mvyZuhYfWvdY_dTdpnDmYU-9TucSxqrCTZJKBM8Uv1H7g_tlGHR9CXMiuSv8ig-CAuoxi_mu_Ckm7aCbP6ELI_)

```
401: 当前请求需要用户验证。
该响应必须包含一个适用于被请求资源的 WWW-Authenticate 信息头用以询问用户信息。
客户端可以重复提交一个包含恰当的 Authorization 头信息的请求。
如果当前请求已经包含了 Authorization 证书，那么401响应代表着服务器验证已经拒绝了那些证书。
如果401响应包含了与前一个响应相同的身份验证询问，且浏览器已经至少尝试了一次验证，
那么浏览器应当向用户展示响应中包含的实体信息，因为这个实体信息中可能包含了相关诊断信息。
```

#### 编程题: 使用JavaScript实时显示当前时间，格式"年-月-日 时:分:秒"

```
<!DOCTYPE HTML>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
<script language="javascript">
function showtime()
{
    var today,hour,second,minute,year,month,date;
    var strDate ;
    today=new Date();
    var n_day = today.getDay();
    switch (n_day)
    {
      case 0:{
        strDate = "星期日"
      }break;
      case 1:{
        strDate = "星期一"
      }break;
      case 2:{
        strDate ="星期二"
      }break;
      case 3:{
        strDate = "星期三"
      }break;
      case 4:{
        strDate = "星期四"
      }break;
      case 5:{
        strDate = "星期五"
      }break;
      case 6:{
        strDate = "星期六"
      }break;
      case 7:{
        strDate = "星期日"
      }break;
    }
    year = today.getYear();
    month = today.getMonth()+1;
    date = today.getDate();
    hour = today.getHours();
    minute =today.getMinutes();
    second = today.getSeconds();
    document.getElementById('time').innerHTML = (year+1900) + "年" + month + "月" + date + "日" +"   " + strDate +"   " + hour + ":" + minute + ":" + second; //显示时间
    setTimeout("showtime();", 1000); //设定函数自动执行时间为 1000 ms(1 s)
}
</script>

<span id="time"></span>
<script language="javascript"> showtime();</script>

</body>
</html>
```

#### 编程题: 使用Python、JavaScript、PHP中的两种语言完成Fibnacci数列的编写。
Python方法1：

```python
fib = lambda n, x=0, y=1 : x if not n else f(n-1, y, x+y)
```

Python方法2：

```python
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
    return 'done'
```

JavaScript方法:

```javascript
function fibn(n){
  if(n<=2){
      return 1;
  }else{
      return f(n-1)+f(n-2);
  }
  alert(f(13));
```
