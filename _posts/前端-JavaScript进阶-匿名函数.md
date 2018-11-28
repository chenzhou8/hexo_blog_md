title: JavaScript进阶-匿名函数
date: 2016-04-10 15:25:09
categories: 前端
tags: JavaScript
cover_img:
description: 本文介绍JavaScript中的匿名函数用法。

---

### 1.函数传递

```javascript
function say(word){
    console.log(word);
}

function execute(someFunction, value){
    someFunction(value);
}

execute(say, "Hello, World");
```

在这段代码中， 我们把say函数作为execute函数的第一个变量进行了传递。
这里返回的并不是say的返回值，而是say的本身！
这样，say就变成了execute中的本地变量someFunction,execute可以通过调用someFunction()(带括号的形式)
来使用say函数。
当然， 因为say有一个变量， execute在调用someFunction时候可以传递这样一个变量。

### 2. 匿名函数

另外，我们可以用直接传递函数作为变量传递。我们不一定要围绕着“先定义，再传递”这个圈子。
我们可以直接在另一个含糊的括号中是定义和传递这个函数

```javascript
function execute(someFunction, value){
    someFunction(value);
}

execute(function(word){console(word)}, "Hello, World");
```

我们在execute接受第一个参数的地方直接定义了我们准备传递给execute的函数。
用这种方式， 我们甚至不用给这个函数起一个函数名字， 这就是叫做匿名函数的原因。

在JavaScript中, 一个函数可以作为另一个函数接收的一个参数。
可以先定义一个函数，然后传递函数名， 也可以在传递参数的地方直接定义函数。
