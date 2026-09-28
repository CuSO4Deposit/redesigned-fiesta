---
title: How to type annotate a Gzipfile in Python?
date: 2024-10-05
lastMod: 2025-10-18
tags:
- lsp
- python
categories:
---

Pyright complains when I use the following code to process gzip files:


```python
import gzip
import os
import typing


def readfile(f: os.PathLike | typing.TextIO):
	pass

with gzip.open("/path/to/foo.gz", 'r') as input:
    readfile(input)
```

Diagnostics:
```
 Argument of type "GzipFile" cannot be assigned to parameter "file" of type "PathLike[Unknown] | TextIO" in func
 tion "readfile"
   Type "GzipFile" is incompatible with type "PathLike[Unknown] | TextIO"
     "GzipFile" is incompatible with protocol "PathLike[Unknown]"
       "__fspath__" is not present
     "GzipFile" is incompatible with "TextIO" [reportArgumentType]
```

## Text File inside

  + According to the gzip.open() docs:

> The *filename* argument can be an actual filename (a [str](https://docs.python.org/3/library/stdtypes.html#str) or [bytes](https://docs.python.org/3/library/stdtypes.html#bytes) object), or an existing file object to read from or write to.
>
> The *mode* argument can be any of 'r', 'rb', 'a', 'ab', 'w', 'wb', 'x' or 'xb' for binary mode, or 'rt', 'at', 'wt', or 'xt' for text mode. The default is 'rb'.
>
> For binary mode, this function is equivalent to the [GzipFile](https://docs.python.org/3/library/gzip.html#gzip.GzipFile) constructor: GzipFile(filename, mode, compresslevel). In this case, the *encoding*, *errors* and *newline* arguments must not be provided.
>
> For text mode, a [GzipFile](https://docs.python.org/3/library/gzip.html#gzip.GzipFile) object is created, and wrapped in an [io.TextIOWrapper](https://docs.python.org/3/library/io.html#io.TextIOWrapper) instance with the specified encoding, error handling behavior, and line ending(s).


  + Thus when opening a gzip file whose content is indeed a text file, we must explicitly specify the file mode `'t'` (in my case, `'rt'`), so that it returns a `io.TextIOWrapper` wrapped instance and won't annoy the lsp with annotation `typing.TextIO`.

## Binary File inside

  + `GzipFile` is not a file object. A type annotation `typing.BinaryIO` is not compatible with it. We can annotate the object with barely `GzipFile`.


  + > Constructor for the [GzipFile](https://docs.python.org/3/library/gzip.html#gzip.GzipFile) class, which simulates most of the methods of a [file object](https://docs.python.org/3/glossary.html#term-file-object), with the exception of the [truncate()](https://docs.python.org/3/library/io.html#io.IOBase.truncate) method.  At least one of *fileobj* and *filename* must be given a non-trivial value.

## References

  + [Stackoverflow: What exactly is a file-like object in Python?](https://stackoverflow.com/questions/4359495/what-exactly-is-a-file-like-object-in-python)


  + [Stackoverflow: Type hint for a file or file-like object?](https://stackoverflow.com/questions/38569401/type-hint-for-a-file-or-file-like-object)

  + [Stackoverflow: Why does mypy complain about TextIOWrapper receiving GzipFile as argument 1?](https://stackoverflow.com/questions/58394410/why-does-mypy-complain-about-textiowrapper-receiving-gzipfile-as-argument-1)

  + [GitHub: typeshed - typing.IO and io.BaseIO type hierarchies are incompatible](https://github.com/python/typeshed/issues/6077)
