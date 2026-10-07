---
title: Vim commands quickref
date: 2021-10-04
lastMod: 2021-10-04
tags:
- quickref
- vim
categories:
slug: vim-commands
---

## Move cursor

h and l : Left and Right.
k and j : Up and Down.


## Basic Edit

i: enter insert mode, cursor is before the highlighted character.
a: enter insert mode, cursor is after the highlighted character.

:wq: save and quit.
:q!: quit and do not save.

## Delete and Undo

x: delete the current highlighted character.

d: delete. Its basic format is d <number> <motion>.

motion:
w: move cursor to the next word's first letter.
e: move cursor to the current word's last letter.
$: move cursor to the end of this line.

then Delete Operation:
dw: delete until cursor get to the first letter of the next character.
d2e: do {delete until deleted the end of the current letter} twice.
... ...
dd: delete the whole line (and put it into the register).

u: undo.
U: undo all the operations to this line.
<Ctrl>+R: redo.

## Paste and Change

p: add things in register after the current cursor.
r<char>: keep in normal mode, replace the current character with <char>.

c: change. It has the same format with d.
cw: delete from cursor to the end of this word, and enter insert mode.

## Locate and File status

<Ctrl>+G: show which line the cursor is at, and file status.
G: jump to the last line of this file.
<number>G: jump to the <number>th line of the file.
gg: jump to the first line of this file.

## Search and Replace

/<string>: search <string> in this file.
?<string>: search <string> in this file, in reverse direction.
n: move to the next <string> found.
N: move to the previous <string> found.
<Ctrl>+O: cursor back to the previous location.
<Ctrl>+I: cursor to the newer location.
%: when cursor is on a brace/bracket, jump to the paired one.
:s/<old>/<new>: replace the first <old> in the cursor's line with <new>
:s/<old>/<new>/g: replace all the <old> in the cursor's line with <new>
:<line>,<line>s/<old>/<new>/g: replace all the <old> from <line> to <line> with <new>
:%s/<old>/<new>/g: replace all the <old> in the file with <new>
:%s/<old>/<new>/gc: replace all the <old> in the file with <new>, but prompt whether to substitute at each one.

## External Command

:!<Command>: execute command in cmd.

## File Operation

:w <filename>: save a new file <filename> at this dir.
v (motion) :w<filename>: save the selected part into <filename>.
:r <filename>: insert the content of <filename> to the cursor line.
:r !<Command>: read the output of external command <Command> and insert below the cursor line.

## Open and Append

o: open a line below the cursor line.
O: open a line above the cursor line.
R: enter replace mode.
y: copy. p: paste.
yw: copy a word.

## Set

:set <command>: set some options. e.g. :set ic means (ignore case), works when find and replace.
