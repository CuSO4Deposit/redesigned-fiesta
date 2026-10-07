---
title: Manipulating Directories - Shell Builtins cd pushd and popd
date: 2025-09-04
lastMod: 2025-09-04
tags:
- shell
categories:
slug: cd-pushd-popd
---

大多数现代 shell 有一系列 shell builtins（例：[zsh](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html) ），其中一些可以用来操作目录。


为了操作目录，在内存中维护了一个目录栈结构。在 bash 中也可以通过 `$DIRSTACK` shell variable 访问到。[bash 的目录栈介绍页](https://www.gnu.org/software/bash/manual/html_node/The-Directory-Stack.html#The-Directory-Stack)，[zsh 的目录栈介绍页](https://zsh.sourceforge.io/Intro/intro_6.html#SEC6)

通过 pushd 和 popd，可以进入一系列目录并且按反序退出。

```
[1:cuso4d@nightcord-laborari:~]
$ pwd
/home/cuso4d
[1:cuso4d@nightcord-laborari:~]
$ pushd ~/source/zsh
~/source/zsh ~
[1:cuso4d@nightcord-laborari:~/source/zsh on master]
$ pushd ~/.ssh
~/.ssh ~/source/zsh ~
[1:cuso4d@nightcord-laborari:~/.ssh]
$ popd
~/source/zsh ~
[1:cuso4d@nightcord-laborari:~/source/zsh on master]
$ popd
~
[1:cuso4d@nightcord-laborari:~]
$ pwd
/home/cuso4d
```

以 zsh 为例子，目录栈是使用链表实现的。位置在 `Src/Bulitin.c`。

```c
static struct builtin builtins[] =
{
	// ...
	BUILTIN("cd", BINF_SKIPINVALID | BINF_SKIPDASH | BINF_DASHDASHVALID, bin_cd, 0, 2, BIN_CD, "qsPL", NULL),
    BUILTIN("popd", BINF_SKIPINVALID | BINF_SKIPDASH | BINF_DASHDASHVALID, bin_cd, 0, 1, BIN_POPD, "q", NULL),
    BUILTIN("pushd", BINF_SKIPINVALID | BINF_SKIPDASH | BINF_DASHDASHVALID, bin_cd, 0, 2, BIN_PUSHD, "qsPL", NULL),
    // ...
}    
```

  + [`BUILTIN` 宏的阅读方法](https://github.com/zsh-users/zsh/blob/3cd363c8804a4569e601f4486a0001b1de14811f/Etc/zsh-development-guide#L498)


  + 第二个参数指定了 `cd`, `popd`, `pushd` 的行为：将无效选项视作参数；支持 `-` 作为参数；支持以 `--` 标识其后均为非选项。

```c
/* Builtin option handling */
#define BINF_SKIPINVALID	(1<<12)	/* Treat invalid option as argument */
#define BINF_KEEPNUM		(1<<13) /* `[-+]NUM' can be an option */
#define BINF_SKIPDASH		(1<<14) /* Treat `-' as argument (maybe `+') */
#define BINF_DASHDASHVALID	(1<<15) /* Handle `--' even if SKIPINVALD */
```

  + 第三个参数指定这三个 builtins 都是使用一个 `bin_cd` 的函数实现的。

  + 第四、五个参数标识这个 builtin 的最小和最大参数量

  + 第六个参数用于在一个函数被多个 builtins 使用时，使用不同的值指示是哪个命令调用的，来带来不同的行为。

  + 第七个参数是可用的参数列表，第八个是必被用的参数。

[`bin_cd` 的实现](https://github.com/zsh-users/zsh/blob/3cd363c8804a4569e601f4486a0001b1de14811f/Src/builtin.c#L839)：

```c
/* set if we are resolving links to their true paths */
static int chasinglinks;

/* The main pwd changing function.  The real work is done by other     *
 * functions.  cd_get_dest() does the initial argument processing;     *
 * cd_do_chdir() actually changes directory, if possible; cd_new_pwd() *
 * does the ancillary processing associated with actually changing    *
 * directory.                                                          */

/**/
int
bin_cd(char *nam, char **argv, Options ops, int func)
{
    LinkNode dir;

    if (isset(RESTRICTED)) {
	zwarnnam(nam, "restricted");
	return 1;
    }
    doprintdir = (doprintdir == -1);

    chasinglinks = OPT_ISSET(ops,'P') ||
	(isset(CHASELINKS) && !OPT_ISSET(ops,'L'));
    queue_signals();
    zpushnode(dirstack, ztrdup(pwd));
    if (!(dir = cd_get_dest(nam, argv, OPT_ISSET(ops,'s'), func))) {
	zsfree(getlinknode(dirstack));
	unqueue_signals();
	return 1;
    }
    cd_new_pwd(func, dir, OPT_ISSET(ops, 'q'));

    unqueue_signals();
    return 0;
}

```

  + 声明一个链表 Node `dir`


  + 如果是受限 shell 则执行不了

  + 如果 `doprintdir` 是 -1 就改成 1, 否则就改成 0 （这是什么能自己变回去的全局变量吗。。暂时没空看）

  + `chasinglinks` 决定是否展开符号链接。如果参数有 `-P` 或者（setoption 了 `chaselinks` 且没有参数 `-L`），就展开符号链接，否则就不展开。

  + `queue_signals()` 大概是为了保证信号的 transactions 之类的……？

  + 把当前目录推到栈顶

  + `cd_get_dest()` 根据调用的命令的不同（`cd`, `pushd`, `popd`），算出来目标目录，如果目标目录无或者不能访问（在参数 `-s` 时可能发生）就返回非零。

  + `cd_new_pwd()` 跳到算出来应该跳到的目录。


