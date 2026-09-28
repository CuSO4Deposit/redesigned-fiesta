---
title: Nix Language Basics
date: 2024-06-30
lastMod: 2025-10-18
tags:
- Nix
categories:
link: "https://nix.dev/tutorials/nix-language"
---

Nix is **[Functional]([[FP]])**, **Lazy evaluated**.


interactive interpreter: `nix repl`. Execute a file containing nix expression: `nix-instantiate --eval file.nix`.

`let` expression (`let` binding): specify binding scope

  + e.g. `let a=1; b=2; in a+b` -> `3`


datatypes:

  + attribute set `{ name1 = ...; name2 = ...; }`, where `...` can be a string, number, list or attribute set.


    + rec attribute set: `rec { ... }`, allow access to attributes within the set itself.


      + e.g. `rec {a = 1; b = a + 1;}` -> `{a = 1; b = 2;}`


    + attribute access with `.`

      + e.g. `let attrset = {a.b.c = 1}; in attrset.a.b` -> `{c = 1;}`


  + list `[a b c]`, separated by white space

  + bool `true`, `false`

  + inline comment `#...`

  + string `"something"`, multiline string uses double single quotes `''some\n\tthing''`

`with` expression: access attributes without repeatedly referencing the attribute set

  + e.g. `let a={x=1; y=2;}; in with a; [x y]` -> `[ 1 2 ]`


`inherit` expression: shorthand for assigning value from existing scope to the same name in a nested scope

  + e.g. `let x=1; y=2; in {inherit x y;}` -> `{x=1; y=2;}`


  + e.g. (specify attrset) `let a={x=1; y=2;} in {inherit (a) x y;}` -> `{x=1; y=2;}`

  + e.g. (in let expr) `let inherit ({x=1; y=2;}) x y; in [x y]` -> `[1 2]`

string interpolation: `${...}`

  + e.g. `let name="Nix"; in "Hello ${name}"` -> `"Hello Nix`


paths

  + absolute and relative paths are similar to bash


  + lookup paths (angle bracket paths)

    + depends on the value of `builtins.nixPath`


    + **Not recommended due to impurities**

    + e.g. `<nixpkgs>/lib` -> `"/nix/var/nix/profiles/per-user/root/channels/nixpkgs/lib"`

Functions

  + Whenever a colon (`:`) appears, it's a function. Functions are always anonymous.


  + Single argument

```
x: x + 1
```

  + Multiple arguments via nesting
```
x: y: x + y
```

  + Attribute set argument
```
{ a, b }: a + b
```

  + With default attributes

```
{ a, b ? 0 }: a + b
```

  + With additional attributes allowed

```
{ a, b, ...}: a + b
```

  + Named attribute set argument

```
args@{ a, b, ... }: a + b + args.c
```

or
```
{ a, b, ... }@args: a + b + args.c
```

Calling Functions

  + use `let` bindings to bind a name for a function
```nix
let f = x : x + 1; in f 1
```
or
```nix
let f = x: x.a; in f { a = 1; }
```


  + use parentheses when do not need a name
```nix
(x: x + 1) 1
```

Function Libraries

  + builtins


    + most builtins are accessible through `builtins`
```nix
a = "Hell${builtins.toString 0} World!";
```
or
```nix
a = "Hell${toString 0} World!";
```


    + import

      + takes a path to a Nix file, reads it and evaluate the contained nix expression, and returns the result value.


  + pkgs.lib

    + The [nixpkgs](https://github.com/NixOS/nixpkgs) repository contains an attribute set called [lib](https://github.com/NixOS/nixpkgs/blob/master/lib/default.nix), which provides a large number of useful functions.
They are implemented in the Nix language, as opposed to [builtins](https://nix.dev/tutorials/nix-language#builtins), which are part of the language itself.
```nix
let
  pkgs = import <nixpkgs> {};
in
pkgs.lib.strings.toUpper "lookup paths considered harmful"
```


Fetchers

  + Files to be used as build inputs do not have to come from the file system.
The Nix language provides built-in impure functions to fetch files over the network during evaluation:


  + [builtins.fetchurl](https://nix.dev/manual/nix/stable/language/builtins.html#builtins-fetchurl)

  + [builtins.fetchTarball](https://nix.dev/manual/nix/stable/language/builtins.html#builtins-fetchTarball)

  + [builtins.fetchGit](https://nix.dev/manual/nix/stable/language/builtins.html#builtins-fetchGit)

  + [builtins.fetchClosure](https://nix.dev/manual/nix/stable/language/builtins.html#builtins-fetchClosure)
These functions evaluate to a file system path in the Nix store.
Example:
```
builtins.fetchurl "https://github.com/NixOS/nix/archive/7c3ab5751568a0bc63430b33a5169c5e4784a0f
```

Derivations

  + The Nix language primitive to declare a derivation is the built-in impure function derivation.


  + It is usually wrapped by the Nixpkgs build mechanism `stdenv.mkDerivation`, which hides much of the complexity involved in non-trivial build procedures.

  + Whenever you encounter `mkDerivation`, it denotes something that Nix will eventually *build*.

Worked Examples

  + Shell environment
```nix
{ pkgs ? import <nixpkgs> {} }:
let
  message = "hello world";
in
pkgs.mkShellNoCC {
  buildInputs = with pkgs; [ cowsay ];
  shellHook = ''
    cowsay ${message}
  '';
}
```


  + NixOS configuration
```nix
{ config, pkgs, ... }: {
  imports = [ ./hardware-configuration.nix ];
  environment.systemPackages = with pkgs; [ git ];
  # ...
}
```
