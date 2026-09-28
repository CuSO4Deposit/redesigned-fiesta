---
title: Configure gVim on Windows
date: 2021-10-02
lastMod: 2026-09-28
tags:
  - vim
categories:
slug: gvim-windows
ai: translated
---

## Version Info

gVim version 8.1.1 8.2.0577 for Windows

## Initialize

[Recommended No-Plugin Vim Configuration (vimrc) and Explanations of Various Vim Options](https://vimjc.com/vimrc.html)

First add these lines to _vimrc.

```vim
set nocompatible
set autoread
set shortmess=atI

set magic
set title
set nobackup

set noerrorbells
set visualbell t_vb=
set t_vb=
set timeoutlen=500

set fileencodings=ucs-bom,utf-8,cp936,gb18030,big5,euc-jp,euc-kr,latin1
set fileformats=unix,dos,mac
set termencoding=utf-8
set formatoptions+=m
set formatoptions+=B
set guifont=Source\ Code\ Pro:h14

set ruler
set number
set nowrap
set showcmd
set showmode
set showmatch
set matchtime=2

set hlsearch
set incsearch
set ignorecase
set smartcase

set expandtab
set smarttab
set shiftround

set autoindent smartindent shiftround
set shiftwidth=4
set tabstop=4
set softtabstop=4

set cursorcolumn
set cursorline

filetype on
syntax on

set foldmethod=syntax
set nofoldenable
```

## Install Theme: Solarized

[A Roundup of 15 Famous Vim Color Schemes - Vim Beginner Tutorial (7)](https://vimjc.com/vim-color-schemes.html)

[github author="altercation" project="vim-colors-solarized"][/github]

Download theme and unpack *.zip. Add Solarized.vim to /Vim/vim81/color directory.Then add this line to _vimrc.

```vim
colorscheme Solarized
```

## Install Vim-plug package manager

[Introducing vim-plug, the Lightweight and Efficient Vim Plugin Manager - Vim Plugins (9)](https://vimjc.com/vim-plug.html)
[How to Install Vim Plugins](https://zhuanlan.zhihu.com/p/108697739)

### Install Vim-plug

First download the plug.vim and put it into the /autoload directory. I find there's already a plug.vim. Maybe it's built-in at Vim ver. 8.1.

Add these lines to _vimrc.

```vim
call plug#begin('D:\Program\ Files\ (x86)\Vim\vim81\pack')

call plug#end()
```

Restart Vim. An error indication:

[vim-plug] `git` executable not found. Most commands

It's because Win10 doesn't have a git as a built-in.[ref][What to Do When Vim on Win10 Reports "git executable not found"](https://jingyan.baidu.com/article/08b6a59103fd2954a9092235.html)[/ref] Install Git.

### Install Git[ref] [Git for Windows](https://gitforwindows.org/) [/ref]

Download Git 2.33.0.2-64-bit.exe. Install.
Restart Vim. The error indication disappears.

### Use Vim-plug to install plugin

Add a github link to the "call plug" mentioned. Then in any gVim window, use command mode, type :PlugInstall. The plugin will be automatically installed.

example:

[github author = "preservim" project = "nerdtree"][/github]

Its URL is [https://github.com/preservim/nerdtree](https://github.com/preservim/nerdtree). Add a line to _vimrc.

```vim
call plug#begin('D:\Program\ Files\ (x86)\Vim\vim81\pack')
Plug 'vim-syntastic/syntastic'
Plug 'preservim/nerdtree'
call plug#end()
```

Then open any file in gVim, type :PlugInstall, the plugin is automatically installed.

vim-plug window

## Plugin: YouCompleteMe

Installing YouCompleteMe is a very complicated and annoying process... But it's a very very powerful tool.

### Install YCM Plugin

[github author = "ycm-core" project = "YouCompleteMe#windows"][/github]

Install it by vim-plug.

### Upgrade Vim

[admonition title="Note" color="orange"]You should backup your theme and _vimrc before each time you upgrade Vim. They will be deleted.[/admonition]

When open any file, there's an error "YouCompleteMe unavailable: requires Vim 8.1.2269+". Sadly my version is 8.1.1, so I have to upgrade it. I'm afraid I have to re-edit lots of settings.

Download vim at github.

[github author="vim" project="vim-win32-installer"][/github]

The setup automatically deleted the old version. Glad that I don't have to change a lot. Download "plug.vim" for vim-plug and put it in /vim/vim82/autoload. Then do this change and reinstall plugins.

```vim
call plug#begin('D:\Program\ Files\ (x86)\Vim\vim81\pack')

->

call plug#begin('D:\Program\ Files\ (x86)\Vim\vim82\pack')
```

### Install [Python](https://www.python.org/downloads/)

### Install [Cmake](https://cmake.org/download/)

### Microsoft VS2019

Already exist in the computer.

### Configure YCM

go to the directory D:\Program Files (x86)\Vim\vim82\pack\YouCompleteMe. Run cmd.

type in

python install.py --clangd-completer

Return:

File D:\Program Files (x86)\Vim\vim82\pack\YouCompleteMe\third_party\ycmd\build.py does not exist; you probably forgot to run:
git submodule update --init --recursive

Run the code it told, return:

fatal: could not get a repository handle for submodule 'third_party/ycmd'

Find a help here: [YouCompleteMe Installation Process Record 2021 - Programmer Tutorial](http://www.manongjc.com/detail/24-kxzqbxffbkqojjv.html)

Go to directory and run cmd, code:

git clone [https://bitbucket.org/mrabarnett/mrab-regex.git](https://bitbucket.org/mrabarnett/mrab-regex.git)

Return:

D:\Program Files (x86)\Vim\vim82\pack\YouCompleteMe\third_party\ycmd\mrab-regex>git clone [https://bitbucket.org/mrabarnett/mrab-regex.git](https://bitbucket.org/mrabarnett/mrab-regex.git)
Cloning into 'mrab-regex'...
Receiving objects: 100% (4768/4768), 48.52 MiB 1.01 MiB/s, done.
Resolving deltas: 100% (756/756), done

return to the ycm dir, repeat the operation.

Things turn out that there are many files missing in my plugin dir. So I deleted them all, enable VPN and install YCM and it's core again. It works, in the ycmd dir many files appears. Then I tried again:

```
python install.py --clangd-completer
```

And python runs normally, despite some warnings.

Some warnings

And it automatically installed clang. Now the python install procejure is done.

Then set encoding=utf-8. Before doing this, in order to keep the menus from becoming messy code, i have to change language to English. That's to add this line [as the first line of _vimrc](https://zhidao.baidu.com/question/681772562373517612.html):

```vim
set langmenu=none
```

Then add set encoding=utf-8 to _vimrc, it works well.

Now when I open a file in vim, it errors:

YouCompleteMe unavailable: unable to load Python.

Go on finding solution, there's one saying that 32-bit vim isn't compatible with 64-bit python. So i should get a 64-bit vim. But first i'll try if editing the _vimrc can solve the problem.

type :echo has('python3'), it returns 0.

0

type :set pythonthreedll?, it returns python3.8.

But my python is 3.6. Add a line in the _vimrc.

```
set pythonthreedll=python36.dll
```

And it works. No error happens when i start vim.

Ohhhhhhhhh

YouCompleteMe is working properly now.

Conclusion: In my installing process, the biggest problem lies in the missing files. Next time installing YCM (especially at places where GitHub isn't completely accessible), pay more attention to files integrity.

Some other references are listed here.
[Record of Installing the Vim Plugin YouCompleteMe (Allegedly the Hardest Vim Plugin to Install?)](https://www.cnblogs.com/YMaster/p/11209813.html)
[YouCompleteMe Installation Process Record 2021](https://www.cnblogs.com/windin/p/14954527.html)
[Pitfalls Encountered When Installing the YouCompleteMe Plugin on Vim8](https://zhuanlan.zhihu.com/p/73429590)
