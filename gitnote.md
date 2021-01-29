git笔记

1、创建git库

先创建一个文件夹

```
$ mkdir learngit
$ cd learngit
$ pwd
/Users/michael/learngit
```

然后将这个文件夹转化为git管理的仓库

```
$ git init
```

2、注意事项：

git能够进行文本追踪的是文本文件，如txt、程序代码等。而Microsoft的word以及图片等是二进制的、没办法进行管理。

3、提交到git库

1）git add filename     添加到仓库

eg：```$ git add readme.txt```

要先确保该文件在git所在的目录中，本例是readme.txt要在learngit文件夹之下

2）git commit -m "description"   提交到仓库

eg:```$ git commit -m "wrote a readme file"```

git commit 可以一次将多个已经添加的文件进行提交，而-m后面的内容是对本次提交的描述

4、查看修改

1）git status

查看状态

2）git diff filename

查看改了哪里

3）提交修改后的文件和3中提到的一样

5、