---
title: Clangd cannot find standard header
date: 2024-01-15
lastMod: 2025-10-18
tags:
- clangd
- lsp
categories:
---

When using clangd (16.0.2) as LSP, it throws the following error:

```
[pp_file_not_found] Line 1: 'stdlib.h' file not found
```

But stdlib.h exists, and gcc compilation passed.


## TL;DR

Create [compilation database file](https://clangd.llvm.org/installation.html#project-setup) at root of project, content:

```
-isystem
C:\Users\username\scoop\apps\gcc\current\x86_64-w64-mingw32\include
-target
x86_64-pc-windows-gnu
```

Where the 2nd line is the path to stdlib.h.

## Debug Process

Use `--check` to run clangd and get error info:

```
% .\clangd.exe --check=\path\to\file.c
```

Log:

```
I[12:18:46.915] clangd version 16.0.2 (https://github.com/llvm/llvm-project 18ddebe1a1a9bde349441631365f0472e9693520)
...
I[12:18:46.924] Loading compilation database...
I[12:18:46.934] Failed to find compilation database for C:\Users\username\path\to\c_file.c
I[12:18:46.935] Generic fallback command is: "C:\\Users\\username\\scoop\\apps\\gcc\\11.2.0\\bin\\clang" "-resource-dir=C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\lib\\clang\\16" -- "C:\\Users\\username\\path\\to\\c_file.c"
...
I[12:18:46.970] Testing features at each token (may be slow in large files)
I[12:18:47.006] All checks completed, 2 errors
```

According to [this post](https://clangd.llvm.org/guides/system-headers#fixing-missing-system-header-issues), "Generic fallback ..." entry means no compilation database. Create an empty `compile_flags.txt` besides `file.c`, re-run check command, log:

```
I[13:21:45.369] clangd version 16.0.2 (https://github.com/llvm/llvm-project 18ddebe1a1a9bde349441631365f0472e9693520)
I[13:21:45.370] Features: windows+grpc
I[13:21:45.370] PID: 2248
I[13:21:45.370] Working directory: C:\Users\username\AppData\Roaming\nvim-data\mason\packages\clangd\clangd_16.0.2\bin
I[13:21:45.371] argv[0]: C:\Users\username\AppData\Roaming\nvim-data\mason\packages\clangd\clangd_16.0.2\bin\clangd.exe
I[13:21:45.371] argv[1]: --check=C:\Users\username\path\to\c_file.c
I[13:21:45.376] Entering check mode (no LSP server)
I[13:21:45.376] Testing on source file C:\Users\username\path\to\c_file.c
I[13:21:45.377] Loading compilation database...
I[13:21:45.388] Loaded compilation database from C:\Users\username\path\to\compile_flags.txt
I[13:21:45.388] Compile command from CDB is: "C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\bin\\clang-tool" "-isystem $HOME/scoop/apps/gcc/current/include/" "-resource-dir=C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\lib\\clang\\16" -- "C:\\Users\\username\\path\\to\\c_file.c"
I[13:21:45.389] Parsing command...
I[13:21:45.401] internal (cc1) args are: -cc1 -triple x86_64-pc-windows-msvc19.20.0 -fsyntax-only -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name c_file.c -mrelocation-model pic -pic-level 2 -mframe-pointer=none -fmath-errno -ffp-contract=on -fno-rounding-math -mconstructor-aliases -funwind-tables=2 -target-cpu x86-64 -tune-cpu generic -mllvm -treat-scalable-fixed-error-as-warning "-fcoverage-compilation-dir=C:\\Users\\username\\path\\to" -resource-dir "C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\lib\\clang\\16" -isystem " $HOME/scoop/apps/gcc/current/include/" -c-isystem "C:\\Users\\username\\scoop\\apps\\gcc\\current\\include" -cxx-isystem "C:\\Users\\username\\scoop\\apps\\gcc\\current\\include" -internal-isystem "C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\lib\\clang\\16\\include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 10.0/VC/include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 9.0/VC/include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 9.0/VC/PlatformSDK/Include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 8/VC/include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 8/VC/PlatformSDK/Include" "-fdebug-compilation-dir=C:\\Users\\username\\path\\to" -ferror-limit 19 -fmessage-length=120 -fno-use-cxa-atexit -fms-extensions -fms-compatibility -fms-compatibility-version=19.20 -fdelayed-template-parsing -no-round-trip-args -faddrsig -x c "C:\\Users\\username\\path\\to\\c_file.c"
I[13:21:45.402] Building preamble...
I[13:21:45.408] Indexing headers...
I[13:21:45.409] Built preamble of size 224804 for file C:\Users\username\path\to\c_file.c version null in 0.01 seconds
E[13:21:45.409] [pp_file_not_found] Line 1: 'stdlib.h' file not found
I[13:21:45.410] Building AST...
E[13:21:45.427] [-Wimplicit-function-declaration] Line 14: call to undeclared library function 'malloc' with type 'void *(unsigned long long)'; ISO C99 and later do not support implicit function declarations
I[13:21:45.428] Indexing AST...
I[13:21:45.428] Building inlay hints
I[13:21:45.428] Building semantic highlighting
I[13:21:45.429] Testing features at each token (may be slow in large files)
I[13:21:45.465] All checks completed, 2 errors
```

Actually, two `stdlib.h` files are in *C:\Users\username\scoop\apps\gcc\current\include\C++\11.2.0\* and *C:\Users\username\scoop\apps\gcc\current\x86_64-w64-mingw32\include.* Notice the `-cxx-isystem` already considers *C:\Users\username\scoop\apps\gcc\current\include*, but still cannot find the file. I don't know why, maybe clangd doesn't perform a recursive search?

In the text editor, the LSP successfully found files in *C:\Users\username\scoop\apps\gcc\current\include*. So I tried this:

```
-isystem
C:\Users\username\scoop\apps\gcc\current\include\C++\11.2.0\
```

It failed. clangd still cannot find `stdlib.h`, but use the mingw32 related path worked:

```
-isystem
C:\Users\username\scoop\apps\gcc\current\x86_64-w64-mingw32\include
```

And clangd successfully loaded stdlib.h, but throws another error. Log:

```
I[15:17:10.869] Features: windows+grpc
I[15:17:10.869] PID: 9948
I[15:17:10.870] Working directory: C:\Users\username\AppData\Roaming\nvim-data\mason\packages\clangd\clangd_16.0.2\bin
I[15:17:10.870] argv[0]: C:\Users\username\AppData\Roaming\nvim-data\mason\packages\clangd\clangd_16.0.2\bin\clangd.exe
I[15:17:10.870] argv[1]: --check=C:\Users\username\path\to\c_file.c
I[15:17:10.875] Entering check mode (no LSP server)
I[15:17:10.876] Testing on source file C:\Users\username\path\to\c_file.c
I[15:17:10.877] Loading compilation database...
I[15:17:10.886] Loaded compilation database from C:\Users\username\path\to\compile_flags.txt
I[15:17:10.887] Compile command from CDB is: "C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\bin\\clang-tool" -isystem "C:\\Users\\username\\scoop\\apps\\gcc\\current\\x86_64-w64-mingw32\\include" "-resource-dir=C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\lib\\clang\\16" -- "C:\\Users\\username\\path\\to\\c_file.c"
I[15:17:10.888] Parsing command...
I[15:17:10.899] internal (cc1) args are: -cc1 -triple x86_64-pc-windows-msvc19.20.0 -fsyntax-only -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name c_file.c -mrelocation-model pic -pic-level 2 -mframe-pointer=none -fmath-errno -ffp-contract=on -fno-rounding-math -mconstructor-aliases -funwind-tables=2 -target-cpu x86-64 -tune-cpu generic -mllvm -treat-scalable-fixed-error-as-warning "-fcoverage-compilation-dir=C:\\Users\\username\\path\\to" -resource-dir "C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\lib\\clang\\16" -isystem "C:\\Users\\username\\scoop\\apps\\gcc\\current\\x86_64-w64-mingw32\\include" -c-isystem "C:\\Users\\username\\scoop\\apps\\gcc\\current\\include" -cxx-isystem "C:\\Users\\username\\scoop\\apps\\gcc\\current\\include" -internal-isystem "C:\\Users\\username\\AppData\\Roaming\\nvim-data\\mason\\packages\\clangd\\clangd_16.0.2\\lib\\clang\\16\\include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 10.0/VC/include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 9.0/VC/include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 9.0/VC/PlatformSDK/Include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 8/VC/include" -internal-isystem "C:/Program Files/Microsoft Visual Studio 8/VC/PlatformSDK/Include" "-fdebug-compilation-dir=C:\\Users\\username\\path\\to" -ferror-limit 19 -fmessage-length=83 -fno-use-cxa-atexit -fms-extensions -fms-compatibility -fms-compatibility-version=19.20 -fdelayed-template-parsing -no-round-trip-args -faddrsig -x c "C:\\Users\\username\\path\\to\\c_file.c"
I[15:17:10.900] Building preamble...
I[15:17:10.916] Indexing headers...
I[15:17:10.925] Built preamble of size 352652 for file C:\Users\username\path\to\c_file.c version null in 0.02 seconds
E[15:17:10.926] [invalid_token_after_toplevel_declarator] Line 1: in included file: expected ';' after top level declarator
I[15:17:10.927] Building AST...
I[15:17:10.943] Indexing AST...
I[15:17:10.944] Building inlay hints
I[15:17:10.944] Building semantic highlighting
I[15:17:10.945] Testing features at each token (may be slow in large files)
I[15:17:10.968] All checks completed, 1 errors
```

Error: **[invalid_token_after_toplevel_declarator] Line 1: in included file: expected ';' after top level declarator.** Refer to [Issue #404 · clangd/vscode-clangd · GitHub](https://github.com/clangd/vscode-clangd/issues/404), add the last 2 lines to `compile_flags.txt` solves the issue:

```
-isystem
C:\Users\username\scoop\apps\gcc\current\x86_64-w64-mingw32\include
-target
x86_64-pc-windows-gnu
```
