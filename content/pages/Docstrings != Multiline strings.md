---
title: "Docstrings != Multiline strings"
date: 2025-02-28
lastMod: 2025-10-18
tags:
- python
categories:
---

Before python 3.13, docstrings are also not trimmed by default.


[Common leading spaces are trimmed from a docstring since 3.13](https://docs.python.org/3/whatsnew/3.13.html#other-language-changes).

But multiline strings are not treated so. Leading spaces are always what-you-see-is-what-you-get.

```python
% nix run nixpkgs#python313
Python 3.13.2 (main, Feb  4 2025, 14:51:09) [GCC 14.2.1 20241116] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> def a():
...     """This is a docstring
...     Its indent is not the same across lines.
...         This line has more indentation.
...     """
...     pass
...
>>> a.__doc__
'This is a docstring\nIts indent is not the same across lines.\n    This line has more indentation.\n'
>>> def a():
...     """
...     This is a docstring
...     Its indent is not the same across lines.
...         This line has more indentation.
...     """
...     pass
...
>>>
>>> a.__doc__
'\nThis is a docstring\nIts indent is not the same across lines.\n    This line has more indentation.\n'
>>> B = """
...     This is a multiline string
...         Its indent is also not the same across lines.
...     """
>>>
>>> B
'\n    This is a multiline string\n        Its indent is also not the same across lines.\n    '
>>> B = """\
...     This is a multiline string
...         Its indent is also not the same across lines.
...     """
>>> B
'    This is a multiline string\n        Its indent is also not the same across lines.\n    '
>>> exit

% nix run nixpkgs#python312
Python 3.12.9 (main, Feb  4 2025, 14:38:38) [GCC 14.2.1 20241116] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> def a():
...     """
...     This is a docstring.
...         Its indent balabala
...     """
...     pass
...
>>> a.__doc__
'\n\tThis is a docstring.\n\t    Its indent balabala\n\t'
```

#python
