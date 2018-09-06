title: 初探Ajax
date: 2016-04-16 12:01:27
categories: 前端
tags: Ajax

---

### 1.介绍
AJAX = Asynchronous JavaScript and XML(异步的JavaScript和XML)

AJAX不是新的编程语言，而是一种使用现有标准的新方法。

AJAX是在不重新加载整个页面的情况下，与服务器交换数据并更新部分网页的艺术。

<!--more-->

### 2.AJAX实例

```javascript
<html>
<head>
<script type="text/javascript">
function loadXMLDoc(){
    ...Ajax script goes here...
}
<script>
</head>
<body>
<div id="myDiv">
  <h3>Let Ajax change this text</h3>
</div>
<button type="button" onclick="loadXMLDoc()">change text</button>
</body>
</html>
```

### 3.创建XMLHttpRequest对象

---
XMLHttpRequest是AJAX的基础
---

#### XMLHttpRequest对象
所有现代浏览器均支持XMLHttpRequest对象(IE5\6 使用AxtiveXObject)
XMLHttpRequest用于在后台与服务器交换数据。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。

#### 创建XMLHttpRequest对象

    variable = new XMLHttpRequest();

#### IE5/6使用ActiveX对象:
    variable = new ActiveObject("Microsoft.XMLHTTP");

为了应对所有的县南丹浏览器，包括IE5/6， 请检查浏览器是否支持XMLHttpRequest对象。如果支持，则创建XMLHttpRequest对象。如果不支持，则创建ActiveXObject:

```javascript
var xmlhttp;
if(window.XMLHttpRequest){
    xmlhttp = new XMLHttpRequest();
}else{
    xmlhttp = new ActiveXObject("Microsoft.XMLHttp");
}
```

### 4.向服务器发送请求
XMLHttpRequest对象用于和服务器交换数据。

---

#### 向服务器发送请求
如需将请求发送到服务器，使用XMLHttpRequest对象的open()和send()方法:

```javascript
xml.http.open("GET", "test1.txt", true);
xmlhttp.send();
```

open(method, url, async)方法:
规定请求的类型，URL以及是否异步处理请求。
method: 请求的类型——GET或者POST
url: 文件在服务器上的位置
async: true(异步)或者false(同步)

send(string)方法:
将请求发送到服务器。
string:仅用于POST请求。

#### GET还是POST?
与POST相比，GET更简单也更快，并且在大部分情况下都能使用。
然而，在以下情况中，请求使用POST:
1. 无法使用缓存文件你(更新服务器上的文件或者数据库)
2. 向服务器发送大量的数据(POST没用数据量的限制)
3. 发送包含位置字符的用户输入时候， POST比GET更稳定也更可靠。

#### GET请求

一个简单的GET请求:
```javascript
<!DOCTYPE html>
<html>
<head>
<title>测试GET方法</title>
<script>
function loadXMLDoc(){
    var xmlhttp;
    if(window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }else{
        xmlhttp = new ActiveXObject("Microsoft.XMLHttp");
    }
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
            document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "/ajax/demo_get.asp", true);
    xmlhttp.send();
}
</script>
</head>
<body>
<h2>AJAX</h2>
<div id="myDiv">
</div>
<button type="button" onclick="loadXMLDoc()">GET方法获取服务器值</button>
</body>
</html>
```

在上面的例子中， 可能得到是缓存的结果，为了避免这种情况，在URL中添加一个唯一的ID:
```javascript
xmlhttp.open("GET", "demo_get.asp?t=" +Math.random(), true);
xmlhttp.send();
```

如果希望通过get方法发送信息， 请向URL添加信息:

```javascript
<!DOCTYPE html>
<html>
<head>
<title>通过GET方法发送信息</title>
<script type="text/javascript">
function loadXMLDoc(){
    var xmlhttp;
    if(window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }else{
        xmlhttp = new ActiveXObject("Microsoft.XMLHttp");
    }
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.State == 4 && xmlhttp.status == 200){
            document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "/ajax/demo_get2.asp?fname=Bill&lname=Gates", true);
    xmlhttp.send();
}
</script>
</head>
<body>
<h2>AJAX</h2>
<button type="button" onclick="loadXMLDoc()">请求数据</button>
<div id="myDiv">
</div>
</body>
</html>
```

#### POST请求

一个就暗淡的POST请求:
```javascript
<!DOCTYPE html>
<html>
<head>
<title>简单的POST请求</title>
<script>
function loadXMLDoc(){
    var xmlhttp;
    if(window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }else{
        xmlhttp = new XMLHttpRequest();
    }
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.State == 4 && xmlhttp.status == 200){
            document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("POST", "/ajax/demo_post.asp", true);
    xmlhttp.send();
}
</script>
</head>
<body>
<h2>AJAX POST</h2>
<button type = "button" onclick="loadXMLDoc()">POST请求服务器数据</button>
<div id="myDiv"></div>
</body>
</html>
```
如果要像HTML表单那样POST数据，使用setRequestHeader()来添加HTTP头。然后在send()方法中规定希望发送的数据:

```javascript
xmlhttp.open("POST", "ajax_test.asp", true);
xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xmlhttp.send("fname=Bill&lname=Gates");
```

setRequestHeader(header, value):
    向请求添加http头:
    header: 规定头的名称
    value: 规定头的值

#### url-服务器上的文件位置
open()方法的url参数是服务器上的文件的位置:
        xmlhttp.open("GET", "ajax_test.asp", true);
该文件可以是任何类型的文件，.txt/.xml/服务器脚本/.asp/.php(在传回响应前能够在服务器上执行任务)

#### 异步-True或者False?
AJAX指的是异步JavaScript和XML。
XMLHttpRequest对象如果要用于AJAX的话，其open()方法的asynnc参数必须设置为true：
        xmlhttp.open("GET", "ajax_test.asp", true);
对于web开发人员来说，发送异步请求是一个巨大的进步。
很多在服务器上执行的任务都相当费时。通过AJAX，JavaScript无需等待服务器的响应，而是:
    *在等待服务器响应时候执行其他脚本
    *当响应就绪后对响应进行处理

#### Async = true
当使用async = true时候，， 请规定在响应处于onreadystatechange事件中的就绪状态执行的函数:
```javascript
      xmlhttp.onreadystatechange = function(){
          if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
              document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
          }
          xmlhttp.open("GET", "test1.txt", true);
          xmlhttp.send();
      }
```

#### Async = False
如需使用async = false, 将open()方法中的第三个参数改为false:
    xmlhttp.open("GET", "test1.txt", false);
不推荐使用async = false.

JavaScript会等到服务器响应就绪才继续执行。如果服务器繁忙或缓慢，应用程序会挂起或停止。

注释: 在使用async = false时候，不要编写onreadystatechange函数-把代码放到send()语句后面执行:
```javascript
xmlhttp.open("GET", "test1.txt", false);
xmlhttp.send();
document.getElementById("myId").innerHTML = xmlhttp.responseText;
```

### 5.服务器响应

#### 服务器响应
如需获得来自服务器的响应, 请使用XMLHttpRequest对象的responseText或者responseXML属性。
*responseText: 获得字符串形式的响应数据。
*responseXML: 获得XML形式的响应数据。

#### responseText属性
如果来自服务器的响应并非XML, 请使用responseText属性。
responseText属性返回字符串形式的响应，可以向下面这样使用:
document.getElementById("myDiv").innerHTML = xmlhttp.responseText;

#### responseXML属性
如果来自服务的响应是XML， 而且需要作为XML对象进行解析， 请使用responseXML属性:
一个例子:

```javascript
<html>
<head>
<title>请求一个xml格式的数据表</title>
<script type="text/javascript">
function loadXMLDoc(){
    var txt, i, x;
    if(window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }else{
        xmlhttp = new ActiveXObject("Microsoft.XMLHttp");
    }
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
            xmlDOC = xmlhttp.responseXML;
            txt = "";
            x = xmlDoc.getElementsByTagname("title");
            for("i=0; i<x.length; i++){
                txt = txt + x[i].childNodes[0].nodeValue + "<br />";
            }
            document.getElementById("myDiv").innerHTML = txt;
        }
    }
</script>
</head>
<body>
<h2>我的书单列表</h2>
<div id="myDiv"></div>
<button type="button" onclick="loadXMLDoc()">获取我的书单列表</button>
</body>
</html>
```

### 6.readyState

#### onreadystatechange事件
当请求被发送到服务器时候，需要执行一些响应的任务。
每当readyState改变时候， 就会触发onreadystatechange事件。
每当readyState属性存有XMLHttpRequest的状态信息。
关于XMLHttpRequest的三个重要的属性:
    *onreadystatechange: 存储函数(或者函数名), 每当readyState属性改变时候，就会调用该函数。
    *readyState: 存有XMLHttpRequest的状态。从0到4发生变化。
                *0: 请求未被初始化
                *1: 服务器连接已建立
                *2: 请求已接收
                *3: 请求处理中
                *4: 请求已完成，响应已就绪
    *status: 200: "OK"
             400: "未找到页面"
在onreadystatechange事件中，规定当服务器响应已做好被处理的准备时所执行的人物。
当xmlhttp.readyState等于4且xmlhttp.status等于200时候，表示响应已就绪。
```javascript
xmlhttp.onreadystatechange = function(){
    if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
        document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
    }
}
```

onreadystatechange事件被触发5次(0-4),对应着readyState的每个变化。

#### 使用Callback函数
callback函数是一种以参数形式传递给另一个函数的函数。
如果网站上存在多个AJAX任务, 则应该为创建XMLHttpRequest对象编写一个标准的函数，并为每个AJAX任务调用该函数。
该函数调用应该包含URL以及发生onreadystatechange事件时执行的任务(每次调用可能不尽相同):

```javascript
    var xmlhttp;
    function loadXMLDoc(url, cfunc){
        if(window.XMLHttpRequest){
            xmlhttp = new XMLHttpRequest();
        }else{
            xmlhttp = new ActiveXObject("Microsoft.XMLHttp");
        }
        xmlhttp.onreadystatechange = cfunc;
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
    }
    function myFunction(){
        loadXMLDoc("/ajax/test1.txt", function(){
            if(xmlhttp.readyState == 4 && xmlhttp.status == 300){
                document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
            }
        });
    }
</script>
</head>
<body>
<div id="myDiv"><h2>Let ajax change this text.</h2></div>
<button type="button" onclick="myFunction()">通过ajax来改变内容</button>
</body>
</html>
```

### 7.ASP/PHP请求实例

#### ajax用于创造动态性更强的应用程序
实例:

```javascript
<!DOCTYPE html>
<html>
<head>
<title>ajax的asp/php实例</title>
<script type="text/javascript">
function showHint(str){
    var xmlhttp;
    if(str.length == 0){
        document.getElementById("txtHint").innerHTML = "";
        return;
    }
    if(window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }else{
        xmlhttp = new ActiveXObject("Microsoft.XMLHttp");
    }
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
            document.getElementById("txtHint").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "/ajax/gethint.asp?q="+str, true);
    xmlhttp.send();
}
</script>
</head>
<body>
<h3>请在下面的输入框中键入字母(A-Z):</h3>
<form action="">
姓氏: <input type="text" id="txt1" onkeyup="showHint(this.value)" />
</form>
<p>建议: <span id="txtHint"></span></p>
</body>
</html>
```
    
源码解释:
如果输入框为空(str.length == 0)， 则该函数清空txtHint占位符的内容, 并退出函数。
如果输入框不为空， showHint()函数执行以下任务:
  *创建XMLHttpRequest对象
  *当服务器响应就绪时候执行函数
  *把请求发送到服务器上的文件
  *向URL添加一个参数q(传递输入框的内容)
---

#### AJAX服务器页面-ASP和PHP
由上面的Javascript调用服务器页面是ASP文件，名为"gethint.asp"。

#### ASP文件
"gethint.asp"中的源代码会检查一个名字数组， 然后向浏览器返回相应的名字:

```php
<%
response.expires=-1
dim a(30)
    '用名字来填充数组
    a(1)="Anna"
    a(2)="Brittany"
    a(3)="Cinderella"
    a(4)="Diana"
    a(5)="Eva"
    a(6)="Fiona"
    a(7)="Gunda"
    a(8)="Hege"
    a(9)="Inga"
    a(10)="Johanna"
    a(11)="Kitty"
    a(12)="Linda"
    a(13)="Nina"
    a(14)="Ophelia"
    a(15)="Petunia"
    a(16)="Amanda"
    a(17)="Raquel"
    a(18)="Cindy"
    a(19)="Doris"
    a(20)="Eve"
    a(21)="Evita"
    a(22)="Sunniva"
    a(23)="Tove"
    a(24)="Unni"
    a(25)="Violet"
    a(26)="Liza"
    a(27)="Elizabeth"
    a(28)="Ellen"
    a(29)="Wenche"
    a(30)="Vicky"

    '获得来自 URL 的 q 参数
    q=ucase(request.querystring("q"))

    '如果 q 大于 0，则查找数组中的所有提示
    if len(q)>0 then
      hint=""
        for i=1 to 30
          if q=ucase(mid(a(i),1,len(q))) then
            if hint="" then
              hint=a(i)
            else
              hint=hint & " , " & a(i)
            end if
          end if
        next
      end if

'如果未找到提示，则输出 "no suggestion"
'否则输出正确的值
if hint="" then
  response.write("no suggestion")
else
  response.write(hint)
end if
%>
```

PHP代码略...

### 8.数据库实例

#### AJAX可用来与数据库进行动态通信。
下面的例子将演示网页如何通过AJAX从数据库读取信息:

```html
<html>
<head>
<script type="text/javascript">
function showCustomer(str)
{
    var xmlhttp;    
    if (str=="")
    {
        document.getElementById("txtHint").innerHTML="";
        return;
    }
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            document.getElementById("txtHint").innerHTML=xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET","/ajax/getcustomer.asp?q="+str,true);
    xmlhttp.send();
}
</script>
</head>
<body>

<form action="" style="margin-top:15px;"> 
<label>请选择一位客户：
<select name="customers" onchange="showCustomer(this.value)" style="font-family:Verdana, Arial, Helvetica, sans-serif;">
<option value="APPLE">Apple Computer, Inc.</option>
<option value="BAIDU ">BAIDU, Inc</option>
<option value="Canon">Canon USA, Inc.</option>
<option value="Google">Google, Inc.</option>
<option value="Nokia">Nokia Corporation</option>
<option value="SONY">Sony Corporation of America</option>
</select>
</label>
</form>
<br />
<div id="txtHint">客户信息将在此处列出 ...</div>

</body>
</html>

```

源码解释:
当用户在下拉列表中选取某个客户时候，会执行名为"showCustom()"的函数， 该函数由"onchange"事件触发.
showCustomer()函数执行以下任务:
  *检查是否已选择某个用户
  *创建XMLHttpRequest对象
  *当服务器响应就绪时候，执行所创建的函数
  *把请求发送到服务器上面的文件
  *向URL添加了参数q(传递输入域中的内容)

#### AJAX服务器页面
上面的JavaScript调用的服务器页面是asp文件, 名为"getcustomer.asp"
"getcustomer.asp"中的原码负责对数据库进行查询, 然后用HTML表格返回结果:

```asp
<%
response.expires=-1
sql="SELECT * FROM CUSTOMERS WHERE CUSTOMERID="
sql=sql & "'" & request.querystring("q") & "'"

set conn=Server.CreateObject("ADODB.Connection")
conn.Provider="Microsoft.Jet.OLEDB.4.0"
conn.Open(Server.Mappath("/db/northwind.mdb"))
set rs=Server.CreateObject("ADODB.recordset")
rs.Open sql,conn

response.write("<table>")
do until rs.EOF
  for each x in rs.Fields
    response.write("<tr><td><b>" & x.name & "</b></td>")
    response.write("<td>" & x.value & "</td></tr>")
  next
  rs.MoveNext
loop
response.write("</table>")
%>
```

### 9. XML文件

#### AJAX可用来与XML文件进行交互式通信
下面的例子将演示通过AJAX来获得XML文件的信息:

```javascript
...
```

当用户点击上面的“获得 CD 信息”这个按钮，就会执行 loadXMLDoc() 函数。
loadXMLDoc() 函数创建 XMLHttpRequest 对象，添加当服务器响应就绪时执行的函数，并将请求发送到服务器。
当服务器响应就绪时，会构建一个 HTML 表格，从 XML 文件中提取节点（元素），最后使用已经填充了 XML 数据的 HTML 表格来更新 txtCDInfo 占位符：

```javascript
function loadXMLDoc(url)
{
    var xmlhttp;
    var txt,xx,x,i;
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            txt="<table border='1'><tr><th>Title</th><th>Artist</th></tr>";
            x=xmlhttp.responseXML.documentElement.getElementsByTagName("CD");
            for (i=0;i<x.length;i++)
            {
                txt=txt + "<tr>";
                xx=x[i].getElementsByTagName("TITLE");
                {
                    try
                    {
                        txt=txt + "<td>" + xx[0].firstChild.nodeValue + "</td>";
                    }
                    catch (er)
                    {
                        txt=txt + "<td> </td>";
                                                                                                                                    }
                    }
                    xx=x[i].getElementsByTagName("ARTIST");
                    {
                        try
                        {
                            txt=txt + "<td>" + xx[0].firstChild.nodeValue + "</td>";
                        }
                        catch (er)
                        {
                            txt=txt + "<td> </td>";
                        }
                    }
                    txt=txt + "</tr>";
                }
                txt=txt + "</table>";
                document.getElementById('txtCDInfo').innerHTML=txt;
            }
        }
        xmlhttp.open("GET",url,true);
        xmlhttp.send();
}
```


