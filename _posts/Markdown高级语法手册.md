title: Markdown高级语法手册
date: 2015-11-30 22:05:29
categories: Markdown
tags: Markdown
description: Markdown 是一种轻量级标记语言，让写作者专注于写作而不用关注样式。Coding 的许多版块均采用了 Markdown 语法，比如冒泡、讨论、Pull Request 等。
cover_img: http://qiniucdn.timilong.com/1543736885620.jpg


---

### 1. 内容目录

在段落中填写 `[toc]` 以显示全文的目录结构

[TOC]

### 2. 标签分类

在编辑区的任意行的列首位置输入以下代码给文稿标签：

标签: 数学 英语 Markdown

或者

Tags: 数学 英语 Markdown

以上是摘要
<!--more-->
以下是余下全文

### 3. 删除线
使用 ~~ 表示删除线

~~这是一段错误的文本~~

### 4. 注脚

使用 [^keyword] 表示注脚。

这是一个注脚[^footnote]的样例。

这是第二个注脚[^footnote2]的样例。


### 5. LaTeX 公式


$ 表示行内公式：

质能守恒方程可以用一个很简洁的方程式 $E=mc^2$来表达。

$$ 表示整行公式：

$$\sum_{i=1}^n a_i=0$$

$$f(x_1,x_x,\ldots,x_n) = x_1^2 + x_2^2 + \cdots + x_n^2 $$

$$\sum^{j-i}_{k=0}{\widehat{\gamma}_{kj} z_k}$$

访问[MathJax](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)参考更多使用方法。

### 6. 加强代码块

支持41种编程语言的语法高亮的显示，行号显示。

非代码示例：

```
$ sudo apt-get install vim-gnome
```

Python示例：

```python
@requires_authorization
def somefunc(param1='', param2=0):
    '''A docstring'''
    if param1 >param2: # intesting
        print 'Greater'
    return (param2 - param1 + 1) or None
    
class SomeClass:
    pass
    
>>> message = '''interpreter
... prompt'''
```

JavaScript示例：

``` javascript
/**
* nth element in the fibonaxxi series.
* @param n >= 0
* @return the nth element, >= 0.
*/
function fib(n) {
    var a = 1, b = 1;
    var tmp;
    while (--n >= 0) {
        tmp = a;
        a += b;
        b = tmp;
    }
    return a;
}

document.write(fib(10));
```

### 7. 流程图

#### 示例

```flow
st=>start: Start: Start:>https://www.longyun.club
io=>inputoutput: verification
op=>operation: Your Operation
cond=>condition: Yes or No?
sub=>subroutine: Your Subroutine
e=>end

st->io->op->cond
cond(yes)->e
cond(no)->sub->io
```

#### 更多语法参考： [流程图语法参考](http://adrai.github.io/flowchart.js/)

### 8. 序列图

#### 示例 1

```seq
Alice-Bob: Hello Bob, how are you?
Note right of Bob: Bob thinks
Bob-->Alice: I am good thinks!
```

#### 示例2

```seq
Title: 时序图
A->B: Normal line
B-->C: Dashed line
C->>D: Open arrow
D-->>A: Dashed open arrow
```

#### 更多语法参考： [序列图语法参考](http://bramp.github.io/js-sequence-diagrams/)

### 9. 表格支持

| 项目        | 价格   |  数量  |
| :--------:   | :-----:  | :----:  |
| 计算机     | $1600 |   5     |
| 手机        |   $12   |   12   |
| 管线        |    $1    |  234  |

### 10. 定义型列表

名词 1
:    定义 1（左侧有一个课件的冒号和四个不可见的空格）

代码块 2
:    这是代码块的定义（左侧有一个可见的冒号和四个不可见的空格)

        代码块（左侧有八个不可见的的空格）
        
### 11. Html标签

本站支持在Markdown语法中嵌套Html
标签， 譬如， 你可以用Html写一个纵跨两行的表格：
   
    <table>
        <tr>
            <th rowspan="2">值班人员</th>
            <th>星期一</th>
            <th>星期二</th>
            <th>星期三</th>
        </tr>
        <tr>
            <td>李强</td>
            <td>张明</td>
            <td>王平</td>
        </tr>
    </table>
    
<table>
    <tr>
        <th rowspan="2">值班人员</th>
        <th>星期一</th>
        <th>星期二</th>
        <th>星期三</th>
    </tr>
    <tr>
        <td>李强</td>
        <td>张明</td>
        <td>王平</td>
    </tr>
</table>

### 12. 内嵌图标

本站的图标系统对外开放， 在文档中输入

    <i class="icon-weibo"></i>

即显示微博的图标： <i  class="icon-weibo icon-5x"></i>

替换 上述 `i 标签` 内的 `icon-weibo`

以显示不同的图标， 例如:

    <i  class="icon-renren"></i>

即显示人人的图标: <i class="icon-renren icon-5x"></i>

更多图标和玩法可以参看[font-awesome](http://fortawesome.github.io/Font-Awesome/3.2.1/icons/) 官方网站。

### 13. 待办事宜Todo列表

使用带有 [] 或者 [x] 未完成或已完成）项目的列表语法撰写一个待办事宜列表，并且支持子列表嵌套以及混用Markdown语法, 例如：

    - [ ] **Cmd Markdown 开发**
        - [ ] 改进 Cmd 渲染算法，使用局部渲染技术提高渲染效率
        - [ ] 支持以 PDF 格式导出文稿
        - [x] 新增Todo列表功能 [语法参考](https://github.com/blog/1375-task-lists-in-gfm-issues-pulls-comments)
        - [x] 改进 LaTex 功能
            - [x] 修复 LaTex 公式渲染问题
            - [x] 新增 LaTex 公式编号功能 [语法参考](http://docs.mathjax.org/en/latest/tex.html#tex-eq-numbers)
    - [ ] **七月旅行准备**
        - [ ] 准备邮轮上需要携带的物品
        - [ ] 浏览日本免税店的物品
        - [x] 购买蓝宝石公主号七月一日的船票
        
对应显示如下待办事宜 Todo 列表：
        
- [ ] **Cmd Markdown 开发**
    - [ ] 改进 Cmd 渲染算法，使用局部渲染技术提高渲染效率
    - [ ] 支持以 PDF 格式导出文稿
    - [x] 新增Todo列表功能 [语法参考](https://github.com/blog/1375-task-lists-in-gfm-issues-pulls-comments)
    - [x] 改进 LaTex 功能
        - [x] 修复 LaTex 公式渲染问题
        - [x] 新增 LaTex 公式编号功能 [语法参考](http://docs.mathjax.org/en/latest/tex.html#tex-eq-numbers)
- [ ] **七月旅行准备**
    - [ ] 准备邮轮上需要携带的物品
    - [ ] 浏览日本免税店的物品
    - [x] 购买蓝宝石公主号七月一日的船票
        


     


