---
title: python-进阶列表和元组的内存分配机制
cover_img: http://qiniucdn.timilong.com/1551521099811.jpg
date: 2019-03-29 12:18:15
tags: python
feature_img: 
description: 关于List, Tuple的内存分配机制的源码分析.
keywords: python
categories: python
---

![cover_img](http://qiniucdn.timilong.com/1551521099811.jpg)

> 链接：https://www.jianshu.com/p/24090fb63968 

## 从内存利用和CPU利用开始了解List和Tuple的优缺点

定义
```
List：动态数组，元素可变，可改变大小（append，resize）
Tuple：静态数组，不可变，数据一旦创建后不可改变
List的内存利用
```

1. 当创建N个元素的List时，Python的动态内存分配长N＋1个元素的内存，第一个元素存储列表长度，和列表的元信息。
2. 当Append一个元素时，Python将创建一个足够大的列表，来容纳N个元素和将要被追加的元素。
3. 重新创建的列表长度大于N＋1（虽然我们只触发一次append操作），实际上，为了未来的Append操作，M个元素长度（M>N+1)的内存将会被额外分配。
4. 然后，旧列表中的数据被copy到新列表中，旧列表销毁。
5. 额外内存的分配，只会发生在第一次Append操作时，当我们创建普通列表时，不会额外分配内存。
(这里的哲学是，一个Append操作很可能是很多Append操作的开始，通过额外分配内存来减少可能的内存分配和内存copy的次数。)
那么，对于一个具有N个元素的列表，当一次Append操作发生时，新列表要分配多少内存（额外M个元素，需多分配一个元素存储长度）呢？答案是：

```
** M = (N >> 3) + (N <9 ? 3 : 6) + 1 **
```

## Python3.6.1的列表resize过程
> 源代码位于Objects/listobject.c中的list_resize函数：

```
static int
list_resize(PyListObject *self, Py_ssize_t newsize)
{
    PyObject **items;
    size_t new_allocated;
    Py_ssize_t allocated = self->allocated;

    /* Bypass realloc() when a previous overallocation is large enough
       to accommodate the newsize.  If the newsize falls lower than half
       the allocated size, then proceed with the realloc() to shrink the list.
    */
    if (allocated >= newsize && newsize >= (allocated >> 1)) {
        assert(self->ob_item != NULL || newsize == 0);
        Py_SIZE(self) = newsize;
        return 0;
    }

    /* This over-allocates proportional to the list size, making room
     * for additional growth.  The over-allocation is mild, but is
     * enough to give linear-time amortized behavior over a long
     * sequence of appends() in the presence of a poorly-performing
     * system realloc().
     * The growth pattern is:  0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...
     */
    new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6);

    /* check for integer overflow */
    if (new_allocated > SIZE_MAX - newsize) {
        PyErr_NoMemory();
        return -1;
    } else {
        new_allocated += newsize;
    }

    if (newsize == 0)
        new_allocated = 0;
    items = self->ob_item;
    if (new_allocated <= (SIZE_MAX / sizeof(PyObject *)))
        PyMem_RESIZE(items, PyObject *, new_allocated);
    else
        items = NULL;
    if (items == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    self->ob_item = items;
    Py_SIZE(self) = newsize;
    self->allocated = new_allocated;
    return 0;
}
```

结合C源码我们来举个例子，当一个list长度为8时，发生append操作后：
```
1）new_size = 原有的size ＋ append一个对象 = 8 + 1 = 9
2）newsize为9，二进制是 1001，9 >> 3 = 1
3）new_allocated = 9 >> 3 + 6 = 7
4）new_allocated += new_size，为9 + 7 ＝ 16  # 列表的最终大小为Py_SIZE = 16
```


## Tuple的内存利用

虽然Tuple不支持resize，但是我们可以粘贴两个元祖组成一个新的元组，这个操作类似于List的append，但是又不会额外的分配内存。

但我们不能把它当成append，因为每次都会进行一个分配内存和内存copy操作。

另一个Tuple的静态本质带来的好处是，resource caching。

Python是garbage collected，当一个变量不用了，内存会被回收并交回给OS。

但是，对于一个20个元素的Tuple，当它不再被用时，内存不会立即返还给OS，而是为了以后应用而暂缓保留，当一个新的Tuple被创建时，我们不会向OS重新申请分配内存，而是用现有reserved的free memory。

也就是，Tuple的创建很简单并且避免频繁与OS申请内存，创建一个具有10个元素的Tuple比创建一个List要快不少，55ns VS 280 ns。

我们可以通过Python源码看到上面的结论，代码位于Objects/tupleobject.c，我们可以清楚的看到tuple的粘贴过程：
```
新的大小等于两个tuple大小之和
重新分配内存
对于分配好的新内存，通过两个for循环将原来的两个元组拷贝到新的元组上
```

## 源码分析
```
static PyObject *
tupleconcat(PyTupleObject *a, PyObject *bb)
{
    Py_ssize_t size;
    Py_ssize_t i;
    PyObject **src, **dest;
    PyTupleObject *np;
    if (!PyTuple_Check(bb)) {
        PyErr_Format(PyExc_TypeError,
             "can only concatenate tuple (not \"%.200s\") to tuple",
                 Py_TYPE(bb)->tp_name);
        return NULL;
    }
#define b ((PyTupleObject *)bb)
    if (Py_SIZE(a) > PY_SSIZE_T_MAX - Py_SIZE(b))
        return PyErr_NoMemory();
    size = Py_SIZE(a) + Py_SIZE(b);
    np = (PyTupleObject *) PyTuple_New(size);
    if (np == NULL) {
        return NULL;
    }
    src = a->ob_item;
    dest = np->ob_item;
    for (i = 0; i < Py_SIZE(a); i++) {
        PyObject *v = src[i];
        Py_INCREF(v);
        dest[i] = v;
    }
    src = b->ob_item;
    dest = np->ob_item + Py_SIZE(a);
    for (i = 0; i < Py_SIZE(b); i++) {
        PyObject *v = src[i];
        Py_INCREF(v);
        dest[i] = v;
    }
    return (PyObject *)np;
#undef b
}
```

在分配内存函数PyTuple_New中，当大小小于20时，Python会直接从一个空闲的内存表中拿出来，不会重新申请，这减少了小元组的内存访问次数，宏PyTuple_MAXSAVESIZE为20
```
PyObject *
PyTuple_New(Py_ssize_t size)
{
    PyTupleObject *op;
    Py_ssize_t i;
    if (size < 0) {
        PyErr_BadInternalCall();
        return NULL;
    }
#if PyTuple_MAXSAVESIZE > 0
    if (size == 0 && free_list[0]) {
        op = free_list[0];
        Py_INCREF(op);
#ifdef COUNT_ALLOCS
        tuple_zero_allocs++;
#endif
        return (PyObject *) op;
    }
    if (size < PyTuple_MAXSAVESIZE && (op = free_list[size]) != NULL) {
        free_list[size] = (PyTupleObject *) op->ob_item[0];
        numfree[size]--;
#ifdef COUNT_ALLOCS
        fast_tuple_allocs++;
#endif
        /* Inline PyObject_InitVar */
#ifdef Py_TRACE_REFS
        Py_SIZE(op) = size;
        Py_TYPE(op) = &PyTuple_Type;
#endif
        _Py_NewReference((PyObject *)op);
    }
    else
#endif
    {
        /* Check for overflow */
        if ((size_t)size > ((size_t)PY_SSIZE_T_MAX - sizeof(PyTupleObject) -
                    sizeof(PyObject *)) / sizeof(PyObject *)) {
            return PyErr_NoMemory();
        }
        op = PyObject_GC_NewVar(PyTupleObject, &PyTuple_Type, size);
        if (op == NULL)
            return NULL;
    }
    for (i=0; i < size; i++)
        op->ob_item[i] = NULL;
#if PyTuple_MAXSAVESIZE > 0
    if (size == 0) {
        free_list[0] = op;
        ++numfree[0];
        Py_INCREF(op);          /* extra INCREF so that this is never freed */
    }
#endif
#ifdef SHOW_TRACK_COUNT
    count_tracked++;
#endif
    _PyObject_GC_TRACK(op);
    return (PyObject *) op;
}
```
