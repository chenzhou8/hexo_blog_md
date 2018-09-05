---
title: linux-日常命令
date: 2018-04-23 23:03:50
tags: linux
---

### tree

```
-a：显示所有文件和目录；
-A：使用ASNI绘图字符显示树状图而非以ASCII字符组合；
-C：在文件和目录清单加上色彩，便于区分各种类型；
-d：先是目录名称而非内容；
-D：列出文件或目录的更改时间；
-f：在每个文件或目录之前，显示完整的相对路径名称；
-F：在执行文件，目录，Socket，符号连接，管道名称名称，各自加上"*"，"/"，"@"，"|"号；
-g：列出文件或目录的所属群组名称，没有对应的名称时，则显示群组识别码；
-i：不以阶梯状列出文件和目录名称；
-l：<范本样式> 不显示符号范本样式的文件或目录名称；
-l：如遇到性质为符号连接的目录，直接列出该连接所指向的原始目录；
-n：不在文件和目录清单加上色彩；
-N：直接列出文件和目录名称，包括控制字符；
-p：列出权限标示；
-P：<范本样式> 只显示符合范本样式的文件和目录名称；
-q：用“？”号取代控制字符，列出文件和目录名称；
-s：列出文件和目录大小；
-t：用文件和目录的更改时间排序；
-u：列出文件或目录的拥有者名称，没有对应的名称时，则显示用户识别码；
-x：将范围局限在现行的文件系统中，若指定目录下的某些子目录，其存放于另一个文件系统上，则将该目录予以排除在寻找范围外。
```

按照指定的层级列出目录文件...

```
tree -d -L 4  # 列出当前目录下的四层目录
```
<!-- more -->

### find

```
-amin<分钟>：查找在指定时间曾被存取过的文件或目录，单位以分钟计算；
-anewer<参考文件或目录>：查找其存取时间较指定文件或目录的存取时间更接近现在的文件或目录；
-atime<24小时数>：查找在指定时间曾被存取过的文件或目录，单位以24小时计算；
-cmin<分钟>：查找在指定时间之时被更改过的文件或目录；
-cnewer<参考文件或目录>查找其更改时间较指定文件或目录的更改时间更接近现在的文件或目录；
-ctime<24小时数>：查找在指定时间之时被更改的文件或目录，单位以24小时计算；
-daystart：从本日开始计算时间；
-depth：从指定目录下最深层的子目录开始查找；
-expty：寻找文件大小为0 Byte的文件，或目录下没有任何子目录或文件的空目录；
-exec<执行指令>：假设find指令的回传值为True，就执行该指令；
-false：将find指令的回传值皆设为False；
-fls<列表文件>：此参数的效果和指定“-ls”参数类似，但会把结果保存为指定的列表文件；
-follow：排除符号连接；
-fprint<列表文件>：此参数的效果和指定“-print”参数类似，但会把结果保存成指定的列表文件；
-fprint0<列表文件>：此参数的效果和指定“-print0”参数类似，但会把结果保存成指定的列表文件；
-fprintf<列表文件><输出格式>：此参数的效果和指定“-printf”参数类似，但会把结果保存成指定的列表文件；
-fstype<文件系统类型>：只寻找该文件系统类型下的文件或目录；
-gid<群组识别码>：查找符合指定之群组识别码的文件或目录；
-group<群组名称>：查找符合指定之群组名称的文件或目录；
-help或——help：在线帮助；
-ilname<范本样式>：此参数的效果和指定“-lname”参数类似，但忽略字符大小写的差别；
-iname<范本样式>：此参数的效果和指定“-name”参数类似，但忽略字符大小写的差别；
-inum<inode编号>：查找符合指定的inode编号的文件或目录；
-ipath<范本样式>：此参数的效果和指定“-path”参数类似，但忽略字符大小写的差别；
-iregex<范本样式>：此参数的效果和指定“-regexe”参数类似，但忽略字符大小写的差别；
-links<连接数目>：查找符合指定的硬连接数目的文件或目录；
-iname<范本样式>：指定字符串作为寻找符号连接的范本样式；
-ls：假设find指令的回传值为Ture，就将文件或目录名称列出到标准输出；
-maxdepth<目录层级>：设置最大目录层级；
-mindepth<目录层级>：设置最小目录层级；
-mmin<分钟>：查找在指定时间曾被更改过的文件或目录，单位以分钟计算；
-mount：此参数的效果和指定“-xdev”相同；
-mtime<24小时数>：查找在指定时间曾被更改过的文件或目录，单位以24小时计算；
-name<范本样式>：指定字符串作为寻找文件或目录的范本样式；
-newer<参考文件或目录>：查找其更改时间较指定文件或目录的更改时间更接近现在的文件或目录；
-nogroup：找出不属于本地主机群组识别码的文件或目录；
-noleaf：不去考虑目录至少需拥有两个硬连接存在；
-nouser：找出不属于本地主机用户识别码的文件或目录；
-ok<执行指令>：此参数的效果和指定“-exec”类似，但在执行指令之前会先询问用户，若回答“y”或“Y”，则放弃执行命令；
-path<范本样式>：指定字符串作为寻找目录的范本样式；
-perm<权限数值>：查找符合指定的权限数值的文件或目录；
-print：假设find指令的回传值为Ture，就将文件或目录名称列出到标准输出。格式为每列一个名称，每个名称前皆有“./”字符串；
-print0：假设find指令的回传值为Ture，就将文件或目录名称列出到标准输出。格式为全部的名称皆在同一行；
-printf<输出格式>：假设find指令的回传值为Ture，就将文件或目录名称列出到标准输出。格式可以自行指定；
-prune：不寻找字符串作为寻找文件或目录的范本样式;
-regex<范本样式>：指定字符串作为寻找文件或目录的范本样式；
-size<文件大小>：查找符合指定的文件大小的文件；
-true：将find指令的回传值皆设为True；
-typ<文件类型>：只寻找符合指定的文件类型的文件；
-uid<用户识别码>：查找符合指定的用户识别码的文件或目录；
-used<日数>：查找文件或目录被更改之后在指定时间曾被存取过的文件或目录，单位以日计算；
-user<拥有者名称>：查找符和指定的拥有者名称的文件或目录；
-version或——version：显示版本信息；
-xdev：将范围局限在先行的文件系统中；
-xtype <文件类型>：此参数的效果和指定-type参数类似，差别在于它针对符号连接检查。

如下命令: 
find . -type f -name "*.py[co]" -delete  # 寻找当前目录下 所有以pyc结尾的文件 并删除

运维中经常用到的寻找大文件的命令: 
find / -type f -size +80M  # 寻找/目录下 所有size大于80Mb的文件
```

### dpkg

```
用法：dpkg [<选项> ...] <命令>

Commands:
  -i|--install       <.deb file name> ... | -R|--recursive <directory> ...
  --unpack           <.deb file name> ... | -R|--recursive <directory> ...
  -A|--record-avail  <.deb file name> ... | -R|--recursive <directory> ...
  --configure        <package> ... | -a|--pending
  --triggers-only    <package> ... | -a|--pending
  -r|--remove        <package> ... | -a|--pending
  -P|--purge         <package> ... | -a|--pending
  -V|--verify <package> ...        Verify the integrity of package(s).
  --get-selections [<pattern> ...] Get list of selections to stdout.
  --set-selections                 Set package selections from stdin.
  --clear-selections               Deselect every non-essential package.
  --update-avail [<Packages-file>] Replace available packages info.
  --merge-avail [<Packages-file>]  Merge with info from file.
  --clear-avail                    Erase existing available info.
  --forget-old-unavail             Forget uninstalled unavailable pkgs.
  -s|--status <package> ...        Display package status details.
  -p|--print-avail <package> ...   Display available version details.
  -L|--listfiles <package> ...     List files 'owned' by package(s).
  -l|--list [<pattern> ...]        List packages concisely.
  -S|--search <pattern> ...        Find package(s) owning file(s).
  -C|--audit [<package> ...]       Check for broken package(s).
  --yet-to-unpack                  Print packages selected for installation.
  --predep-package                 Print pre-dependencies to unpack.
  --add-architecture <arch>        Add <arch> to the list of architectures.
  --remove-architecture <arch>     Remove <arch> from the list of architectures.
  --print-architecture             Print dpkg architecture.
  --print-foreign-architectures    Print allowed foreign architectures.
  --assert-<feature>               Assert support for the specified feature.
  --validate-<thing> <string>      Validate a <thing>'s <string>.
  --compare-versions <a> <op> <b>  Compare version numbers - see below.
  --force-help                     Show help on forcing.
  -Dh|--debug=help                 Show help on debugging.

  -?, --help                       显示本帮助信息。
      --version                    显示版本信息。

Assert 特性： support-predepends, working-epoch, long-filenames,
  multi-conrep, multi-arch, versioned-provides.

Validatable things: pkgname, archname, trigname, version.

调用 dpkg 并带参数 -b, --build, -c, --contents, -e, --control, -I, --info,
  -f, --field, -x, --extract, -X, --vextract, --ctrl-tarfile, --fsys-tarfile
是针对归档文件的。 (输入 dpkg-deb --help 获取帮助)

选项：
  --admindir=<目录>          使用 <目录> 而非 /var/lib/dpkg。
  --root=<目录>              安装到另一个根目录下。
  --instdir=<目录>           改变安装目录的同时保持管理目录不变。
  --path-exclude=<表达式>    不要安装符合Shell表达式的路径。
  --path-include=<表达式>    在排除模式后再包含一个模式。
  -O|--selected-only         忽略没有被选中安装或升级的软件包。
  -E|--skip-same-version     忽略版本与已安装软件版本相同的软件包。
  -G|--refuse-downgrade      忽略版本早于已安装软件版本的的软件包。
  -B|--auto-deconfigure      就算会影响其他软件包，也要安装。
  --[no-]triggers            跳过或强制随之发生的触发器处理。
  --verify-format=<格式>     检查输出格式('rpm'被支持)。
  --no-debsig                不去尝试验证软件包的签名。
  --no-act|--dry-run|--simulate
                             仅报告要执行的操作 - 但是不执行。
  -D|--debug=<八进制数>      开启调试(参见 -Dhelp 或者 --debug=help)。
  --status-fd <n>            发送状态更新到文件描述符<n>。
  --status-logger=<命令>     发送状态更新到 <命令> 的标准输入。
  --log=<文件名>             将状态更新和操作信息到 <文件名>。
  --ignore-depends=<软件包>,...
                             忽略关于 <软件包> 的所有依赖关系。
  --force-...                忽视遇到的问题(参见 --force-help)。
  --no-force-...|--refuse-...
                             当遇到问题时中止运行。
  --abort-after <n>          累计遇到 <n> 个错误后中止。

可供--compare-version 使用的比较运算符有：
 lt le eq ne ge gt        (如果版本号为空，那么就认为它先于任意版本号)；
 lt-nl le-nl ge-nl gt-nl  (如果版本号为空，那么就认为它后于任意版本号)；
 < << <= = >= >> >        (仅仅是为了与主控文件的语法兼容)。

'apt' 和 'aptitude' 提供了更为便利的软件包管理。
```

如下例子: 
```
dpkg --list | grep postgresql  # 列出postgresql相关的所有安装包
dpkg --purge postgresql  # 删除postgresql
```

