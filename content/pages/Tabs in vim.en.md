---
title: Tabs in vim
date: 2024-10-11
lastMod: 2024-10-11
tags:
  - Neovim
  - Nixvim
  - vim
categories:
slug: vim-tabs
ai: translated
---

## Options Explanation

**expandtab**: a boolean value controls whether **the real input** is a tab character (\t) or the specified number of spaces.

```
                                 'expandtab' 'et' 'noexpandtab' 'noet'
'expandtab' 'et'        boolean (default off)
                        local to buffer
        In Insert mode: Use the appropriate number of spaces to insert a
        <Tab>.  Spaces are used in indents with the '>' and '<' commands and
        when 'autoindent' is on.  To insert a real tab when 'expandtab' is
        on, use CTRL-V<Tab>.  See also :retab and ins-expandtab.
```

**tabstop**: number of spaces a tab **visually** counts for. Defaults to 8. It does not affect how many spaces/tabs will be inserted directly.

```
                                                'tabstop' 'ts'
'tabstop' 'ts'          number  (default 8)
                        local to buffer
        Number of spaces that a <Tab> in the file counts for.  Also see
        the :retab command, and the 'softtabstop' option.

        Note: Setting 'tabstop' to any other value than 8 can make your file
        appear wrong in many places.
        The value must be more than 0 and less than 10000.
```

**shiftwidth**: number of columns to use when **indenting**, such as `>>`. When zero it falls back to `tabstop` value.

```
                                                'shiftwidth' 'sw'
'shiftwidth' 'sw'       number  (default 8)
                        local to buffer
        Number of spaces to use for each step of (auto)indent.  Used for
        'cindent', >>, <<, etc.
        When zero the 'ts' value will be used.  Use the shiftwidth()
        function to get the effective shiftwidth value.
```

**softtabstop**: a integet defaults to 0. It defined **how many columns moved** when \<tab\> is pressed or \<BS\>-ed. When `expandtab` is true, it always uses space, otherwise it uses a mix of spaces and tabs. A negative value makes it fall back to the value `shiftwidth`.

For example:

when `:set tabstop=4 softtabstop=8 noexpandtab`, pressing \<tab\> once will move you 8 columns right, inserting 2 tabs. When there are 14 spaces in the buffer, pressing \<BS\> will remove 6 (move you 6 columns left to the nearest tabstop), and next press will remove the 8 left.

when `set tabstop=8 softtabstop=4 noexpandtab`, pressing \<tab\> once will move you 4 columns right, it does so by inserting 4 spaces. Pressing \<tab\> again will move you 4 columns right again, but the former 8 spaces is now replaced by one tab (\t). Now press \<BS\> once, you are moved 4 columns left, the tab is now removed (because tabstop=8) and there are 4 spaces left.

when `set tabstop=4 softtabstop=0 noexpandtab`, the softtabstop feature is disabled. Each time you press \<tab\>, you insert a tab and moves to the next tabstop.

```
                                        'softtabstop' 'sts'
'softtabstop' 'sts'     number  (default 0)
                        local to buffer
        Number of spaces that a <Tab> counts for while performing editing
        operations, like inserting a <Tab> or using <BS>.  It "feels" like
        <Tab>s are being inserted, while in fact a mix of spaces and <Tab>s is
        used.  This is useful to keep the 'ts' setting at its standard value
        of 8, while being able to edit like it is set to 'sts'.  However,
        commands like "x" still work on the actual characters.
        When 'sts' is zero, this feature is off.
        When 'sts' is negative, the value of 'shiftwidth' is used.
        See also ins-expandtab.  When 'expandtab' is not set, the number of
        spaces is minimized by using <Tab>s.
        The 'L' flag in 'cpoptions' changes how tabs are used when 'list' is
        set.

        The value of 'softtabstop' will be ignored if 'varsofttabstop' is set
        to anything other than an empty string.
```

**smarttab**: a boolean value controls whether a tab length is `shiftwidth` or `tabstop`/`softtabstop`.

```
                                 'smarttab' 'sta' 'nosmarttab' 'nosta'
'smarttab' 'sta'        boolean (default on)
                        global
        When on, a <Tab> in front of a line inserts blanks according to
        'shiftwidth'.  'tabstop' or 'softtabstop' is used in other places.  A
        <BS> will delete a 'shiftwidth' worth of space at the start of the
        line.
        When off, a <Tab> always inserts blanks according to 'tabstop' or
        'softtabstop'.  'shiftwidth' is only used for shifting text left or
        right shift-left-right.
        What gets inserted (a <Tab> or spaces) depends on the 'expandtab'
        option.  Also see ins-expandtab.  When 'expandtab' is not set, the
        number of spaces is minimized by using <Tab>s.
```

**autoindent**: boolean value, defaults on. When starting a newline, copy indent from current line.

```
                        'autoindent' 'ai' 'noautoindent' 'noai'
'autoindent' 'ai'       boolean (default on)
                        local to buffer
        Copy indent from current line when starting a new line (typing <CR>
        in Insert mode or when using the "o" or "O" command).  If you do not
        type anything on the new line except <BS> or CTRL-D and then type
        <Esc>, CTRL-O or <CR>, the indent is deleted again.  Moving the cursor
        to another line has the same effect, unless the 'I' flag is included
        in 'cpoptions'.
        When autoindent is on, formatting (with the "gq" command or when you
        reach 'textwidth' in Insert mode) uses the indentation of the first
        line.
        When 'smartindent' or 'cindent' is on the indent is changed in
        a different way.
        {small difference from Vi: After the indent is deleted when typing
        <Esc> or <CR>, the cursor position when moving up or down is after the
        deleted indent; Vi puts the cursor somewhere in the deleted indent}.
```

**smartindent**: boolean value controls the behavior when dealing with `{`, `}`, or cinwords. Defaults to off.

```
                             'smartindent' 'si' 'nosmartindent' 'nosi'
'smartindent' 'si'      boolean (default off)
                        local to buffer
        Do smart autoindenting when starting a new line.  Works for C-like
        programs, but can also be used for other languages.  'cindent' does                                             something like this, works better in most cases, but is more strict,
        see C-indenting.  When 'cindent' is on or 'indentexpr' is set,
        setting 'si' has no effect.  'indentexpr' is a more advanced                                                    alternative.
        Normally 'autoindent' should also be on when using 'smartindent'.
        An indent is automatically inserted:                                                                            - After a line ending in "{".
        - After a line starting with a keyword from 'cinwords'.
        - Before a line starting with "}" (only with the "O" command).
        When typing '}' as the first character in a new line, that line is
        given the same indent as the matching "{".
        When typing '#' as the first character in a new line, the indent for
        that line is removed, the '#' is put in the first column.  The indent                                           is restored for the next line.  If you don't want this, use this                                                mapping: ":inoremap # X^H#", where ^H is entered with CTRL-V CTRL-H.
        When using the ">>" command, lines starting with '#' are not shifted
        right.
```

## Best practices

```
        There are four main ways to use tabs in Vim:
        1. Always keep 'tabstop' at 8, set 'softtabstop' and 'shiftwidth' to 4
           (or 3 or whatever you prefer) and use 'noexpandtab'.  Then Vim
           will use a mix of tabs and spaces, but typing <Tab> and <BS> will
           behave like a tab appears every 4 (or 3) characters.
        2. Set 'tabstop' and 'shiftwidth' to whatever you prefer and use
           'expandtab'.  This way you will always insert spaces.  The
           formatting will never be messed up when 'tabstop' is changed.
        3. Set 'tabstop' and 'shiftwidth' to whatever you prefer and use a
           modeline to set these values when editing the file again.  Only
           works when using Vim to edit the file.
        4. Always set 'tabstop' and 'shiftwidth' to the same value, and
           'noexpandtab'.  This should then work (for initial indents only)
           for any tabstop setting that people use.  It might be nice to have
           tabs after the first non-blank inserted as spaces if you do this
           though.  Otherwise aligned comments will be wrong when 'tabstop' is
           changed.
```

## How to set individual tab options for different filetypes?

in vim, use [autocmd](https://vimdoc.sourceforge.net/htmldoc/autocmd.html).

```vim
autocmd BufEnter *.py :setlocal tabstop=4 shiftwidth=4 expandtab
```

in neovim, use [ftplugin](https://neovim.io/doc/user/usr_41.html#ftplugin).

```lua
-- nvim/ftplugin/python.lua

vim.bo.tabstop = 4
vim.bo.shiftwidth = 4
vim.bo.expandtab = true
vim.bo.softtabstop = 4
```

in nixvim, use `files` sub-modules. [ref](https://github.com/nix-community/nixvim/discussions/2066)

```nix
programs.nixvim = {
  enable = true;

  files.foo = {
    path = "ftplugin/python.lua";
    opts.expandtab = true;
  };
};
```

and as in submodules `path` defaults to `name`, so this is also fine:

```nix
programs.nixvim = {
  enable = true;

  files."ftplugin/python.lua" = {
    opts.expandtab = true;
  };
};
```
