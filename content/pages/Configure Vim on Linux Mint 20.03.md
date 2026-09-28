---
title: Configure Vim on Linux Mint 20.03
date: 2022-02-12
lastMod: 2026-09-28
tags:
- Linux
- vim
categories:
slug: vim-linux-mint
---

This is just a simple record. About the configuring process on Windows, here is [another blog](/vim-configure-process-recording/).


## Version Info

Vi IMproved 8.1 (2018 May 18)

Huge version with GTK3 GUI.

## .vimrc

[无插件Vim配置文件vimrc推荐与各VIM配置项解释](https://vimjc.com/vimrc.html)

```vim
" All system-wide defaults are set in $VIMRUNTIME/debian.vim and sourced by
" the call to :runtime you can find below.  If you wish to change any of those
" settings, you should do it in this file (/etc/vim/vimrc), since debian.vim
" will be overwritten everytime an upgrade of the vim packages is performed.
" It is recommended to make changes after sourcing debian.vim since it alters
" the value of the 'compatible' option.

runtime! debian.vim

" Vim will load $VIMRUNTIME/defaults.vim if the user does not have a vimrc.
" This happens after /etc/vim/vimrc(.local) are loaded, so it will override
" any settings in these files.
" If you don't want that to happen, uncomment the below line to prevent
" defaults.vim from being loaded.
let g:skip_defaults_vim = 1

" Uncomment the next line to make Vim more Vi-compatible
" NOTE: debian.vim sets 'nocompatible'.  Setting 'compatible' changes numerous
" options, so any other options should be set AFTER setting 'compatible'.
"set compatible

" Vim5 and later versions support syntax highlighting. Uncommenting the next
" line enables syntax highlighting by default.
if has("syntax")
syntax on
endif

" If using a dark background within the editing area and syntax highlighting
" turn on this option as well
"set background=dark

" Uncomment the following to have Vim jump to the last position when
" reopening a file
"au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$")  exe "normal! g'\""  endif

" Uncomment the following to have Vim load indentation rules and plugins
" according to the detected filetype.
"filetype plugin indent on

" The following are commented out as they cause vim to behave a lot
" differently from regular Vi. They are highly recommended though.
"set showcmd" Show (partial) command in status line.
"set showmatch" Show matching brackets.
"set ignorecase" Do case insensitive matching
"set smartcase" Do smart case matching
"set incsearch" Incremental search
"set autowrite" Automatically save before commands like :next and :make
"set hidden" Hide buffers when they are abandoned
"set mouse=a" Enable mouse usage (all modes)

" Source a global configuration file if available
if filereadable("/etc/vim/vimrc.local")
source /etc/vim/vimrc.local
endif

set nocompatible
set autoread"reload files when changed on disk (via Git)
set shortmess=atI"use ":h shortmess to view help

set magic
set title
set nobackup

set noerrorbells
set visualbell t_vb=
set t_vb=
set timeoutlen=1000

"Encodings
set encoding=utf-8
set fileencodings=usc-bom,utf-8,cp936,gb18030,big5,euc-jp,euc-kr,latin1
set fileformats=unix,dos,mac
set termencoding=utf-8
set formatoptions+=m
set formatoptions+=B

"View
set ruler
set number
set showcmd
set showmode
set showmatch
set matchtime=2
set guifont=Ubuntu\ Mono\ Regular\ 15 " IMPORTANT: :h15 can't be recognized

"Searching
set hlsearch"highlight searches
set incsearch"incremerntal searching
set ignorecase
set smartcase" no ignore case when Uppercase char present

"Tab
set expandtab" expand all tabs to spaces\
set smarttab
set shiftround

"Indent
set autoindent smartindent shiftround
set shiftwidth=4
set tabstop=4
set softtabstop=4

"Cursor
set cursorcolumn
set cursorline

" Theme
syntax enable
set background=dark
colorscheme solarized

"KeyMapping
nnoremap k gk
nnoremap gk k
nnoremap j gj
nnoremap gj j
```

## YouCompleteMe

### Cmake

$ pip install --user cmake

Looking in indexes: [https://pypi.tuna.tsinghua.edu.cn/simple/](https://pypi.tuna.tsinghua.edu.cn/simple/)
Collecting cmake
Downloading [https://pypi.tuna.tsinghua.edu.cn/packages/43/f7/cf42906411c364dbf60087a2d977b09ec5d0b87d3ba6be485fc031480f59/cmake-3.22.2-py2.py3-none-manylinux\_2\_17\_x86\_64.manylinux2014\_x86\_64.whl](https://pypi.tuna.tsinghua.edu.cn/packages/43/f7/cf42906411c364dbf60087a2d977b09ec5d0b87d3ba6be485fc031480f59/cmake-3.22.2-py2.py3-none-manylinux%5C_2%5C_17%5C_x86%5C_64.manylinux2014%5C_x86%5C_64.whl) (22.7 MB)
████████████████████████████████ 22.7 MB 4.6 MB/s 
Installing collected packages: cmake
Successfully installed cmake-3.22.2

### Quick start

$ sudo apt install build-essential cmake vim-nox python3-dev

### Error message

FAILED

ERROR: the build failed.

NOTE: it is *highly* unlikely that this is a bug but rather that this is a problem with the configuration of your system or a missing dependency. Please carefully read CONTRIBUTING.md and if you're sure that it is a bug, please raise an issue on the issue tracker, including the entire output of this script (with --verbose) and the invocation line used to run it.

The installation failed; please see above for the actual error. In order to get more information, please re-run the command, adding the --verbose flag. If you think this is a bug and you raise an issue, you MUST include the *full verbose* output.

For example, run:/usr/bin/python3 /home/cuso4d/.vim/plugged/YouCompleteMe/third_party/ycmd/build.py --all --verbose

Add "--verbose", it will show detailed info when building.

### If you want C# support...

If you chose "install all support of YCM", or you want a C# support, caution:

**The source that built.py provided is a 404 page...**

Here is the traceback:

Installing Omnisharp v1.37.11
Downloading Omnisharp from [https://github.com/OmniSharp/omnisharp-roslyn/releases/download/v1.37.11/omnisharp.http-linux-x64.tar.gz...Traceback](https://github.com/OmniSharp/omnisharp-roslyn/releases/download/v1.37.11/omnisharp.http-linux-x64.tar.gz...Traceback) (most recent call last):
File "/home/cuso4d/.vim/plugged/YouCompleteMe/third_party/ycmd/build.py", line 1256, in 
Main()
File "/home/cuso4d/.vim/plugged/YouCompleteMe/third_party/ycmd/build.py", line 1229, in Main
EnableCsCompleter( args )
File "/home/cuso4d/.vim/plugged/YouCompleteMe/third_party/ycmd/build.py", line 736, in EnableCsCompleter
package_path = DownloadCsCompleter( WriteStdout, download_data )
File "/home/cuso4d/.vim/plugged/YouCompleteMe/third_party/ycmd/build.py", line 786, in DownloadCsCompleter
DownloadFileTo( download_url, package_path )
File "/home/cuso4d/.vim/plugged/YouCompleteMe/third_party/ycmd/build.py", line 149, in DownloadFileTo
with urllib.request.urlopen( download_url ) as response:
File "/usr/lib/python3.8/urllib/request.py", line 222, in urlopen
return opener.open(url, data, timeout)
File "/usr/lib/python3.8/urllib/request.py", line 525, in open
response = self._open(req, data)
File "/usr/lib/python3.8/urllib/request.py", line 542, in _open
result = self._call_chain(self.handle_open, protocol, protocol +
File "/usr/lib/python3.8/urllib/request.py", line 502, in _call_chain
result = func(*args)
File "/usr/lib/python3.8/urllib/request.py", line 1397, in https_open
return self.do_open(http.client.HTTPSConnection, req,
File "/usr/lib/python3.8/urllib/request.py", line 1358, in do_open
r = h.getresponse()
File "/usr/lib/python3.8/http/client.py", line 1348, in getresponse
response.begin()
File "/usr/lib/python3.8/http/client.py", line 316, in begin
version, status, reason = self._read_status()
File "/usr/lib/python3.8/http/client.py", line 285, in _read_status
raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response

I don't need a C# support. If you do, maybe you can download the file manually, or modify the build.py file.

### C-family support

python3 install.py --clangd-completer
