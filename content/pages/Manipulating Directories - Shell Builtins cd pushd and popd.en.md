---
title: Manipulating Directories - Shell Builtins cd pushd and popd
ai: translated
date: 2025-09-04
lastMod: 2025-09-04
tags:
- shell
categories:
slug: cd-pushd-popd
---

Most modern shells have a set of shell builtins (e.g. [zsh](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html)), some of which can be used to manipulate directories.


To manipulate directories, a directory stack structure is maintained in memory. In bash it can also be accessed through the `$DIRSTACK` shell variable. [bash's introduction to the directory stack](https://www.gnu.org/software/bash/manual/html_node/The-Directory-Stack.html#The-Directory-Stack), [zsh's introduction to the directory stack](https://zsh.sourceforge.io/Intro/intro_6.html#SEC6)

With pushd and popd, you can enter a series of directories and leave them in reverse order.

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

Taking zsh as an example, the directory stack is implemented as a linked list. It is located in `Src/Bulitin.c`.

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

  + [How to read the `BUILTIN` macro](https://github.com/zsh-users/zsh/blob/3cd363c8804a4569e601f4486a0001b1de14811f/Etc/zsh-development-guide#L498)


  + The second parameter specifies the behavior of `cd`, `popd`, and `pushd`: treat invalid options as arguments; support `-` as an argument; support using `--` to indicate that everything after it is not an option.

```c
/* Builtin option handling */
#define BINF_SKIPINVALID	(1<<12)	/* Treat invalid option as argument */
#define BINF_KEEPNUM		(1<<13) /* `[-+]NUM' can be an option */
#define BINF_SKIPDASH		(1<<14) /* Treat `-' as argument (maybe `+') */
#define BINF_DASHDASHVALID	(1<<15) /* Handle `--' even if SKIPINVALD */
```

  + The third parameter specifies that all three builtins are implemented with a single `bin_cd` function.

  + The fourth and fifth parameters indicate the minimum and maximum number of arguments for this builtin

  + The sixth parameter is used when a single function is shared by multiple builtins, using different values to indicate which command invoked it, resulting in different behavior.

  + The seventh parameter is the list of available options, and the eighth is the options that must be used.

[Implementation of `bin_cd`](https://github.com/zsh-users/zsh/blob/3cd363c8804a4569e601f4486a0001b1de14811f/Src/builtin.c#L839):

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

  + Declare a linked-list node `dir`


  + If it is a restricted shell, it cannot be executed

  + If `doprintdir` is -1, change it to 1; otherwise change it to 0 (is this some global variable that can turn itself back?.. no time to look for now)

  + `chasinglinks` determines whether to resolve symbolic links. If the argument includes `-P`, or (`chaselinks` is set via setopt and there is no `-L` argument), resolve symbolic links; otherwise do not.

  + `queue_signals()` is probably to ensure something like signal transactions...?

  + Push the current directory onto the top of the stack

  + `cd_get_dest()` computes the target directory depending on which command was invoked (`cd`, `pushd`, `popd`); it returns non-zero if the target directory is absent or inaccessible (which can happen with the `-s` argument).

  + `cd_new_pwd()` jumps to the directory it computed.

