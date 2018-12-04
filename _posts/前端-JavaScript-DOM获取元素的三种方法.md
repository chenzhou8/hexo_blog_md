title: JavaScript DOM获取元素的三种方法
date: 2016-02-01 18:29
categories: 前端
tags: JavaScript
description: JavaScript Dom获取元素的几种方法介绍。
cover_img: http://qiniucdn.timilong.com/1543736896543.jpg
---

![tu](http://qiniucdn.timilong.com/1543736896543.jpg)

## JavaScript DOM获取元素的三种方法
### 通过id 
DOM提供了一个名为: getElementById的方法, 这个方法将返回一个那个有着给定id属性的值的元素节点对应的对象。在这里强调: JavaScript语言严格区分字母的大小写!
它是document对象特有的函数。在脚本代码里, 函数名的后面必须跟有一对圆括号, 这对圆括号包含着函数的参数。getElementById方法只有一个参数: 想要获得的那个元素的id属性的值, 这个id值必须放在单引号或者双引号里面:

```javascript
    document.getElementById(id)
```

例子：
```html
    <!DOCTYPE html>
    <head>
      <meta charset="utf-8">
      <title>Shopping list</title>
    </head>
    <body>
      <h1>What to buy</h1>
      <p title="a gentle reminder">Don't forget to buy this stuff.</p>
      <ul id="purchases">
        <li>A tin of beanns</li>
        <li class="sale">Cheese</li>
        <li class="sale important">Milk</li>
      </ul>
      <script>
        alert(typeof document.getElementById("purchases"));
      </script>
    </body>
    </html>

```

文档中的每一个元素都是一个对象。利用DOM提供的方法能得到任何一个对象。
一般来说，用不着为文档里面每一个元素都定义一个独一无二的id值。DOM提供了另一个方法获取那些没有id属性的对象。

---

### 通过标签名字
DOM提供了一个名为：getElementsByTagName的方法。
getElementsByTagName方法返回一个对象数组，每个对象分别对应着文档里有着给定标签的一个元素。类似于getElementById。该方法只有一个参数，它的参数是标签的名字。

```
    element.getElementsByTagName(tag);
```
该方法返回的是一个数组。
例子：

```
    document.getElementsByTagName("li");
    
```
    
这个调用将返回一个对象数组, 每个对象分别对应着document对象中的一个li项元素。与其他任何数组一样，我们可以通过length属性查出这个数组的长度。

```
    <!DOCTYPE html>
    <head>
      <meta charset="utf-8">
      <title>Shopping list</title>
    </head>
    <body>
      <h1>What to buy</h1>
      <p title="a gentle reminder">Don't forget to buy this stuff.</p>
      <ul id="purchases">
        <li>A tin of beanns</li>
        <li class="sale">Cheese</li>
        <li class="sale important">Milk</li>
     </ul>
     <script>
       alert(typeof document.getElementsByTagName("li"));
     </script>
    </body>
    </html>

```
浏览器显示：3
该数组中的每个元素都是一个对象。可以通过一个循环语句和typeof操作符去遍历该数组，得到三个对象:

```
    for(var i = 0; i<document.getElementsByTagName("li").length; i++){
        alert(typeof docement.getElementsByTagName("li"));
    }
```

减少不必要的代码重复，并使代码更简洁易读：

```
    var items = document.getElementsByTagName("li");
    for(var i = 0; i<items.length; i++)
    {
        alert(typeof items[i]);
    }
```

getElementsByTagName允许把一个通配符"*"作为它的参数， 而这意味着文档里面的每个元素都将在所得到的这个数组中占有一个我位置，通配符必须放在引号里， 这样通配符就可以与乘法符号区别， 如果你想知道某分文档总共有多少元素节点：

```
    alert(document.getElementsByTagName("*").length;
```

将getElementById和getElementsByTagName结合起来。如果想知道id值为purchase的元素包含多少个列表项，必须通过一个更具体的方法去调用这个方法， 如下所示：

```
    var shopping = document.getElementById("purchases");
    var items = shopping.getElementsByTagName("*");
```

这两条语句执行完后, items数组将只包含id属性值是purchases的无序清单里的元素。

---

### 通过类名字
DOM提供getElementsByClassName的方法。
HTML5 DOM新增了getElementsByClassName的方法，能够通过class属性中的类名来访问元素。
getElementsByClassName方法只接受一个参数，就是类名：
document.getElementByClassName(class);
返回值是一个具有相同类名的数组。下面这行代码就是返回一个数组， 包含类名为"sale"的所有元素。
document.getElementsByClassName("sale");
使用这个方法还可以查找带有多个类的元素。要指定多个类名，只要在字符串参数中用空格分隔类名即可。
例如, 在`<script>`标签中添加下面alert代码：

```
alert(document.getElementsByClassName("important sale").length);
```

类名的顺序无关。
组合使用getElementById和getElementsByClassName：
在id = purchases下寻找class = sale元素标签。

```
    var shopping = document.getElementById("purchases");
    var sales = shopping.getElementsByClassName("sale");
```

该方法只有支持html5 DOM的新浏览器才支持。
所以，通过以下代码兼容老浏览器；

```
    function getElementsByClassName(node, classname){
      if(node.getElementsByClassName){
        return node.getElementsByClassName(class);
      }else{
         var results = new Array();
         var elems = node.getElementsByTagName("*");
         for(var i=0; i<elems.length; i++){
           if(elems[i].className.indexOf(classname) != -1){
             results[results.length] = elems[i];
           }
         }return results;
      }
    }
```

这个getElementsByClassName接受两个参数， 第一个node表示DOM树中的搜索起点， 第二个classname表示要搜索的类名。

<完>


