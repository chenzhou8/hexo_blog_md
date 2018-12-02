title: html中将非a标签变成超链接
date: 2016-05-28 01:11:34
categories: 前端
tags: 前端
cover_img: http://qiniucdn.timilong.com/1543735509225.jpg
description: Html中将非a标签变成超链接.

---

  在《计算机网络》课程项目：搭建一个web邮件服务器中，遇到了要将收件箱中的``<tr>``标签
变成一个整体可点击的链接标签，尝试过用``<a>``标签包含``<tr>``标签的做法，无果。
  仔细琢磨，结合onclick属性，得出如下方法:

```html
<!DOCTYPE html>
  <head>
    <title>test</title>
    <style type="text/css">
      td{
          width: 100px;
          height: 50px;
          border: 1px solid black;
          text-align: center;
      }
      tr:hover{
          background-color: gray;
          cursor: pointer;
      }
    </style>
  </head>
  <body>
    <table>
      <tr onclick="parent.location='https://www.zhihu.com';">
        <td>1</td>
        <td>2</td>
        <td>3</td>
        <td>4</td>
      </tr>
    </table>
  </body>
</html>
```
