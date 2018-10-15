title: 我的vim配置(.vimrc)
date: 2016-05-15 12:45:33
categories: vim
tags: vim
description: vim配置的介绍, deepin linux 2015


---

上周三更新了Deepin Linux系统，将deepin2014升级到deepin2015。新版deepin对界面优化了不少，开关机铃声蛮不错的，能够自定义就更好了(仔细琢磨，查看deepin的源码应该可以实现自定义开关机铃声的).

话不多说，进入今天主题: vim配置。

效果图如下:

![vim效果图](http://7xorah.com1.z0.glb.clouddn.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE20160515162228.png)

使用vundle管理vim插件, 配置代码部分:
在home目录下添加：

> vim ~/.vimrc

.vimrc内容:

```vim

set nocompatible               " be iMproved
 filetype off                   " required!
set rtp+=~/.vim/bundle/vundle/
   call vundle#rc()

" 设置退格键的正确性
set backspace=indent,eol,start

" let Vundle manage Vundle
" required!
Bundle 'gmarik/vundle'

" 我的Bundle配置"
Bundle 'scrooloose/nerdtree'      "树形目录插件
Bundle 'majutsushi/tagbar'        "显示函数列表插件
Bundle "tomasr/molokai"           "皮肤插件
Bundle 'kien/ctrlp.vim'           "快熟找到项目中的文件插件
Bundle 'scrooloose/syntastic'     "多语言语法与编码风格检查插件
Bundle 'Valloric/YouCompleteMe'   "多语言自动补全插件, 新版本超赞
Bundle 'bling/vim-airline'        "时间管理插件

"airline配置
set laststatus=2

" <F2>启动nerdtree
let NERDTreeWinPos='left'
let NERDTreeWinSize=31
let NERDTreeChDirMode=1
map <F2> :NERDTreeToggle<CR>

" Tagbar
let g:tagbar_width=35
let g:tagbar_autofocus=1
nmap <F3> :TagbarToggle<CR>

" syntastic
let g:syntastic_check_on_open = 1
let g:syntastic_error_symbol = '✗'
let g:syntastic_warning_symbol = '⚠'

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_python_checkers=['flake8']

" YouCompleteMe
let g:ycm_pythona_binary_path = "/usr/bin/python3" "添加YouCompleteMe对Python3的支持"

set nu
syntax on
set cursorline

" 设置tab
set ts=4
set expandtab
set shiftwidth=4
set smartindenta
colorscheme molokai
highlight NonText guibg=#060606
highlight Folded  guibg=#0A0A0A guifg=#9090D0

```

编辑好.vimrc文件后，进入vim命令模式，执行下列命令中所需命令安装更新插件等.
Vundle命令：

```
:BundleList-列举出列表中(.vimrc中)配置的所有插件
:BundleInstall-安装列表中全部插件
:BundleInstall!-更新列表中全部插件
:BundleSearch foo-查找foo插件
:BundleSearch! foo-刷新foo插件的缓存
:BundleClean-清除列表中没有的插件
:BundleClean!-清楚列表中没有的插件
```

接下来配置YouCompleteMe插件对vim的支持。
官网 [YouCompleteMe官网](https://github.com/Valloric/YouCompleteMe)
官网针对Ubuntu Linux x64安装YouCompleteMe有以下介绍:

```
Please refer to the full installation Guide below; the following commands are provided on a best-effort basis and may not work for you.
请参阅下列的完全安装指南；下列的命令提供了最佳的基础安装，同样，这套解决方案存在对您不管用的可能性。

Make sure you have Vim 7.3.598 with python2 or python3 support. Ubuntu 14.04 and later have a Vim that's recent enough. You can see the version of Vim installed by running <code>vim --version</code>. If
the version is too old, you may need to compile Vim form source(don't worry, it's easy).
请确保你安装了拥有Python2 或者Python3 支持的 7.3.598或更高版本的Vim. Ubuntu 14.04 或者更高的版本的系统是足够支持的。 你可以在终端通过vim --version命令查看当前系统的vim版本。如果vim版本太老，则需要重新安装更高版本的vim（不用太担心，很拥有的）。

译者注: Vim最新版本已更新到7.4。重新编译安装Vim参照：[编译Vim](http://www.linuxidc.com/Linux/2014-04/99717.htm)

Install YouCompleteMe with Vundle.
请通过[Vundle](https://github.com/gmarik/vundle)安装YouCompleteMe.

Remember: YCM is a plugin with a compiled component. If you update YCM using Vundle and the ycm_core library APIs have changed(happens rarely), YCM will notify you to recompile it. You should then rerun the install process.
请记住：YouCompleteMe 是一个带有编译组件的插件. 如果你通过Vundle来更新YouCompleteMe, 并且ycm_core库的API发生了改变，YCM会提醒你重新编译它，这时，需要你重新运行安装程序。

Install development tools and CMAKE: sudo apt-get install build-essential cmake
请通过sudo apt-get install build-essential cmake安装开发工具build-essential和CMAKE

Make sure you have Python headers installed: sudo apt-get install python-dev python3-dev
请确保你安装了Python的头文件, 可以通过: sudo apt-get install python-dev python3-dev安装。

Compiling YCM with semantic support for C-family languages:
通过以下命令编译对C-family语义支持的YouCompleteMe:
   cd ~/.vim/bundle/YouCompleteMe
   ./install.py --clang-completer

Compiling YCM without semantic support for C-family languages:
通过以下命令编译不对C-family语义支持的YouCompleteMe:
    cd ~/.vim/bundle/YouCompleteMe
    ./install.py

The following addition language suppoert options are avalable：
  - C# support: add --omnisharp-completer when calling ./install.py.
  - Go support: ensure go is installed and add --gocode-completer when calling ./install.py.
  - TypeScript support: install nodejs and npm then isntall the TypeScript SDK with npm install -g TypeScript.
  - JavaScript support: install nodejs and npm and add --tern-completer when calling ./install.py.
  - Rust support: install rustc and cargo and add --racer-completer when calling ./install.py.
下列附加的语言支持选项可供选择：
  - 对C#的支持: 当调用 ./install.py 时 添加 --omnisharp-completer 
  - 对GO的支持: 当调用 ./install.py 时 添加 --gocode-completer
  - 对TypeScript的支持: 安装nodejs 和 npm 然后通过 npm install -g typescript 安装TypeScript SDK
  - 对JavaScript的支持：安装nodejs 和 npm 然后当调用 ./install.py 时 添加 --tern-completer 
  - 对Rust的支持: 安装 rustc 和 cargo  然后当调用 ./install.py 时 添加 --racer-completer

To simply compile with everything enabled, there's a --all flag. So, to install with all langeage features, ensure npm, go, mono, rust, and typescript API are installed and in your PATH, then simply run:
通过 --all 可以简单编译，就能能对上述所有语言的支持。当然，这需要安装所有语言特征，确保 npm, go, mono, rust, typescript API 都已成功安装到环境变量中。然后简单的运行：
    cd ~.vim/bundle/YouCompleteMe
    ./install.py --all

That's it. You're done. Refer to the User Guide section on how to use YCM. Don't forget that if you want the C-family semantic completion engine to work, you will need to provide the compilation flags for your project to YCM. It's all in the User Guide.
已经完成编译安装了。请参照用户指南来学习如何使用YCM。别忘了， 如果你想让 C-family 语义引擎正常工作， 你需要为你的项目提供YouCompleteMe的编译选项。用户指南里又详细介绍。

YCM comes with sane defaults for its options, but you still may want to take a look at what's available for configuration. There are a few interestion options that are conservatively truned off by default that you may want to tuen on.
YCM带有完整的默认选项， 但如果你仍然想查看配置的功用。这里提供了几个默认情况下是关闭的关闭的配置选项，如有需要的话，请自行打开。
```
<完>











